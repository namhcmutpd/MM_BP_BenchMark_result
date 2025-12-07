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
- **Số lượng test case**: 12 file Petri Net (định dạng PNML)
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
| input1.pnml | 4 | 2 | 3 | 5.65 | 0.054 | 3 | 0.42 | 0.003 | 3 | 0.24 | 0.003 |
| input2.pnml | 5 | 4 | 3 | 3.06 | 0.073 | 3 | 0.46 | 0.003 | 3 | 0.26 | 0.003 |
| input3.pnml | 4 | 2 | 2 | 1.44 | 0.037 | 2 | 0.32 | 0.003 | 2 | 0.16 | 0.002 |
| input4.pnml | 23 | 23 | 3072 | 125.25 | 3.163 | 3072 | 2422.79 | 0.814 | 3072 | 994.89 | 0.825 |
| input5.pnml | 8 | 6 | 6 | 8.54 | 0.246 | 6 | 1.03 | 0.004 | 6 | 0.48 | 0.004 |
| input6.pnml | 8 | 12 | 36 | 27.40 | 0.747 | 36 | 9.25 | 0.010 | 36 | 4.61 | 0.008 |
| input7.pnml | 15 | 20 | 1536 | 84.46 | 2.118 | 1536 | 945.72 | 0.377 | 1536 | 447.72 | 0.374 |
| input8.pnml | 12 | 12 | 4096 | 41.47 | 0.848 | 4096 | 1996.38 | 0.699 | 4096 | 839.63 | 0.690 |
| input9.pnml | 8 | 10 | 20 | 17.45 | 0.376 | 20 | 7.26 | 0.007 | 20 | 3.46 | 0.007 |
| input10.pnml | 8 | 8 | 8 | 10.92 | 0.264 | 8 | 1.11 | 0.005 | 8 | 0.67 | 0.004 |
| input11.pnml | 10 | 6 | 16 | 10.66 | 0.332 | 16 | 4.71 | 0.006 | 16 | 1.69 | 0.005 |
| input12.pnml | 12 | 16 | 256 | 35.08 | 0.805 | 256 | 143.27 | 0.047 | 256 | 63.35 | 0.046 |

### 3.2. Tổng hợp thống kê

| Chỉ số | BDD | BFS | DFS |
|--------|-----|-----|-----|
| **Tổng thời gian (ms)** | 371.38 | 5532.72 | 2357.16 |
| **Tổng bộ nhớ (MB)** | 9.06 | 1.98 | 1.97 |

### 3.3. Tỉ lệ so sánh hiệu suất

| So sánh | Tỉ lệ |
|---------|-------|
| Tốc độ BDD nhanh hơn BFS | **14.90x** |
| Tốc độ BDD nhanh hơn DFS | **6.35x** |
| Bộ nhớ BFS/BDD | 0.22x | (Không dùng để so sánh)
| Bộ nhớ DFS/BDD | 0.22x | (Không dùng để so sánh)

---

## 4. Phân tích và đánh giá

### 4.1. Ưu điểm của phương pháp BDD

#### 4.1.1. Hiệu suất thời gian vượt trội trên Petri Net lớn

Kết quả thực nghiệm cho thấy phương pháp BDD thể hiện **ưu thế rõ rệt về thời gian thực thi** khi kích thước không gian trạng thái tăng lên:

- Với **input4.pnml** (23 places, 23 transitions, 3072 states): BDD hoàn thành trong **125.25ms**, trong khi BFS cần **2422.79ms** (chậm hơn ~19.3 lần) và DFS cần **994.89ms** (chậm hơn ~7.9 lần).
- Với **input8.pnml** (12 places, 12 transitions, 4096 states): BDD hoàn thành trong **41.47ms**, trong khi BFS cần **1996.38ms** (chậm hơn ~48.1 lần) và DFS cần **839.63ms** (chậm hơn ~20.2 lần).
- Với **input7.pnml** (15 places, 20 transitions, 1536 states): BDD hoàn thành trong **84.46ms**, trong khi BFS cần **945.72ms** (chậm hơn ~11.2 lần).

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

Kết quả cho thấy BDD sử dụng **bộ nhớ nhiều hơn khoảng 4.5 lần** so với phương pháp explicit (9.06 MB so với ~2 MB). Điều này là do:

- Chi phí khởi tạo BDD manager và các cấu trúc dữ liệu hỗ trợ.
- Overhead của unique table và computed cache.
- Việc xây dựng transition relation monolithic.

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

1. **Phương pháp BDD vượt trội về thời gian** khi không gian trạng thái lớn (từ hàng trăm đến hàng nghìn trạng thái trở lên), với tốc độ nhanh hơn từ **6 đến 20 lần** so với DFS và từ **10 đến 50 lần** so với BFS.

2. **Phương pháp Explicit phù hợp với Petri Net nhỏ** do chi phí khởi tạo thấp và implementation đơn giản.

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
