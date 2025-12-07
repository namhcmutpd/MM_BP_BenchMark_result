from typing import Tuple, List, Dict, Set
import numpy as np
from dd import autoref as _bdd
from src.PetriNet import PetriNet

# TASK 3 
def bdd_reachable(pn: PetriNet) -> Tuple[object, int]:
    '''
    --- 1. SETUP & CHUẨN HÓA DỮ LIỆU ---
    Do các ma trận I và O được nhóm em dùng có dạng
    hàng là places, cột là transitions, 1 tương ứng 
    có cung từ place đến transition, ngược lại là 0 nên chỉ cần dùng int8 là đủ
    Nên ta chuyển đổi chúng sang numpy array với dtype là int8 để tiết kiệm bộ nhớ
    Đồng thời, ta kiểm tra và tự động chuyển vị ma trận I và O nếu cần
    để đảm bảo số hàng tương ứng với số place thực tế
    Ngoài ra, ta cũng chuẩn hóa kích thước của M0 nếu cần thiết
    '''
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

    '''
    Resize M0 nếu cần ( Nếu số lượng place trong M0 khác với số lượng place thực tế)
    Tạo mảng mới với kích thước đúng với toàn bộ giá trị là 0
    và sao chép giá trị từ M0 cũ sang mảng mới
    '''
    if M0.shape[0] != num_places:
        new_M0 = np.zeros(num_places, dtype=np.int8) 
        new_M0[:min(M0.shape[0], num_places)] = M0[:min(M0.shape[0], num_places)] 
        M0 = new_M0

    # Tạo tên biến BDD
    # Sử dụng tên place nếu có, nếu không thì dùng place ID, nếu vẫn không có thì dùng tên mặc định P[i]
    place_ids = getattr(pn, "place_ids", None) or [] 
    bdd_var_names: List[str] = []
    
    for i in range(num_places):
        name = None
        if i < len(raw_place_names) and raw_place_names[i]: 
            name = str(raw_place_names[i]) 
        elif i < len(place_ids) and place_ids[i]:
            name = str(place_ids[i]) 
        bdd_var_names.append((name or f"P{i}").replace(" ", "").replace("-", "")) 
                                                                                   
    bdd_var_names_p = [n + "_p" for n in bdd_var_names] # Mảng lưu tên biến BDD cho trạng sau khi fire ( p1 -> p1_p)
    
    '''
     --- 2. KHỞI TẠO BDD MANAGER ---
    '''

    bdd = _bdd.BDD()

    # Interleaved ordering: x0, x0', x1, x1'...
    ordered_vars = []
    for i in range(num_places):
        ordered_vars.extend([bdd_var_names[i], bdd_var_names_p[i]])
    bdd.declare(*ordered_vars)
    # Đặt thứ tự biến trong BDD theo kiểu xen kẽ: x0, x0', x1, x1' 
    # để tối ưu hóa hiệu suất thao tác BDD sau này

    # Pre-fetch BDD nodes vào lists
    x_nodes = [bdd.var(bdd_var_names[i]) for i in range(num_places)] # BDD nodes cho trạng thái hiện tại x[i] để truy cập nhanh
    xp_nodes = [bdd.var(bdd_var_names_p[i]) for i in range(num_places)] # BDD nodes cho trạng thái tiếp theo x'[i] để truy cập nhanh


    # Cache equivalence BDDs: equiv[i] = (x[i] <-> x'[i])
    equiv_cache = [(x_nodes[i] & xp_nodes[i]) | (~x_nodes[i] & ~xp_nodes[i])  
                   for i in range(num_places)]
    ''' 
    Vì khi 1 transition bắn, chỉ 1 số ít place bị ảnh hưởng phần còn lại sẽ giữ nguyên trạng thái
    Nên ta dùng cache này để tái sử dụng, dùng nó làm khung và chỉ thay đổi những place bị ảnh hưởng
    giúp giảm thiểu số lượng thao tác BDD cần thiết
    '''

    '''
     --- 3. XÂY DỰNG MONOLITHIC TRANSITION RELATION ---
     Phần này xây dựng BDD biểu diễn quan hệ chuyển đổi monolithic T_monolithic
     từ ma trận I và O của Petri net thông qua việc lặp qua từng transition và 
     kết hợp các điều kiện enable, update và frame
    '''

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
        affected_set = input_set | output_set # Tập hợp các place bị ảnh hưởng bởi transition t

        '''
        Enable condition
        Điều kiện enable: tất cả input phải có token
        và tất cả output không thuộc input (không phải self-loop) không có token
        '''
        enable = bdd.true
        for idx in input_idx:
            enable &= x_nodes[idx] 
        for idx in output_idx:
            if idx not in input_set: 
                enable &= ~x_nodes[idx] 
        
        if enable == bdd.false: # Mâu thuẫn, bỏ qua transition này
            continue
        
        '''
        Update condition  
        Điều kiện update: cập nhật trạng thái các place bị ảnh hưởng
        input mất token (nếu không phải self-loop), output nhận token (nếu không phải self-loop)
        '''
        change = bdd.true
        for idx in input_idx:
            change &= xp_nodes[idx] if idx in output_set else ~xp_nodes[idx]
        for idx in output_idx:
            if idx not in input_set:
                change &= xp_nodes[idx]

        '''
        Frame condition (dùng cache)
        Với những place không bị ảnh hưởng ( không phải input hay output)
        giữ nguyên trạng thái bằng cách sử dụng cache
        '''
        frame = bdd.true
        for i in range(num_places):         
            if i not in affected_set:       
                frame &= equiv_cache[i]     
        
        T_monolithic |= enable & change & frame
        # Cập nhật transition (kết hợp điều kiện enable, update và frame) vào transition relation
    
    del equiv_cache   

    # --- 4. TRẠNG THÁI KHỞI TẠO ---
    # Đầu tiên, initial marking M0 đươc thêm vào tập trạng thái reachable R
    R = bdd.true 
    for i in range(num_places):
        R &= x_nodes[i] if M0[i] else ~x_nodes[i] 
    
    # --- 5. REACHABILITY LOOP  ---
    '''
    Vòng lặp tìm kiếm các trạng thái reachable mới từ frontier hiện tại
    Đầu tiên, frontier được khởi tạo bằng tập R ban đầu
    Trong mỗi vòng lặp, ta tính giao của frontier với T_monolithic để tìm
    các trạng thái có thể đạt được từ frontier
    Sau đó, sử dụng phép lượng tử hóa để loại bỏ biến hiện tại x[i], chỉ giữ lại biến tiếp theo x'[i]
    Tiếp theo, đổi tên biến x'[i] thành x[i] để tiếp tục xử lý
    Lọc ra các trạng thái mới chưa có trong tập R
    Nếu tìm thấy trạng thái mới, cập nhật tập R và frontier để tiếp tục tìm kiếm
    Ngược lại, nếu không tìm thấy trạng thái mới, vòng lặp kết thúc
    '''
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
    return R, int(bdd.count(R, nvars=num_places)) # Trả về BDD của tập trạng thái reachable và số lượng trạng thái trong đó