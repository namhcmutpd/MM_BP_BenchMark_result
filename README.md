# BÁO CÁO TASK 3: SO SÁNH HIỆU SUẤT PHƯƠNG PHÁP BDD VÀ EXPLICIT TRONG PHÂN TÍCH REACHABILITY ANALYSIS TRONG PETRI NET

## 1. Giới thiệu

Báo cáo này trình bày kết quả so sánh hiệu suất giữa hai phương pháp phân tích Reachability Analysis trên mô hình Petri Net:

- **Phương pháp Symbolic (BDD - Binary Decision Diagram)**: Sử dụng cấu trúc dữ liệu BDD để biểu diễn và thao tác trên tập trạng thái một cách tượng trưng.
- **Phương pháp Explicit (BFS & DFS)**: Duyệt và lưu trữ từng trạng thái cụ thể trong không gian trạng thái.

Mục tiêu của TASK là đánh giá và so sánh thời gian thực thi, mức sử dụng bộ nhớ, cũng như khả năng mở rộng (scalability) của các phương pháp trên các Petri Net có kích thước khác nhau.

---

## 2. Phương pháp thực nghiệm

### 2.1. Môi trường thực nghiệm

- **Ngôn ngữ lập trình**: Python 3.14
- **Thư viện BDD**: `dd` (autoref)
- **Số lượng test case**: 15 file Petri Net (định dạng PNML)
- **Các chỉ số đo lường**:
  - Số lượng trạng thái đạt được
  - Thời gian thực thi (ms)
  - Bộ nhớ sử dụng (MB)

### 2.2. Thuật toán được so sánh

| Thuật toán | Mô tả |
|------------|-------|
| **BDD Symbolic** | Sử dụng Binary Decision Diagram với frontier optimization |
| **BFS Explicit** | Breadth-First Search - duyệt theo chiều rộng |
| **DFS Explicit** | Depth-First Search - duyệt theo chiều sâu |

---

## 3. Kết quả thực nghiệm

### 3.1. Bảng kết quả chi tiết

| File | Places | Trans | BDD States | BDD Time(ms) | BDD Mem(MB) | BFS States | BFS Time(ms) | BFS Mem(MB) | DFS States | DFS Time(ms) | DFS Mem(MB) |
|------|--------|-------|------------|--------------|-------------|------------|--------------|-------------|------------|--------------|-------------|
| input1.pnml | 4 | 2 | 3 | 3.74 | 0.051 | 3 | 1.42 | 0.003 | 3 | 0.19 | 0.002 |
| input2.pnml | 5 | 4 | 3 | 3.70 | 0.069 | 3 | 0.52 | 0.003 | 3 | 0.26 | 0.003 |
| input3.pnml | 4 | 2 | 2 | 1.72 | 0.035 | 2 | 0.34 | 0.003 | 2 | 0.16 | 0.002 |
| input4.pnml | 23 | 23 | 3072 | 166.91 | 3.038 | 3072 | 2760.20 | 0.791 | 3072 | 1121.42 | 0.801 |
| input5.pnml | 8 | 6 | 6 | 9.55 | 0.235 | 6 | 1.05 | 0.004 | 6 | 0.54 | 0.004 |
| input6.pnml | 8 | 12 | 36 | 31.80 | 0.721 | 36 | 9.56 | 0.009 | 36 | 5.54 | 0.008 |
| input7.pnml | 15 | 20 | 1536 | 105.98 | 2.031 | 1536 | 1080.42 | 0.365 | 1536 | 500.80 | 0.362 |
| input8.pnml | 12 | 12 | 4096 | 47.68 | 0.812 | 4096 | 2293.28 | 0.668 | 4096 | 936.82 | 0.659 |
| input9.pnml | 8 | 10 | 20 | 17.73 | 0.361 | 20 | 9.73 | 0.007 | 20 | 5.49 | 0.006 |
| input10.pnml | 8 | 8 | 8 | 12.58 | 0.252 | 8 | 1.32 | 0.004 | 8 | 0.76 | 0.004 |
| input11.pnml | 10 | 6 | 16 | 12.53 | 0.318 | 16 | 4.50 | 0.006 | 16 | 1.84 | 0.005 |
| input12.pnml | 12 | 16 | 256 | 41.14 | 0.773 | 256 | 161.86 | 0.045 | 256 | 71.08 | 0.044 |
| input13.pnml | 28 | 21 | 16384 | 337.49 | 5.759 | 16384 | 8760.08 | 4.637 | 16384 | 4334.67 | 4.628 |
| input14.pnml | 32 | 24 | 65536 | 491.83 | 8.179 | 65536 | 54358.85 | 20.512 | 65536 | 41300.47 | 20.503 |
| input15.pnml | 36 | 27 | 262144 | 1482.65 | 11.629 | 262144 | 370359.67 | 90.012 | 262144 | 189472.09 | 90.003 |

### 3.2. Tổng hợp thống kê

| Chỉ số | BDD | BFS | DFS |
|--------|-----|-----|-----|
| **Tổng thời gian (ms)** | 2767.01 | 439802.79 | 237752.11 |
| **Tổng bộ nhớ (MB)** | 34.26 | 117.07 | 117.03 |

### 3.3. Tỉ lệ so sánh hiệu suất

| So sánh | Tỉ lệ |
|---------|-------|
| Tốc độ BDD nhanh hơn BFS | **158.95x** |
| Tốc độ BDD nhanh hơn DFS | **85.92x** |
| Bộ nhớ BFS/BDD | 3.42x |
| Bộ nhớ DFS/BDD | 3.42x |

---

## 4. Phân tích và đánh giá

### 4.1. Ưu điểm của phương pháp BDD

#### 4.1.1. Hiệu suất thời gian vượt trội trên Petri Net lớn

Kết quả thực nghiệm cho thấy phương pháp BDD thể hiện **ưu thế rõ rệt về thời gian thực thi** khi kích thước không gian trạng thái tăng lên:

- Với **input13.pnml** (28 places, 21 transitions, 16384 states): BDD hoàn thành trong **337.49ms**, trong khi BFS cần **8760.08ms** (chậm hơn ~26 lần) và DFS cần **4334.67ms** (chậm hơn ~12.8 lần).
- Với **input14.pnml** (32 places, 24 transitions, 65536 states): BDD hoàn thành trong **491.83ms**, trong khi BFS cần **54358.85ms** (chậm hơn ~110.5 lần) và DFS cần **41300.47ms** (chậm hơn ~84 lần).
- Với **input15.pnml** (36 places, 27 transitions, 262144 states): BDD hoàn thành trong **1482.65ms**, trong khi BFS cần **370359.67ms** (chậm hơn ~249.8 lần) và DFS cần **189472.09ms** (chậm hơn ~127.8 lần).

#### 4.1.2. Khả năng mở rộng (Scalability)

Phương pháp BDD cho thấy khả năng mở rộng tốt hơn nhiều so với phương pháp explicit:

- **Độ phức tạp không gian**: BDD biểu diễn tập trạng thái một cách nén gọn thông qua cấu trúc đồ thị quyết định nhị phân, thay vì lưu từng trạng thái riêng lẻ.
- **Độ phức tạp thời gian**: Các phép toán trên BDD (giao, hợp, lượng tử hóa) được thực hiện hiệu quả nhờ cơ chế memoization và unique table.

#### 4.1.3. Tính tối ưu trong frontier exploration

Implementation BDD sử dụng **frontier optimization**, chỉ tính toán trạng thái mới từ frontier (tập trạng thái vừa khám phá), thay vì tính lại từ toàn bộ tập đã đạt được. Điều này giúp giảm đáng kể số phép toán cần thực hiện.

#### 4.1.4. Interleaved variable ordering

Việc sắp xếp biến theo kiểu interleaved (x0, x0', x1, x1', ...) giúp tối ưu hóa hiệu suất của các phép toán BDD, đặc biệt là phép quantification và rename.

### 4.2. Hạn chế của phương pháp BDD

#### 4.2.1. Tiêu tốn bộ nhớ cao hơn cho Petri Net nhỏ

Với các Petri Net nhỏ, BDD sử dụng bộ nhớ nhiều hơn do chi phí khởi tạo BDD manager và các cấu trúc dữ liệu hỗ trợ. Tuy nhiên, với các Petri Net lớn, BDD lại **tiết kiệm bộ nhớ hơn ~3.4 lần** so với Explicit.

#### 4.2.2. Không hiệu quả bằng Explicit cho Petri Net rất nhỏ

Với các Petri Net có số lượng places và transitions nhỏ (input1, input2, input3), phương pháp explicit thực sự nhanh hơn BDD do:

- Chi phí khởi tạo BDD lớn hơn lợi ích thu được.
- Không gian trạng thái nhỏ không phát huy được ưu thế nén của BDD.

#### 4.2.3. Phụ thuộc vào variable ordering

Hiệu suất của BDD phụ thuộc nhiều vào thứ tự các biến. Một variable ordering không tốt có thể dẫn đến kích thước BDD tăng theo hàm mũ, làm giảm hiệu quả của phương pháp.

---

## 5. Kết luận

### 5.1. Tổng kết

Qua kết quả thực nghiệm, nhóm rút ra các kết luận sau:

1. **Phương pháp BDD vượt trội về thời gian** khi không gian trạng thái lớn (từ hàng nghìn đến hàng trăm nghìn trạng thái), với tốc độ nhanh hơn từ **85 đến 160 lần** so với các phương pháp Explicit.

2. **BDD tiết kiệm bộ nhớ hơn ~3.4 lần** so với Explicit khi xử lý các Petri Net lớn.

3. **Phương pháp Explicit phù hợp với Petri Net nhỏ** do chi phí khởi tạo thấp và implementation đơn giản.

### 5.2. Khuyến nghị sử dụng

| Kích thước Petri Net | Phương pháp khuyến nghị |
|----------------------|-------------------------|
| Nhỏ (< 10 places, < 100 states) | DFS hoặc BFS |
| Trung bình (10-20 places, 100-1000 states) | BDD |
| Lớn (> 20 places, > 1000 states) | **BDD (bắt buộc)** |

---

## 6. Hướng dẫn chạy chương trình

### 6.1. Cài đặt dependencies

```bash
pip install numpy dd
```

### 6.2. Chạy benchmark

```bash
python run_all_test.py
```

### 6.3. Kết quả output

Sau khi chạy, kết quả được lưu tại thư mục `Benchmark_output/`:
- `result.csv`: Kết quả dạng CSV để phân tích
- `result.txt`: Báo cáo dạng text với bảng định dạng

---

## 7. Lời cảm ơn

Nhóm chúng em xin gửi lời cảm ơn chân thành đến **Thầy Mai Xuân Toàn** đã tận tình chỉ dẫn và hỗ trợ trong quá trình thực hiện bài tập này.

Cảm ơn Thầy đã dành thời gian đọc báo cáo Task 3 về phân tích và so sánh hiệu suất phương pháp BDD trong Reachability Analysis của chúng em

Mọi góp ý và nhận xét từ Thầy sẽ là nguồn động lực quý báu giúp nhóm hoàn thiện hơn trong các nhiệm vụ tiếp theo.

---

**Ngày hoàn thành**: 07/12/2025

**Tác Giả** : Hoàng Nam & Thế Lộc

**Link GitHub**: [https://github.com/namhcmutpd/MM_BP_BenchMark_result](https://github.com/namhcmutpd/MM_BP_BenchMark_result)
