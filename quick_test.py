"""Quick benchmark test for BDD optimization"""
import time
import tracemalloc
import os
from src.PetriNet import PetriNet
from src.BDD import bdd_reachable

def test_bdd(filename):
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return
    
    pn = PetriNet.from_pnml(filename)
    print(f"\n{filename}: {len(pn.place_names)} places, {len(pn.trans_names)} transitions")
    
    # Warmup
    tracemalloc.start()
    
    t1 = time.perf_counter()
    _, count = bdd_reachable(pn)
    t2 = time.perf_counter()
    
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    time_ms = (t2 - t1) * 1000
    mem_mb = peak_mem / (1024 * 1024)
    
    print(f"  States: {count}")
    print(f"  Time:   {time_ms:.2f} ms")
    print(f"  Memory: {mem_mb:.4f} MB")
    return time_ms, mem_mb, count

if __name__ == "__main__":
    print("="*60)
    print("BDD OPTIMIZATION TEST")
    print("="*60)
    
    test_files = [
        "input.pnml",       # Small
        "input2.pnml",      # Small  
        "parallel.pnml",    # BDD was 24ms, BFS was 2120ms
        "ring.pnml",        # BDD was 60ms
        "large_dining_5phil.pnml",  # BDD was 350ms
        "large_dining_6phil.pnml",  # BDD was 1562ms
        "source_sink.pnml", # Medium
        "selfloop.pnml",    # Medium
    ]
    
    results = []
    for f in test_files:
        result = test_bdd(f)
        if result:
            results.append((f, *result))
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"{'File':<30} | {'Time (ms)':<12} | {'Memory (MB)':<12} | {'States'}")
    print("-"*70)
    for name, time_ms, mem_mb, count in results:
        print(f"{name:<30} | {time_ms:<12.2f} | {mem_mb:<12.4f} | {count}")
