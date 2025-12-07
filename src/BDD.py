from typing import Tuple, List, Dict, Set
import numpy as np
from dd import autoref as _bdd
from src.PetriNet import PetriNet

def bdd_reachable(pn: PetriNet) -> Tuple[object, int]:
    """
    Tính toán Reachability sử dụng BDD (Binary Decision Diagrams).
    
    OPTIMIZED VERSION - Các tối ưu chính:
    1. Frame Condition Cache: Tính equiv BDDs 1 lần, dùng nhiều lần
    2. Pre-computed Lists: Truy cập O(1) thay vì dict lookup
    3. NumPy Vectorization: Dùng np.flatnonzero thay vì Python loops
    4. Monolithic Transition Relation: Gộp tất cả transitions, tận dụng BDD sharing
    5. Memory Efficient: Dùng int8, cleanup sớm các objects không cần
    6. Interleaved Variable Ordering: Giảm kích thước BDD
    """

    # --- 1. SETUP & CHUẨN HÓA DỮ LIỆU ---
    I = np.asarray(pn.I, dtype=np.int8)
    O = np.asarray(pn.O, dtype=np.int8)
    M0 = np.asarray(pn.M0, dtype=np.int8)

    raw_place_names = getattr(pn, "place_names", None) or []
    num_places_declared = len(raw_place_names)
    rows, cols = I.shape
    
    # Auto-transpose nếu ma trận bị ngược
    if cols == num_places_declared and rows != num_places_declared:
        I, O = I.T, O.T
    
    num_places, num_trans = I.shape
    
    # Resize M0 nếu cần
    if M0.shape[0] != num_places:
        new_M0 = np.zeros(num_places, dtype=np.int8)
        new_M0[:min(M0.shape[0], num_places)] = M0[:min(M0.shape[0], num_places)]
        M0 = new_M0

    # Tạo tên biến BDD
    place_ids = getattr(pn, "place_ids", None) or []
    bdd_var_names: List[str] = []
    
    for i in range(num_places):
        name = None
        if i < len(raw_place_names) and raw_place_names[i]:
            name = str(raw_place_names[i])
        elif i < len(place_ids) and place_ids[i]:
            name = str(place_ids[i])
        bdd_var_names.append((name or f"P{i}").replace(" ", "_").replace("-", "_"))

    bdd_var_names_p = [n + "_p" for n in bdd_var_names]

    # --- 2. KHỞI TẠO BDD MANAGER ---
    bdd = _bdd.BDD()
    
    # Interleaved ordering: x0, x0', x1, x1'...
    ordered_vars = []
    for i in range(num_places):
        ordered_vars.extend([bdd_var_names[i], bdd_var_names_p[i]])
    bdd.declare(*ordered_vars)
    
    # Pre-fetch BDD nodes vào lists
    x_nodes = [bdd.var(bdd_var_names[i]) for i in range(num_places)]
    xp_nodes = [bdd.var(bdd_var_names_p[i]) for i in range(num_places)]
    
    # Cache equivalence BDDs: equiv[i] = (x[i] <-> x'[i])
    equiv_cache = [(x_nodes[i] & xp_nodes[i]) | (~x_nodes[i] & ~xp_nodes[i]) 
                   for i in range(num_places)]

    # --- 3. XÂY DỰNG MONOLITHIC TRANSITION RELATION ---
    I_bool = I > 0
    O_bool = O > 0
    T_monolithic = bdd.false
    
    for t in range(num_trans):
        input_idx = np.flatnonzero(I_bool[:, t])
        output_idx = np.flatnonzero(O_bool[:, t])
        
        if len(input_idx) == 0 and len(output_idx) == 0:
            continue
            
        input_set = set(input_idx)
        output_set = set(output_idx)
        affected_set = input_set | output_set
        
        # Enable condition
        enable = bdd.true
        for idx in input_idx:
            enable &= x_nodes[idx]
        for idx in output_idx:
            if idx not in input_set:
                enable &= ~x_nodes[idx]
        
        if enable == bdd.false:
            continue
        
        # Update condition  
        change = bdd.true
        for idx in input_idx:
            change &= xp_nodes[idx] if idx in output_set else ~xp_nodes[idx]
        for idx in output_idx:
            if idx not in input_set:
                change &= xp_nodes[idx]
        
        # Frame condition (dùng cache)
        frame = bdd.true
        for i in range(num_places):
            if i not in affected_set:
                frame &= equiv_cache[i]
        
        T_monolithic |= enable & change & frame
    
    del equiv_cache  # Cleanup

    # --- 4. TRẠNG THÁI KHỞI TẠO ---
    R = bdd.true
    for i in range(num_places):
        R &= x_nodes[i] if M0[i] else ~x_nodes[i]
    
    # --- 5. REACHABILITY LOOP (FRONTIER OPTIMIZATION) ---
    frontier = R
    rename_map = {bdd_var_names_p[i]: bdd_var_names[i] for i in range(num_places)}
    q_vars = set(bdd_var_names)
    
    while True:
        conj = frontier & T_monolithic
        if conj == bdd.false:
            break
        
        img = bdd.quantify(conj, q_vars, forall=False)
        img_renamed = bdd.let(rename_map, img)
        new_states = img_renamed & ~R
        
        if new_states == bdd.false:
            break
        
        R |= new_states
        frontier = new_states

    # --- 6. ĐẾM SỐ LƯỢNG ---
    return R, int(bdd.count(R, nvars=num_places))