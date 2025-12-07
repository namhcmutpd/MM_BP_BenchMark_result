"""
run_all_test.py - Benchmark BDD vs Explicit (BFS & DFS) cho tất cả Petri Net
File này chạy benchmark cho tất cả các file .pnml trong thư mục Test_cases
và xuất kết quả ra Benchmark_output/result.csv và Benchmark_output/result.txt
"""

import os
import sys
import time
import tracemalloc
import gc
import csv
from datetime import datetime
from typing import Dict, List, Optional, Any

# Thêm src vào path và cài đặt để import các module
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
sys.path.insert(0, ROOT_DIR)

# Tạo fake package 'src' để relative import hoạt động
import types
src_package = types.ModuleType('src')
src_package.__path__ = [SRC_DIR]
sys.modules['src'] = src_package

# Giờ có thể import bình thường
from src.PetriNet import PetriNet
from src.BDD import bdd_reachable
from src.BFS import bfs_reachable
from src.DFS import dfs_reachable


def measure_performance(algo_name: str, func, pn: PetriNet, timeout_seconds: float = 300) -> Optional[Dict[str, Any]]:
    """
    Đo thời gian và bộ nhớ của một thuật toán.
    
    Args:
        algo_name: Tên thuật toán
        func: Hàm thực thi
        pn: Petri Net
        timeout_seconds: Thời gian tối đa cho phép (giây)
    
    Returns:
        Dictionary chứa kết quả hoặc None nếu thất bại
    """
    # Force GC before starting
    gc.collect()
    
    # Reset và bắt đầu đo bộ nhớ
    tracemalloc.stop()
    tracemalloc.start()
    
    # Bắt đầu bấm giờ
    start_time = time.perf_counter()
    
    try:
        if algo_name == "BDD":
            # BDD trả về (bdd_object, count)
            _, count = func(pn)
        else:
            # BFS/DFS trả về Set[Tuple]
            visited_set = func(pn)
            count = len(visited_set)
            
    except Exception as e:
        tracemalloc.stop()
        return {
            "name": algo_name,
            "count": "ERROR",
            "time_ms": -1,
            "memory_mb": -1,
            "error": str(e)
        }
        
    # Dừng bấm giờ
    end_time = time.perf_counter()
    
    # Lấy thông số bộ nhớ (peak)
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Tính toán
    elapsed_time_ms = (end_time - start_time) * 1000
    peak_mem_mb = peak_mem / (1024 * 1024)
    
    return {
        "name": algo_name,
        "count": count,
        "time_ms": elapsed_time_ms,
        "memory_mb": peak_mem_mb,
        "error": None
    }


def get_pnml_files(test_folder: str) -> List[str]:
    """Lấy danh sách các file .pnml trong thư mục Test_cases, sắp xếp theo tên."""
    pnml_files = []
    if os.path.exists(test_folder):
        for f in os.listdir(test_folder):
            if f.endswith('.pnml'):
                pnml_files.append(os.path.join(test_folder, f))
    
    # Sắp xếp theo số trong tên file
    def extract_number(filepath):
        filename = os.path.basename(filepath)
        # Trích xuất số từ tên file (vd: input1.pnml -> 1)
        num_str = ''.join(filter(str.isdigit, filename))
        return int(num_str) if num_str else 0
    
    return sorted(pnml_files, key=extract_number)


def run_benchmark_all(test_folder: str = "Test_cases", output_folder: str = "Benchmark_output"):
    """
    Chạy benchmark cho tất cả các file Petri Net và xuất kết quả.
    """
    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(output_folder, exist_ok=True)
    
    # Lấy danh sách file PNML
    pnml_files = get_pnml_files(test_folder)
    
    if not pnml_files:
        print(f"Không tìm thấy file .pnml nào trong {test_folder}")
        return
    
    print("=" * 80)
    print("BENCHMARK: BDD vs BFS vs DFS (Reachability Analysis)")
    print(f"Thời gian chạy: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Số lượng file: {len(pnml_files)}")
    print("=" * 80)
    
    # Kết quả tổng hợp
    all_results = []
    
    for idx, pnml_file in enumerate(pnml_files, 1):
        filename = os.path.basename(pnml_file)
        print(f"\n[{idx}/{len(pnml_files)}] Processing: {filename}")
        print("-" * 60)
        
        # Đọc Petri Net
        try:
            pn = PetriNet.from_pnml(pnml_file)
            num_places = len(pn.place_names)
            num_trans = len(pn.trans_names)
            print(f"  Places: {num_places}, Transitions: {num_trans}")
        except Exception as e:
            print(f"  ERROR: Không thể đọc file - {e}")
            all_results.append({
                "file": filename,
                "places": "N/A",
                "transitions": "N/A",
                "bdd_states": "ERROR",
                "bdd_time_ms": -1,
                "bdd_memory_mb": -1,
                "bfs_states": "ERROR",
                "bfs_time_ms": -1,
                "bfs_memory_mb": -1,
                "dfs_states": "ERROR",
                "dfs_time_ms": -1,
                "dfs_memory_mb": -1
            })
            continue
        
        # Chạy 3 thuật toán
        result_entry = {
            "file": filename,
            "places": num_places,
            "transitions": num_trans
        }
        
        # BDD
        print("  Running BDD...", end=" ", flush=True)
        res_bdd = measure_performance("BDD", bdd_reachable, pn)
        if res_bdd:
            result_entry["bdd_states"] = res_bdd["count"]
            result_entry["bdd_time_ms"] = res_bdd["time_ms"]
            result_entry["bdd_memory_mb"] = res_bdd["memory_mb"]
            status = "OK" if res_bdd["error"] is None else f"ERROR: {res_bdd['error']}"
            print(f"{status} (States: {res_bdd['count']}, Time: {res_bdd['time_ms']:.2f}ms)")
        
        # BFS
        print("  Running BFS...", end=" ", flush=True)
        res_bfs = measure_performance("BFS", bfs_reachable, pn)
        if res_bfs:
            result_entry["bfs_states"] = res_bfs["count"]
            result_entry["bfs_time_ms"] = res_bfs["time_ms"]
            result_entry["bfs_memory_mb"] = res_bfs["memory_mb"]
            status = "OK" if res_bfs["error"] is None else f"ERROR: {res_bfs['error']}"
            print(f"{status} (States: {res_bfs['count']}, Time: {res_bfs['time_ms']:.2f}ms)")
        
        # DFS
        print("  Running DFS...", end=" ", flush=True)
        res_dfs = measure_performance("DFS", dfs_reachable, pn)
        if res_dfs:
            result_entry["dfs_states"] = res_dfs["count"]
            result_entry["dfs_time_ms"] = res_dfs["time_ms"]
            result_entry["dfs_memory_mb"] = res_dfs["memory_mb"]
            status = "OK" if res_dfs["error"] is None else f"ERROR: {res_dfs['error']}"
            print(f"{status} (States: {res_dfs['count']}, Time: {res_dfs['time_ms']:.2f}ms)")
        
        all_results.append(result_entry)
    
    # Xuất kết quả ra file
    export_results_csv(all_results, output_folder)
    export_results_txt(all_results, output_folder)
    
    print("\n" + "=" * 80)
    print("BENCHMARK HOÀN TẤT!")
    print(f"Kết quả được lưu tại:")
    print(f"  - {os.path.join(output_folder, 'result.csv')}")
    print(f"  - {os.path.join(output_folder, 'result.txt')}")
    print("=" * 80)


def export_results_csv(results: List[Dict], output_folder: str):
    """Xuất kết quả ra file CSV."""
    csv_file = os.path.join(output_folder, "result.csv")
    
    fieldnames = [
        "file", "places", "transitions",
        "bdd_states", "bdd_time_ms", "bdd_memory_mb",
        "bfs_states", "bfs_time_ms", "bfs_memory_mb",
        "dfs_states", "dfs_time_ms", "dfs_memory_mb"
    ]
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def export_results_txt(results: List[Dict], output_folder: str):
    """Xuất kết quả ra file TXT với định dạng bảng."""
    txt_file = os.path.join(output_folder, "result.txt")
    
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("=" * 140 + "\n")
        f.write("BENCHMARK RESULTS: BDD vs BFS vs DFS (Reachability Analysis)\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 140 + "\n\n")
        
        # Header
        header = (
            f"{'File':<15} | {'Places':>6} | {'Trans':>6} | "
            f"{'BDD States':>12} | {'BDD Time(ms)':>14} | {'BDD Mem(MB)':>12} | "
            f"{'BFS States':>12} | {'BFS Time(ms)':>14} | {'BFS Mem(MB)':>12} | "
            f"{'DFS States':>12} | {'DFS Time(ms)':>14} | {'DFS Mem(MB)':>12}"
        )
        f.write(header + "\n")
        f.write("-" * 140 + "\n")
        
        # Data rows
        for r in results:
            def fmt_val(val, is_time=False, is_mem=False):
                if val == "ERROR" or val == "N/A" or val == -1:
                    return "N/A"
                if is_time:
                    return f"{val:.4f}"
                if is_mem:
                    return f"{val:.6f}"
                return str(val)
            
            row = (
                f"{r['file']:<15} | {str(r['places']):>6} | {str(r['transitions']):>6} | "
                f"{fmt_val(r.get('bdd_states', 'N/A')):>12} | {fmt_val(r.get('bdd_time_ms', -1), is_time=True):>14} | {fmt_val(r.get('bdd_memory_mb', -1), is_mem=True):>12} | "
                f"{fmt_val(r.get('bfs_states', 'N/A')):>12} | {fmt_val(r.get('bfs_time_ms', -1), is_time=True):>14} | {fmt_val(r.get('bfs_memory_mb', -1), is_mem=True):>12} | "
                f"{fmt_val(r.get('dfs_states', 'N/A')):>12} | {fmt_val(r.get('dfs_time_ms', -1), is_time=True):>14} | {fmt_val(r.get('dfs_memory_mb', -1), is_mem=True):>12}"
            )
            f.write(row + "\n")
        
        f.write("-" * 140 + "\n")
        
        # Tổng hợp thống kê
        f.write("\n" + "=" * 80 + "\n")
        f.write("TỔNG HỢP THỐNG KÊ\n")
        f.write("=" * 80 + "\n\n")
        
        # Tính tổng và trung bình
        valid_results = [r for r in results if r.get('bdd_time_ms', -1) > 0]
        
        if valid_results:
            # Tổng thời gian
            total_bdd_time = sum(r['bdd_time_ms'] for r in valid_results)
            total_bfs_time = sum(r['bfs_time_ms'] for r in valid_results if r.get('bfs_time_ms', -1) > 0)
            total_dfs_time = sum(r['dfs_time_ms'] for r in valid_results if r.get('dfs_time_ms', -1) > 0)
            
            f.write(f"Tổng thời gian BDD: {total_bdd_time:.4f} ms\n")
            f.write(f"Tổng thời gian BFS: {total_bfs_time:.4f} ms\n")
            f.write(f"Tổng thời gian DFS: {total_dfs_time:.4f} ms\n\n")
            
            # Tổng bộ nhớ
            total_bdd_mem = sum(r['bdd_memory_mb'] for r in valid_results)
            total_bfs_mem = sum(r['bfs_memory_mb'] for r in valid_results if r.get('bfs_memory_mb', -1) > 0)
            total_dfs_mem = sum(r['dfs_memory_mb'] for r in valid_results if r.get('dfs_memory_mb', -1) > 0)
            
            f.write(f"Tổng bộ nhớ BDD: {total_bdd_mem:.6f} MB\n")
            f.write(f"Tổng bộ nhớ BFS: {total_bfs_mem:.6f} MB\n")
            f.write(f"Tổng bộ nhớ DFS: {total_dfs_mem:.6f} MB\n\n")
            
            # So sánh hiệu suất
            f.write("-" * 80 + "\n")
            f.write("SO SÁNH HIỆU SUẤT (BDD vs Explicit Methods)\n")
            f.write("-" * 80 + "\n\n")
            
            if total_bfs_time > 0:
                speedup_vs_bfs = total_bfs_time / total_bdd_time if total_bdd_time > 0 else 0
                f.write(f"Tỉ lệ tốc độ BDD/BFS: {speedup_vs_bfs:.2f}x\n")
            
            if total_dfs_time > 0:
                speedup_vs_dfs = total_dfs_time / total_bdd_time if total_bdd_time > 0 else 0
                f.write(f"Tỉ lệ tốc độ BDD/DFS: {speedup_vs_dfs:.2f}x\n")
            
            if total_bfs_mem > 0:
                mem_ratio_bfs = total_bfs_mem / total_bdd_mem if total_bdd_mem > 0 else 0
                f.write(f"Tỉ lệ bộ nhớ BFS/BDD: {mem_ratio_bfs:.2f}x\n")
            
            if total_dfs_mem > 0:
                mem_ratio_dfs = total_dfs_mem / total_bdd_mem if total_bdd_mem > 0 else 0
                f.write(f"Tỉ lệ bộ nhớ DFS/BDD: {mem_ratio_dfs:.2f}x\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")


if __name__ == "__main__":
    run_benchmark_all()
