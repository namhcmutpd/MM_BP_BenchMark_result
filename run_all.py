import os
import time
import tracemalloc
import numpy as np
import csv
from pathlib import Path
from datetime import datetime

# Import các module của bạn
from src.PetriNet import PetriNet
from src.BDD import bdd_reachable
from src.BFS import bfs_reachable
from src.DFS import dfs_reachable

def measure_performance(algo_name, func, pn):
    """
    Hàm phụ trợ để đo thời gian và bộ nhớ của một thuật toán.
    """
    print(f"    {algo_name:<20}", end=" ", flush=True)
    
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
    
    print("✓")
    return {
        "name": algo_name,
        "count": count,
        "time_ms": elapsed_time_ms,
        "memory_mb": peak_mem_mb
    }

def test_single_file(filename):
    """
    Test một file Petri Net với cả 3 thuật toán.
    Trả về dictionary chứa kết quả.
    """
    print(f"\nTesting: {filename}")
    
    if not os.path.exists(filename):
        print(f"  ❌ Lỗi: Không tìm thấy file {filename}.")
        return None

    # Đọc PetriNet
    print(f"  Reading file...", end=" ", flush=True)
    try:
        pn = PetriNet.from_pnml(filename)
        print("✓")
    except Exception as e:
        print(f"FAILED! ({e})")
        return None
        
    places_count = len(pn.place_names)
    trans_count = len(pn.trans_names)
    print(f"  Net Info: {places_count} places, {trans_count} transitions.")

    # Chạy lần lượt 3 thuật toán
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

    # Kiểm tra tính đúng đắn (Consistency Check)
    consistency_ok = True
    if len(results) == 3:
        count_bdd = results[0]['count']
        count_bfs = results[1]['count']
        count_dfs = results[2]['count']
        
        if count_bdd == count_bfs == count_dfs:
            print(f"  ✅ Consistency check: PASS (All found {count_bdd} states)")
        else:
            print(f"  ❌ Consistency check: FAIL")
            print(f"     BDD: {count_bdd}, BFS: {count_bfs}, DFS: {count_dfs}")
            consistency_ok = False

    return {
        "filename": filename,
        "places": places_count,
        "transitions": trans_count,
        "results": results,
        "consistency_ok": consistency_ok
    }

def find_pnml_files():
    """
    Tìm tất cả các file .pnml trong thư mục hiện tại.
    """
    pnml_files = []
    for file in os.listdir('.'):
        if file.endswith('.pnml'):
            pnml_files.append(file)
    return sorted(pnml_files)

def generate_summary_report(all_results, output_file="benchmark_results.txt"):
    """
    Tạo file tổng hợp kết quả so sánh hiệu suất.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*100 + "\n")
        f.write("PETRI NET REACHABILITY ANALYSIS - BENCHMARK REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*100 + "\n\n")

        # Tóm tắt từng file
        for file_result in all_results:
            if file_result is None:
                continue
            
            f.write(f"\nFile: {file_result['filename']}\n")
            f.write(f"  Places: {file_result['places']}, Transitions: {file_result['transitions']}\n")
            f.write("-" * 100 + "\n")
            f.write(f"  {'ALGORITHM':<20} | {'STATES':<12} | {'TIME (ms)':<20} | {'MEMORY (MB)':<20}\n")
            f.write("-" * 100 + "\n")
            
            for res in file_result['results']:
                f.write(f"  {res['name']:<20} | {res['count']:<12} | {res['time_ms']:<20.4f} | {res['memory_mb']:<20.6f}\n")
            
            consistency_status = "✅ PASS" if file_result['consistency_ok'] else "❌ FAIL"
            f.write(f"\n  Consistency Check: {consistency_status}\n")

        # Bảng so sánh tổng hợp
        f.write("\n\n" + "="*100 + "\n")
        f.write("PERFORMANCE COMPARISON SUMMARY\n")
        f.write("="*100 + "\n\n")
        
        f.write(f"{'FILE':<35} | {'BDD Time':<20} | {'BFS Time':<20} | {'DFS Time':<20}\n")
        f.write("-" * 100 + "\n")
        
        for file_result in all_results:
            if file_result is None or len(file_result['results']) < 3:
                continue
            
            filename = file_result['filename']
            bdd_time = file_result['results'][0]['time_ms']
            bfs_time = file_result['results'][1]['time_ms']
            dfs_time = file_result['results'][2]['time_ms']
            
            f.write(f"{filename:<35} | {bdd_time:<20.4f} | {bfs_time:<20.4f} | {dfs_time:<20.4f}\n")

        # Thống kê tổng hợp
        f.write("\n\n" + "="*100 + "\n")
        f.write("AGGREGATE STATISTICS\n")
        f.write("="*100 + "\n\n")
        
        bdd_times = []
        bfs_times = []
        dfs_times = []
        bdd_mems = []
        bfs_mems = []
        dfs_mems = []
        
        for file_result in all_results:
            if file_result is None or len(file_result['results']) < 3:
                continue
            
            bdd_times.append(file_result['results'][0]['time_ms'])
            bfs_times.append(file_result['results'][1]['time_ms'])
            dfs_times.append(file_result['results'][2]['time_ms'])
            bdd_mems.append(file_result['results'][0]['memory_mb'])
            bfs_mems.append(file_result['results'][1]['memory_mb'])
            dfs_mems.append(file_result['results'][2]['memory_mb'])
        
        f.write("EXECUTION TIME (ms):\n")
        f.write("-" * 60 + "\n")
        f.write(f"  BDD Symbolic:\n")
        f.write(f"    Mean:   {np.mean(bdd_times):.4f} ms\n")
        f.write(f"    Median: {np.median(bdd_times):.4f} ms\n")
        f.write(f"    Std:    {np.std(bdd_times):.4f} ms\n")
        f.write(f"    Min:    {np.min(bdd_times):.4f} ms\n")
        f.write(f"    Max:    {np.max(bdd_times):.4f} ms\n\n")
        
        f.write(f"  BFS Explicit:\n")
        f.write(f"    Mean:   {np.mean(bfs_times):.4f} ms\n")
        f.write(f"    Median: {np.median(bfs_times):.4f} ms\n")
        f.write(f"    Std:    {np.std(bfs_times):.4f} ms\n")
        f.write(f"    Min:    {np.min(bfs_times):.4f} ms\n")
        f.write(f"    Max:    {np.max(bfs_times):.4f} ms\n\n")
        
        f.write(f"  DFS Explicit:\n")
        f.write(f"    Mean:   {np.mean(dfs_times):.4f} ms\n")
        f.write(f"    Median: {np.median(dfs_times):.4f} ms\n")
        f.write(f"    Std:    {np.std(dfs_times):.4f} ms\n")
        f.write(f"    Min:    {np.min(dfs_times):.4f} ms\n")
        f.write(f"    Max:    {np.max(dfs_times):.4f} ms\n\n")
        
        f.write("MEMORY USAGE (MB):\n")
        f.write("-" * 60 + "\n")
        f.write(f"  BDD Symbolic:\n")
        f.write(f"    Mean:   {np.mean(bdd_mems):.6f} MB\n")
        f.write(f"    Median: {np.median(bdd_mems):.6f} MB\n")
        f.write(f"    Std:    {np.std(bdd_mems):.6f} MB\n")
        f.write(f"    Min:    {np.min(bdd_mems):.6f} MB\n")
        f.write(f"    Max:    {np.max(bdd_mems):.6f} MB\n\n")
        
        f.write(f"  BFS Explicit:\n")
        f.write(f"    Mean:   {np.mean(bfs_mems):.6f} MB\n")
        f.write(f"    Median: {np.median(bfs_mems):.6f} MB\n")
        f.write(f"    Std:    {np.std(bfs_mems):.6f} MB\n")
        f.write(f"    Min:    {np.min(bfs_mems):.6f} MB\n")
        f.write(f"    Max:    {np.max(bfs_mems):.6f} MB\n\n")
        
        f.write(f"  DFS Explicit:\n")
        f.write(f"    Mean:   {np.mean(dfs_mems):.6f} MB\n")
        f.write(f"    Median: {np.median(dfs_mems):.6f} MB\n")
        f.write(f"    Std:    {np.std(dfs_mems):.6f} MB\n")
        f.write(f"    Min:    {np.min(dfs_mems):.6f} MB\n")
        f.write(f"    Max:    {np.max(dfs_mems):.6f} MB\n\n")

        # So sánh hiệu suất
        f.write("\n" + "="*100 + "\n")
        f.write("PERFORMANCE COMPARISON\n")
        f.write("="*100 + "\n\n")
        
        avg_bdd = np.mean(bdd_times)
        avg_bfs = np.mean(bfs_times)
        avg_dfs = np.mean(dfs_times)
        
        f.write(f"Average Execution Time:\n")
        f.write(f"  BDD:  {avg_bdd:.4f} ms\n")
        f.write(f"  BFS:  {avg_bfs:.4f} ms\n")
        f.write(f"  DFS:  {avg_dfs:.4f} ms\n\n")
        
        fastest = min([("BDD", avg_bdd), ("BFS", avg_bfs), ("DFS", avg_dfs)], key=lambda x: x[1])
        f.write(f"Fastest Algorithm: {fastest[0]} ({fastest[1]:.4f} ms)\n\n")
        
        f.write(f"Speed Comparison (relative to fastest):\n")
        f.write(f"  BDD: {avg_bdd/fastest[1]:.2f}x\n")
        f.write(f"  BFS: {avg_bfs/fastest[1]:.2f}x\n")
        f.write(f"  DFS: {avg_dfs/fastest[1]:.2f}x\n\n")
        
        f.write("="*100 + "\n")

def generate_csv_report(all_results, output_file="benchmark_results.csv"):
    """
    Tạo file CSV để dễ phân tích dữ liệu.
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Filename', 'Places', 'Transitions', 'Algorithm', 'States Found', 'Time (ms)', 'Memory (MB)', 'Consistency OK'])
        
        for file_result in all_results:
            if file_result is None:
                continue
            
            for res in file_result['results']:
                writer.writerow([
                    file_result['filename'],
                    file_result['places'],
                    file_result['transitions'],
                    res['name'],
                    res['count'],
                    f"{res['time_ms']:.4f}",
                    f"{res['memory_mb']:.6f}",
                    "Yes" if file_result['consistency_ok'] else "No"
                ])

def main():
    print("\n" + "="*100)
    print("PETRI NET REACHABILITY ANALYSIS - BENCHMARK FOR ALL FILES")
    print("="*100)
    
    # Tìm tất cả các file .pnml
    pnml_files = find_pnml_files()
    
    if not pnml_files:
        print("❌ Không tìm thấy file .pnml nào trong thư mục hiện tại.")
        return
    
    print(f"\n✓ Found {len(pnml_files)} PNML files:\n")
    for i, f in enumerate(pnml_files, 1):
        print(f"  {i}. {f}")
    
    print("\n" + "-"*100)
    
    # Test từng file
    all_results = []
    for filename in pnml_files:
        result = test_single_file(filename)
        all_results.append(result)
    
    print("\n" + "-"*100)
    
    # Tạo file tổng hợp
    print("\n📊 Generating summary reports...")
    generate_summary_report(all_results, "benchmark_results.txt")
    generate_csv_report(all_results, "benchmark_results.csv")
    print(f"  ✓ Text report: benchmark_results.txt")
    print(f"  ✓ CSV report: benchmark_results.csv")
    
    print("\n" + "="*100)
    print("BENCHMARK COMPLETE!")
    print("="*100 + "\n")

if __name__ == "__main__":
    main()
