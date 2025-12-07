# 🔬 TASK 3: Symbolic Reachability Analysis using BDD

**Symbolic computation of reachable markings by using BDD (Binary Decision Diagrams)**

> Encode markings symbolically using Binary Decision Diagrams (BDDs). Construct the reachability set iteratively by symbolic image computation. Return a BDD representing the set of all reachable markings. Report the total number of reachable markings and compare performance with the explicit approach (time and memory).

---

## 📊 Benchmark Results Summary

| Test Case | States | BDD (ms) | BFS (ms) | DFS (ms) | Winner | Speedup |
|-----------|--------|----------|----------|----------|--------|---------|
| example.pnml | **1,048,559** | 8,664 | 852,830 | 433,816 | 🏆 **BDD** | **98x vs BFS** |
| parallel.pnml | 4,096 | 48 | 2,245 | 819 | 🏆 **BDD** | **46x vs BFS** |
| mixed_stress.pnml | 1,536 | 116 | 1,120 | 441 | 🏆 **BDD** | **9.6x vs BFS** |
| source_sink.pnml | 256 | 57 | 150 | 64 | 🏆 **BDD** | **2.6x vs BFS** |
| large_parallel_5x4.pnml | 1,024 | 139 | 344 | 180 | 🏆 **BDD** | **2.5x vs BFS** |
| large_parallel_4x5.pnml | 625 | 142 | 217 | 108 | DFS | 1.5x vs BFS |
| input.pnml | 13 | 29 | 3.8 | 1.7 | DFS | - |
| input2.pnml | 5 | 7.6 | 0.7 | 0.3 | DFS | - |
| ring.pnml | 8 | 11 | 1.3 | 0.7 | DFS | - |

### 📈 Key Findings

- **BDD excels with large state spaces**: Up to **98x faster** than BFS for 1M+ states
- **Memory efficient**: BDD uses ~48MB for 1M states vs ~232MB for explicit methods  
- **Explicit methods win for small nets**: DFS is fastest for < 100 states
- **Crossover point**: BDD becomes advantageous around **500-1000 states**

---

## 🛠️ Installation

### 1. Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Run Full Benchmark
```bash
python run_full_benchmark.py
```
This generates:
- `benchmark_results.txt` - Detailed report with statistics
- `benchmark_results.csv` - Data for analysis/visualization

### Run Unit Tests
```bash
# Run all tests
python -m pytest -vv test_BDD.py

# Run specific test
python -m pytest -vv test_BDD.py::test_001
```

### Quick Test
```bash
python quick_test.py
```

### Test Single File
```python
from src.PetriNet import PetriNet
from src.BDD import bdd_reachable

pn = PetriNet.from_pnml("testcases/parallel.pnml")
bdd_result, count = bdd_reachable(pn)
print(f"Reachable states: {count}")
```

---

## 📁 Project Structure

```
TASK3_BTL_HK251-main/
├── src/
│   ├── BDD.py          # 🔑 Optimized BDD implementation
│   ├── BFS.py          # Explicit BFS algorithm
│   ├── DFS.py          # Explicit DFS algorithm
│   └── PetriNet.py     # PNML parser
├── testcases/          # 📂 All PNML test files
│   ├── example.pnml    # Large test (1M+ states)
│   ├── parallel.pnml   # Parallel structure
│   ├── ring.pnml       # Ring topology
│   └── ...             # 17 test files total
├── benchmark_results.txt   # 📊 Detailed results
├── benchmark_results.csv   # 📊 CSV for analysis
├── run_full_benchmark.py   # Benchmark script
├── test_BDD.py            # Unit tests
└── requirements.txt       # Dependencies
```

---

## ⚡ BDD Optimizations Applied

| Optimization | Description | Impact |
|--------------|-------------|--------|
| **Frame Condition Cache** | Pre-compute equivalence BDDs once | Reduces redundant computation |
| **Monolithic Transition Relation** | Combine all transitions into single BDD | Better node sharing |
| **Interleaved Variable Ordering** | `x0, x0', x1, x1'...` ordering | Compact BDD representation |
| **NumPy Vectorization** | Use `np.flatnonzero()` | Faster index computation |
| **Memory Efficient Types** | Use `np.int8` instead of `np.int64` | 8x memory reduction |
| **Early Termination** | Skip impossible transitions | Avoid unnecessary computation |

---

## 📝 Algorithm Overview

```
Input: Petri Net (Places, Transitions, I/O matrices, Initial Marking)
Output: BDD representing all reachable markings, Count of reachable states

1. Initialize BDD Manager with interleaved variable ordering
2. Encode initial marking M0 as BDD
3. Build transition relation T(x, x') for all transitions:
   - Enable condition: input places have tokens
   - Update condition: consume/produce tokens  
   - Frame condition: unchanged places keep their value
4. Iterative reachability (frontier-based):
   WHILE new states found:
     - Compute image: Next = ∃x. (Frontier(x) ∧ T(x, x'))
     - Rename x' → x
     - Add new states to Reachable set
     - Update Frontier = newly discovered states
5. Count satisfying assignments of final BDD
```

---

## 📊 Detailed Benchmark Results

See [benchmark_results.txt](benchmark_results.txt) for complete statistics including:
- Execution time comparison (all 17 test files)
- Memory usage analysis  
- Speedup calculations
- Consistency verification

See [benchmark_results.csv](benchmark_results.csv) for raw data.

---

## 📋 Requirements

- Python 3.8+
- `dd` - Decision Diagram library
- `numpy` - Numerical operations
- `pytest` - Testing framework

---

<p align="center">
  <b>BDD-based Symbolic Model Checking for Petri Net Reachability</b><br>
  <i>Optimized implementation achieving up to 98x speedup over explicit methods</i>
</p>

---

<p align="center">
  <a href="https://github.com/namhcmutpd/MM_BP_BenchMark_result">
    <img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
</p>

---

<p align="center">
  <a href="https://www.facebook.com/Shiba.Vo.Tien">
    <img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"/>
  </a>
  <a href="https://www.tiktok.com/@votien_shiba">
    <img src="https://img.shields.io/badge/TikTok-000000?style=for-the-badge&logo=tiktok&logoColor=white" alt="TikTok"/>
  </a>
  <a href="https://www.facebook.com/groups/khmt.ktmt.cse.bku?locale=vi_VN">
    <img src="https://img.shields.io/badge/Facebook%20Group-4267B2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook Group"/>
  </a>
  <a href="https://www.facebook.com/CODE.MT.BK">
    <img src="https://img.shields.io/badge/Page%20CODE.MT.BK-0057FF?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook Page"/>
  </a>
  <a href="https://github.com/VoTienBKU">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
</p>
