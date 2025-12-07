import os
import time
import tracemalloc
import numpy as np
from src.PetriNet import PetriNet
from src.BDD import bdd_reachable
from pyeda.inter import *

def test_001():
    P = ["p1", "p2", "p3"]
    T = ["t1", "t2", "t3"]
    I = np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]])
    O = np.array([[0,1,0],
                  [0,0,1],
                  [1,0,0]])
    M0 = np.array([1,0,0])
    bdd, count = bdd_reachable(PetriNet(P, T, P, T, I, O, M0))

    p1, p2, p3 = exprvar('p1'), exprvar('p2'), exprvar('p3')
    expected_expr = Or(And(~p1, ~p2, p3),
                    And(~p1, p2, ~p3),
                    And(p1, ~p2, ~p3))

    assert count == 3
    assert bdd2expr(bdd).equivalent(expected_expr) 

def test_002():
    P = ["p1", "p2", "p3"]
    T = ["t1", "t2", "t3"]
    I = np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]])
    O = np.array([[0,1,0],
                  [0,0,1],
                  [1,0,0]])
    M0 = np.array([1,0,1])
    bdd, count = bdd_reachable(PetriNet(P, T, P, T, I, O, M0))

    p1, p2, p3 = exprvar('p1'), exprvar('p2'), exprvar('p3')
    expected_expr = Or(And(~p1, p2, p3),
                    And(p1, p2, ~p3),
                    And(p1, ~p2, p3))

    assert count == 3
    assert bdd2expr(bdd).equivalent(expected_expr) 

def test_003():
    P = ["p1", "p2", "p3"]
    T = ["t1", "t2", "t3"]
    I = np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]])
    O = np.array([[0,1,0],
                  [0,0,1],
                  [1,0,0]])
    M0 = np.array([1,1,1])
    bdd, count = bdd_reachable(PetriNet(P, T, P, T, I, O, M0))

    p1, p2, p3 = exprvar('p1'), exprvar('p2'), exprvar('p3')
    expected_expr = Or(And(p1, p2, p3))

    assert count == 1
    assert bdd2expr(bdd).equivalent(expected_expr) 

def test_004():
    P = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7']
    T = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8']
    I = np.array([[1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 1, 0],
                [0, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0]])
    O = np.array([[0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 1],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0]])
    M0 = np.array([1, 0, 0, 0, 0, 0, 0])
    bdd, count = bdd_reachable(PetriNet(P, T, P, T, I, O, M0))

    p1, p2, p3, p4, p5, p6, p7 = [exprvar(i) for i in P]
    expected_expr = Or(
        And(~p1, ~p2, ~p3, ~p4, ~p5, ~p6, p7),
        And(~p1, ~p2, ~p3, p4, ~p5, p6, ~p7),
        And(~p1, ~p2, ~p3, p4, p5, ~p6, ~p7),
        And(~p1, ~p2, p3, ~p4, ~p5, p6, ~p7),
        And(~p1, ~p2, p3, ~p4, p5, ~p6, ~p7),
        And(~p1, p2, ~p3, ~p4, ~p5, p6, ~p7),
        And(~p1, p2, ~p3, ~p4, p5, ~p6, ~p7),
        And(p1, ~p2, ~p3, ~p4, ~p5, ~p6, ~p7)
    )
    
    assert count == 8
    assert bdd2expr(bdd).equivalent(expected_expr) 

def test_005():
    P = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7']
    T = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8']
    I = np.array([[1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 1, 0],
                [0, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0]])
    O = np.array([[0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 1],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0]])
    M0 = np.array([1, 0, 0, 0, 0, 1, 0])
    bdd, count = bdd_reachable(PetriNet(P, T, P, T, I, O, M0))

    p1, p2, p3, p4, p5, p6, p7 = [exprvar(i) for i in P]
    expected_expr = Or(
        And(~p1, ~p2, ~p3, ~p4, ~p5, p6, p7),
        And(~p1, ~p2, ~p3, ~p4, p5, ~p6, p7),
        And(~p1, ~p2, ~p3, p4, p5, p6, ~p7),
        And(~p1, ~p2, p3, ~p4, p5, p6, ~p7),
        And(~p1, p2, ~p3, ~p4, p5, p6, ~p7),
        And(p1, ~p2, ~p3, ~p4, ~p5, p6, ~p7)
    )
        
    assert count == 6
    assert bdd2expr(bdd).equivalent(expected_expr) 

'''
def test_007():
    P = ['P1', 'P2', 'P3', 'P4', 'P5']
    T = ['T1', 'T2', 'T3', 'T4']
    I = np.array([
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 1, 0, 0]
    ])
    O = np.array([
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1]
    ])
    M0 = np.array([1, 0, 0, 0, 0])
    bdd, count = bdd_reachable(PetriNet(P, T, P, T, I, O, M0))

    p1, p2, p3, p4, p5 = [exprvar(i) for i in P]
    expected_expr = Or(
        And(~p1, p2, ~p3, p4, p5),
        And(~p1, p2, p3, p4, ~p5),
        And(p1, ~p2, ~p3, ~p4, ~p5),
        And(p1, ~p2, ~p3, p4, p5),
        And(p1, ~p2, p3, p4, ~p5),
        And(p1, p2, ~p3, ~p4, ~p5)
    )

    assert count == 6
    assert bdd2expr(bdd).equivalent(expected_expr) 

'''

# Giả sử PetriNet và bdd_reachable đã được import từ module chính
# from PetriNet import PetriNet
# from your_module import bdd_reachable 
'''
def test_007():
    print("\n--- TEST: SIMPLE FORK SYSTEM (1 -> 2 Parallel -> 2 End) ---")

    # 1. Định nghĩa cấu trúc
    # P1: Start
    # P2: Task A Running, P3: Task B Running
    # P4: Task A Done,    P5: Task B Done
    P = ['P1', 'P2', 'P3', 'P4', 'P5']
    
    # T1: Fork (P1 -> P2, P3)
    # T2: Finish A (P2 -> P4)
    # T3: Finish B (P3 -> P5)
    T = ['T1', 'T2', 'T3']

    # 2. Ma trận Input (I) - [Số Transition x Số Place]
    # Dựa theo code của bạn, hàng là Transition, cột là Place
    I = np.array([
        [1, 0, 0, 0, 0], # T1 lấy P1
        [0, 1, 0, 0, 0], # T2 lấy P2
        [0, 0, 1, 0, 0]  # T3 lấy P3
    ])

    # 3. Ma trận Output (O) - [Số Transition x Số Place]
    O = np.array([
        [0, 1, 1, 0, 0], # T1 sinh ra P2, P3
        [0, 0, 0, 1, 0], # T2 sinh ra P4
        [0, 0, 0, 0, 1]  # T3 sinh ra P5
    ])

    # 4. Trạng thái đầu (M0): Có 1 token ở P1
    M0 = np.array([1, 0, 0, 0, 0])

    # 5. Khởi tạo đối tượng (theo constructor trong snippet của bạn)
    # PetriNet(place_ids, trans_ids, place_names, trans_names, I, O, M0)
    pn = PetriNet(P, T, P, T, I, O, M0)

    # 6. Chạy thuật toán
    bdd_result, count = bdd_reachable(pn)

    # 7. In kết quả để kiểm tra
    print(f"\n[RESULT] Số lượng trạng thái tìm được: {count}")
    
    # In công thức logic đại diện
    print("\n[LOGIC FORMULA] Biểu thức BDD:")
    print(bdd2expr(bdd_result))

    # In chi tiết từng trạng thái (Giải nén BDD ra danh sách)
    print("\n[DETAILS] Danh sách các Marking cụ thể:")
    solutions = list(bdd_result.satisfy_all())
    
    for i, sol in enumerate(solutions, 1):
        # Tạo chuỗi hiển thị dạng (1, 0, 0...) cho dễ nhìn
        state_vector = []
        for p_name in P:
            # Kiểm tra biến p có trong solution và bằng 1 không
            # Lưu ý: PyEDA trả về dict {var: 0/1}
            val = 0
            for var, value in sol.items():
                if str(var) == p_name:
                    val = value
                    break
            state_vector.append(val)
        
        print(f"  State #{i}: {state_vector} ", end="")
        
        # Chú thích ý nghĩa trạng thái
        if state_vector == [1, 0, 0, 0, 0]: print("-> (Start)")
        elif state_vector == [0, 1, 1, 0, 0]: print("-> (Forked: A & B running)")
        elif state_vector == [0, 0, 1, 1, 0]: print("-> (A done, B running)")
        elif state_vector == [0, 1, 0, 0, 1]: print("-> (B done, A running)")
        elif state_vector == [0, 0, 0, 1, 1]: print("-> (All Done)")
        else: print("-> (Unknown/Error?)")

    assert count == 6
    assert bdd2expr(bdd).equivalent(expected_expr) 
'''

def test_007_benchmark():
    print("\n" + "="*50)
    print("TEST: LOAD FROM PNML FILE WITH BENCHMARKING")
    print("="*50)
    
    # 1. Đường dẫn file PNML
    filename = "input.pnml"

    # 2. Đọc PetriNet từ file
    print(f"Reading file: {filename}...")
    try:
        pn = PetriNet.from_pnml(filename)
    except Exception as e:
        print(f"Lỗi khi đọc file PNML: {e}")
        return
    
    print("--- Petri Net Info ---")
    print(f"Places: {len(pn.place_names)} nodes")
    print(f"Transitions: {len(pn.trans_names)} transitions")
    print("----------------------")

    # ====================================================
    # BẮT ĐẦU ĐO HIỆU NĂNG (BENCHMARK START)
    # ====================================================
    
    # Bắt đầu theo dõi bộ nhớ
    tracemalloc.start()
    
    # Bắt đầu bấm giờ
    start_time = time.perf_counter()

    # 3. Chạy thuật toán Symbolic Reachable (Core Algorithm)
    bdd_result, count = bdd_reachable(pn)

    # Dừng bấm giờ
    end_time = time.perf_counter()
    
    # Lấy thông số bộ nhớ (current, peak)
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    
    # Dừng theo dõi bộ nhớ
    tracemalloc.stop()
    
    # Tính toán thời gian chạy (đổi ra milliseconds cho dễ nhìn)
    elapsed_time_ms = (end_time - start_time) * 1000
    
    # Đổi byte ra MB
    peak_mem_mb = peak_mem / (1024 * 1024)

    # ====================================================
    # KẾT THÚC ĐO HIỆU NĂNG (BENCHMARK END)
    # ====================================================

    # 4. In kết quả thuật toán
    print(f"\n[RESULT] Số lượng trạng thái tìm được: {count}")
    
    # (Tùy chọn) In công thức logic nếu muốn kiểm tra
    # print("\n[LOGIC FORMULA]:")
    # print(bdd2expr(bdd_result))

    # 5. Liệt kê chi tiết các Marking tìm được
    print("\n[DETAILS] Danh sách các Marking cụ thể:")
    solutions = list(bdd_result.satisfy_all())
    
    for i, sol in enumerate(solutions, 1):
        state_vector = []
        current_active_places = []
        
        # Mapping solution map về vector
        sol_str_key = {str(k): v for k, v in sol.items()}
        
        for p_name in pn.place_names: 
            val = sol_str_key.get(p_name, 0)
            state_vector.append(val)
            if val == 1:
                current_active_places.append(p_name)
        
        print(f"  State #{i}: {state_vector} -> Active: {current_active_places}")

    # 6. In Báo cáo Hiệu năng
    print("\n" + "-"*40)
    print("PERFORMANCE REPORT")
    print("-"*40)
    print(f"Execution Time : {elapsed_time_ms:.4f} ms")
    print(f"Peak Memory    : {peak_mem_mb:.6f} MB")
    print("-"*40)

    # 7. Assertions (Kiểm tra tính đúng đắn)
    # Bài toán người lái đò thường có số trạng thái cụ thể (ví dụ 16 hoặc ít hơn tùy cách mô hình)
    # Bạn cần thay số 6 bằng con số thực tế của bài toán man_boat_riddle
    assert count == 6
    assert bdd2expr(bdd).equivalent(expected_expr) 