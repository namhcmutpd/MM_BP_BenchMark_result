import os
import time
import tracemalloc
import numpy as np

# Import các module của bạn
from src.PetriNet import PetriNet
from src.BDD import bdd_reachable
from src.BFS import bfs_reachable
from src.DFS import dfs_reachable

def measure_performance(algo_name, func, pn):
    """
    Hàm phụ trợ để đo thời gian và bộ nhớ của một thuật toán.
    """
    print(f"Running {algo_name}...", end=" ", flush=True)
    
    # 1. Reset và Bắt đầu đo bộ nhớ
    tracemalloc.stop() # Stop nếu đang chạy
    tracemalloc.start()
    
    # 2. Bắt đầu bấm giờ
    start_time = time.perf_counter()
    
    # 3. Chạy thuật toán
    try:
        if algo_name == "BDD Symbolic":
            # BDD trả về (bdd_object, count)
            _, count = func(pn)
        else:
            # BFS/DFS trả về Set[Tuple]
            visited_set = func(pn)
            count = len(visited_set)
            
    except Exception as e:
        print(f"FAILED! ({e})")
        return None
        
    # 4. Dừng bấm giờ
    end_time = time.perf_counter()
    
    # 5. Lấy thông số bộ nhớ (peak)
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # 6. Tính toán
    elapsed_time_ms = (end_time - start_time) * 1000
    peak_mem_mb = peak_mem / (1024 * 1024)
    
    print("Done.")
    return {
        "name": algo_name,
        "count": count,
        "time_ms": elapsed_time_ms,
        "memory_mb": peak_mem_mb
    }

def test_compare_algorithms():
    print("\n" + "="*60)
    print("BENCHMARK: BDD vs BFS vs DFS (Reachability Analysis)")
    print("="*60)
    
    # 1. Cấu hình file PNML
    filename = "example.pnml"
    
    if not os.path.exists(filename):
        print(f"Lỗi: Không tìm thấy file {filename}.")
        return

    # 2. Đọc PetriNet
    print(f"Reading file: {filename}...")
    try:
        pn = PetriNet.from_pnml(filename)
    except Exception as e:
        print(f"Lỗi đọc file: {e}")
        return
        
    print(f"Net Info: {len(pn.place_names)} places, {len(pn.trans_names)} transitions.")
    print("-" * 60)

    # 3. Chạy lần lượt 3 thuật toán
    results = []
    
    # --- A. BDD Symbolic ---
    res_bdd = measure_performance("BDD Symbolic", bdd_reachable, pn)
    if res_bdd: results.append(res_bdd)
    
    # --- B. BFS Explicit ---
    res_bfs = measure_performance("BFS Explicit", bfs_reachable, pn)
    if res_bfs: results.append(res_bfs)
    
    # --- C. DFS Explicit ---
    res_dfs = measure_performance("DFS Explicit", dfs_reachable, pn)
    if res_dfs: results.append(res_dfs)

    # 4. In Bảng So Sánh
    print("\n" + "="*65)
    print(f"{'ALGORITHM':<15} | {'STATES':<10} | {'TIME (ms)':<15} | {'MEMORY (MB)':<15}")
    print("-" * 65)
    
    for res in results:
        print(f"{res['name']:<15} | {res['count']:<10} | {res['time_ms']:<15.4f} | {res['memory_mb']:<15.6f}")
    print("="*65)

    # 5. Kiểm tra tính đúng đắn (Consistency Check)
    # Số lượng trạng thái tìm được phải giống hệt nhau giữa các thuật toán
    if len(results) == 3:
        count_bdd = results[0]['count']
        count_bfs = results[1]['count']
        count_dfs = results[2]['count']
        
        if count_bdd == count_bfs == count_dfs:
            print("\n✅ KẾT QUẢ KHỚP: Cả 3 thuật toán đều tìm ra cùng số lượng trạng thái.")
        else:
            print("\n❌ CẢNH BÁO: Kết quả không khớp!")
            print(f"   BDD: {count_bdd}, BFS: {count_bfs}, DFS: {count_dfs}")

if __name__ == "__main__":
    test_compare_algorithms()