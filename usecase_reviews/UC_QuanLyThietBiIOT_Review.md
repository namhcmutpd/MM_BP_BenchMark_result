# Đánh Giá Phân Rã Use Case – Quản Lý Thiết Bị IoT (Smart Parking)

> **Người đánh giá:** AI Reviewer (chế độ khó tính)
> **Đối tượng chấm điểm:** Hai diagram trong hình được nộp — *Quản lý bãi đỗ* và *Quản lý thiết bị IOT*
> **Thang điểm:** 10 (cộng điểm từng tiêu chí; không làm tròn có lợi cho sinh viên)

---

## Tiêu Chí Chấm Điểm

| # | Tiêu chí | Điểm tối đa |
|---|----------|-------------|
| 1 | Tính đầy đủ của use case (completeness) | 3.0 |
| 2 | Tính đúng đắn của quan hệ `<<include>>` / `<<extend>>` | 2.5 |
| 3 | Tính đúng đắn của Actor | 1.5 |
| 4 | Mức độ phân rã / granularity | 1.5 |
| 5 | Ký hiệu UML (notation & layout) | 1.5 |
| **Tổng** | | **10.0** |

---

## Phân Tích Chi Tiết

---

### Tiêu Chí 1 – Tính Đầy Đủ (Completeness) — **1.5 / 3.0** ❌

#### Những gì đã có ✓
Diagram liệt kê được 4 use case cơ bản mang tính CRUD:
- Thêm/Xóa thiết bị
- Kích hoạt/vô hiệu hóa thiết bị
- Cập nhật trạng thái thiết bị
- Kiểm tra tình trạng kết nối

#### Những gì bị thiếu ✗

| Use case thiếu | Lý do bắt buộc phải có trong Smart Parking IoT |
|---|---|
| **Cấu hình thiết bị** (Configure device) | Mỗi cảm biến/camera cần được gán vào đúng vị trí đỗ xe, thiết lập tham số ngưỡng (threshold), tần suất gửi tín hiệu. Thiếu cái này, thiết bị thêm vào xong không biết làm gì. |
| **Gán thiết bị vào vị trí đỗ** (Assign to slot) | Quan hệ 1-1 hoặc 1-nhiều giữa thiết bị IoT và ô đỗ xe là nghiệp vụ cốt lõi của smart parking. |
| **Xem nhật ký / lịch sử thiết bị** (View device logs) | Admin cần biết thiết bị đã hoạt động như thế nào, khi nào mất kết nối, để debug và audit. |
| **Cập nhật firmware / phần mềm thiết bị** (Update firmware) | Thiết bị IoT trong thực tế cần OTA update. Đây là use case quan trọng trong quản lý vòng đời thiết bị. |
| **Xem báo cáo tình trạng thiết bị** (Device health report) | Admin cần dashboard tổng hợp, không chỉ kiểm tra từng thiết bị rời lẻ. |

> ⚠️ **5 use case quan trọng bị bỏ sót** → Diagram mới chỉ đạt ~44% yêu cầu nghiệp vụ thực tế.

---

### Tiêu Chí 2 – Quan Hệ `<<include>>` / `<<extend>>` — **0.8 / 2.5** ❌

#### Lỗi 1: Hướng mũi tên `<<extend>>` bị **ngược** (nghiêm trọng)

Trong sơ đồ, mũi tên `<<extend>>` chạy từ **"Kiểm tra tình trạng kết nối" → "Thông báo lỗi"**.

**Theo chuẩn UML 2.x:**
> Mũi tên `<<extend>>` PHẢI chỉ từ **use case mở rộng (extension)** → **use case cơ sở (base)**.
> Tức là: **"Thông báo lỗi" → "Kiểm tra tình trạng kết nối"**

```
❌ Sai:   [Kiểm tra tình trạng kết nối] ──<<extend>>──> [Thông báo lỗi]
✓ Đúng:  [Thông báo lỗi] ──<<extend>>──> [Kiểm tra tình trạng kết nối]
```

Đây là lỗi cơ bản về ký hiệu UML, không phải lỗi nhỏ.

#### Lỗi 2: "Thông báo lỗi" chỉ liên kết với 1 use case — **quá hẹp**

"Thông báo lỗi" là hành vi mở rộng (conditional behavior). Trên thực tế nó có thể được kích hoạt từ nhiều use case:
- Kích hoạt/vô hiệu hóa thiết bị (thiết bị không phản hồi lệnh)
- Cập nhật trạng thái thiết bị (lỗi timeout)
- Cập nhật firmware (lỗi truyền tải)

Chỉ nối "Thông báo lỗi" vào một use case duy nhất là **không phản ánh đúng nghiệp vụ**.

#### Lỗi 3: Thiếu `<<include>>` cần thiết

`"Cập nhật trạng thái thiết bị"` LUÔN phải gọi `"Kiểm tra tình trạng kết nối"` trước khi cập nhật → đây là quan hệ `<<include>>` bắt buộc nhưng hoàn toàn vắng mặt.

```
✓ Nên có: [Cập nhật trạng thái thiết bị] ──<<include>>──> [Kiểm tra tình trạng kết nối]
```

#### Vấn đề trong diagram "Quản lý bãi đỗ" (để tham khảo chéo)

Chỉ "Cập nhật tình trạng bãi đỗ" có `<<include>>` "Đồng bộ dữ liệu", nhưng "Thêm/Xóa bãi đỗ" và "Cập nhật thông tin & sơ đồ" khi thực hiện cũng **phải** đồng bộ dữ liệu — sự thiếu nhất quán này cho thấy thiếu phân tích nghiệp vụ kỹ.

---

### Tiêu Chí 3 – Tính Đúng Đắn của Actor — **0.8 / 1.5** ⚠️

#### Vấn đề với actor "System"

Trong UML Use Case Diagram:
- **System boundary** (hình chữ nhật bao quanh) đại diện cho hệ thống đang phát triển.
- **Actor** là thực thể **bên ngoài** tương tác với hệ thống.

Đặt **"System"** làm một actor bên phải là **mơ hồ và có thể gây nhầm lẫn**:

| Câu hỏi | Trả lời cần có |
|---|---|
| "System" là hệ thống nào? | Phải chỉ rõ: là hệ thống IoT Gateway, hệ thống Monitoring backend, hay chính ứng dụng? |
| Nếu là hệ thống bên ngoài (external system) | Đặt tên cụ thể hơn: "IoT Gateway", "Cloud Platform", "Monitoring Service" |
| Nếu là hành vi nội bộ của ứng dụng | Không nên là actor; nên là use case hoặc sub-system |

**Điểm tích cực:** Ít nhất đã nhận ra cần có actor phía "System" để thể hiện tương tác tự động — ý đồ là đúng, nhưng tên gọi quá chung chung.

---

### Tiêu Chí 4 – Mức Độ Phân Rã / Granularity — **0.7 / 1.5** ⚠️

#### Vấn đề: Gộp chung hai hành động đối lập vào một use case

| Use case trong diagram | Vấn đề |
|---|---|
| **"Thêm/Xóa thiết bị"** | "Thêm" và "Xóa" là hai hành động có luồng nghiệp vụ, precondition, postcondition hoàn toàn khác nhau. Gộp chung vi phạm nguyên tắc Single Responsibility cho use case. |
| **"Kích hoạt/vô hiệu hóa thiết bị"** | Tương tự — hai hành động với điều kiện khác nhau, nên tách hoặc dùng `<<extend>>` để mô hình hóa quan hệ. |

**Chuẩn mực:** Mỗi use case nên mô tả **một mục tiêu người dùng** (user goal) hoàn chỉnh. "Add OR Remove" không phải một mục tiêu.

#### Vấn đề: Thiếu phân biệt use case theo mức độ

Các use case hiện tại đang trộn lẫn hai level:
- **Business-level**: Thêm/Xóa thiết bị (hành động của Admin)
- **System-level**: Kiểm tra tình trạng kết nối (thường là tác vụ nền tự động)

Điều này làm cho diagram khó đọc và khó verify với stakeholders.

---

### Tiêu Chí 5 – Ký Hiệu UML & Layout — **0.8 / 1.5** ⚠️

| Điểm kiểm tra | Đánh giá |
|---|---|
| Hình ellipse cho use case | ✓ Đúng |
| Hình người que cho actor | ✓ Đúng |
| System boundary (hình chữ nhật) | ✓ Có, đúng |
| Tên use case bên trong boundary | ✓ Đúng |
| Đường `<<extend>>` là nét đứt | ✓ Có vẻ đúng (khó nhìn rõ) |
| Hướng mũi tên `<<extend>>` | ❌ Ngược chiều (lỗi nghiêm trọng, xem Tiêu chí 2) |
| Label stereotype `<<extend>>` nằm gần đường | ⚠️ Đặt ở giữa - chấp nhận được nhưng vị trí chưa rõ |
| Không có extension point (extension point note) | ❌ Chuẩn UML 2.x yêu cầu khai báo extension point trên use case cơ sở khi dùng `<<extend>>` |
| Layout tổng thể | ⚠️ Chấp nhận được nhưng dày đặc, khó theo dõi mũi tên |

---

## Tổng Hợp Điểm Số

| # | Tiêu chí | Điểm tối đa | Điểm đạt |
|---|----------|-------------|----------|
| 1 | Tính đầy đủ (Completeness) | 3.0 | **1.5** |
| 2 | Quan hệ include/extend | 2.5 | **0.8** |
| 3 | Actor | 1.5 | **0.8** |
| 4 | Granularity | 1.5 | **0.7** |
| 5 | UML Notation & Layout | 1.5 | **0.8** |
| | **TỔNG** | **10.0** | **4.6 / 10** |

> ### 🔴 Điểm: **4.6 / 10**

---

## Những Điểm Đáng Ghi Nhận

- ✅ Đã biết sử dụng cả `<<include>>` và `<<extend>>` — thể hiện hiểu được sự tồn tại của hai loại quan hệ này.
- ✅ Tách thành 2 diagram riêng (Quản lý bãi đỗ / Quản lý thiết bị IoT) — phân nhóm use case hợp lý.
- ✅ Xác định được Admin là actor chính — đúng.
- ✅ Có ý tưởng đưa "Thông báo lỗi" vào như hành vi điều kiện — ý tưởng đúng, chỉ sai chiều mũi tên.

---

## Hướng Sửa Ưu Tiên Cao

Theo thứ tự cần sửa ngay:

1. **[NGHIÊM TRỌNG]** Đảo chiều mũi tên `<<extend>>`:
   `[Thông báo lỗi] ──<<extend>>──> [Kiểm tra tình trạng kết nối]`

2. **[QUAN TRỌNG]** Tách "Thêm/Xóa thiết bị" thành hai use case riêng biệt.

3. **[QUAN TRỌNG]** Thêm `<<include>>` từ "Cập nhật trạng thái thiết bị" → "Kiểm tra tình trạng kết nối".

4. **[QUAN TRỌNG]** Thêm use case còn thiếu: Cấu hình thiết bị, Gán vị trí đỗ, Xem nhật ký thiết bị.

5. **[TRUNG BÌNH]** Đổi tên actor "System" thành tên cụ thể hơn (VD: "IoT Gateway" hoặc "Monitoring Service").

6. **[TRUNG BÌNH]** Thêm extension point vào use case "Kiểm tra tình trạng kết nối" theo chuẩn UML 2.x.

---

## Diagram Đề Xuất Cải Tiến (PlantUML)

Xem file [`UC_QuanLyThietBiIOT_Improved.puml`](./UC_QuanLyThietBiIOT_Improved.puml) trong cùng thư mục.

---

*Đánh giá hoàn thành — hãy sửa các lỗi theo thứ tự ưu tiên trước khi nộp lại.*
