# Đánh Giá Phân Rã Use Case – Quản Lý Bãi Đỗ (Smart Parking)

> **Người đánh giá:** AI Reviewer (chế độ khó tính)
> **Đối tượng chấm điểm:** Diagram *Quản lý bãi đỗ* trong hình đã nộp
> **Thang điểm:** 10 (cộng điểm từng tiêu chí; không làm tròn có lợi cho sinh viên)

---

## Quan Sát Diagram Gốc

Từ hình đã nộp, diagram "Quản lý bãi đỗ" bao gồm:

**Actors:** Admin (trái) · System (phải)

**Use cases (bên trong system boundary):**
1. Thêm/Xóa bãi đỗ
2. Đóng/mở bãi đỗ
3. Cập nhật thông tin & sơ đồ
4. Cập nhật tình trạng bãi đỗ
5. Đồng bộ dữ liệu *(nằm phía phải, kết nối với System)*

**Quan hệ:**
- Admin → tất cả 4 use case chính
- `<<include>>`: "Cập nhật tình trạng bãi đỗ" → "Đồng bộ dữ liệu"
- System → "Đồng bộ dữ liệu"

---

## Tiêu Chí Chấm Điểm

| # | Tiêu chí | Điểm tối đa |
|---|----------|-------------|
| 1 | Tính đầy đủ của use case (Completeness) | 3.0 |
| 2 | Tính đúng đắn của quan hệ `<<include>>` / `<<extend>>` | 2.5 |
| 3 | Tính đúng đắn của Actor | 1.5 |
| 4 | Mức độ phân rã / Granularity | 1.5 |
| 5 | Ký hiệu UML (Notation & Layout) | 1.5 |
| **Tổng** | | **10.0** |

---

## Phân Tích Chi Tiết

---

### Tiêu Chí 1 – Tính Đầy Đủ (Completeness) — **1.2 / 3.0** ❌

#### Những gì đã có ✓
Diagram bắt trúng 4 tác vụ cơ bản mà Admin thực hiện trên bãi đỗ:
- Thêm / xóa bãi đỗ (quản lý vòng đời bãi)
- Đóng / mở bãi đỗ (quản lý trạng thái vận hành)
- Cập nhật thông tin & sơ đồ (quản lý metadata)
- Cập nhật tình trạng bãi đỗ (quản lý real-time occupancy)

#### Những gì bị thiếu ✗

| Use case thiếu | Mức độ quan trọng | Lý do bắt buộc phải có |
|---|---|---|
| **Tìm kiếm / xem thông tin bãi đỗ** | 🔴 Bắt buộc | Admin (và người dùng) cần đọc thông tin bãi trước khi chỉnh sửa. Không có read operation là thiếu CRUD cơ bản nhất. |
| **Phân chia / quản lý khu vực đỗ (zone/slot)** | 🔴 Bắt buộc | Bãi đỗ trong smart parking không phải đơn khối — có nhiều tầng, khu vực (A/B/C), loại xe (xe máy, ô tô, xe điện). Thiếu UC quản lý zone là thiếu nghiệp vụ cốt lõi. |
| **Đặt giá / phí đỗ xe** | 🟡 Quan trọng | Admin cần thiết lập bảng giá theo giờ, theo loại xe, theo ngày. Đây là nghiệp vụ tài chính thiết yếu. |
| **Xem báo cáo / thống kê bãi đỗ** | 🟡 Quan trọng | Admin cần biết tỷ lệ lấp đầy, doanh thu, các giờ cao điểm. Thiếu reporting là thiếu nhu cầu quản lý thực sự. |
| **Xem lịch sử hoạt động bãi đỗ** | 🟠 Trung bình | Log audit trail: khi nào bãi đóng, ai thay đổi thông tin, sự cố gì xảy ra. |
| **Quản lý phương tiện / vé đỗ** | 🟠 Trung bình | Check-in/check-out phương tiện là core flow của smart parking. Không hẳn thuộc UC "Quản lý bãi đỗ" nhưng cần có liên kết rõ ràng với UC khác. |

> ⚠️ **Kết luận:** Diagram chỉ bao phủ ~35% nghiệp vụ thực tế của chức năng "Quản lý bãi đỗ" trong một ứng dụng smart parking đủ dùng.

---

### Tiêu Chí 2 – Quan Hệ `<<include>>` / `<<extend>>` — **1.0 / 2.5** ❌

#### Điểm tích cực ✓

Chiều mũi tên `<<include>>` **đúng**: từ "Cập nhật tình trạng bãi đỗ" → "Đồng bộ dữ liệu".
Đây là điều bắt buộc và đã làm đúng theo chuẩn UML 2.x.

```
✓ Đúng: [Cập nhật tình trạng bãi đỗ] ──<<include>>──> [Đồng bộ dữ liệu]
```

#### Lỗi 1: Thiếu `<<include>>` từ các use case khác đến "Đồng bộ dữ liệu" — **Lỗi logic nghiêm trọng**

Nếu "Cập nhật tình trạng bãi đỗ" cần đồng bộ dữ liệu, thì TẤT CẢ các hành động thay đổi trạng thái bãi đỗ đều phải đồng bộ:

| Use case | Có cần đồng bộ không? | Diagram hiện tại |
|---|---|---|
| Thêm/Xóa bãi đỗ | ✅ Có — thêm bãi mới vào hệ thống phải sync | ❌ Không có `<<include>>` |
| Đóng/mở bãi đỗ | ✅ Có — trạng thái vận hành phải sync để driver app biết | ❌ Không có `<<include>>` |
| Cập nhật thông tin & sơ đồ | ✅ Có — thay đổi sơ đồ/thông tin phải phản ánh lên app | ❌ Không có `<<include>>` |
| Cập nhật tình trạng bãi đỗ | ✅ Có | ✓ Có `<<include>>` |

**Hệ quả:** Diagram ngụ ý rằng chỉ "Cập nhật tình trạng" mới cần đồng bộ — điều này sai về mặt nghiệp vụ. Admin thêm một bãi đỗ mới mà không sync → driver app không biết bãi tồn tại.

#### Lỗi 2: Hoàn toàn vắng mặt của `<<extend>>` — **Thiếu hành vi điều kiện**

Trong nghiệp vụ quản lý bãi đỗ, có nhiều tình huống điều kiện (conditional behavior) cần mô hình hóa bằng `<<extend>>`:

| Tình huống | Extend từ đâu → vào đâu |
|---|---|
| Gửi thông báo đến driver khi bãi đầy hoặc mở lại | [Gửi thông báo] →`<<extend>>`→ [Cập nhật tình trạng bãi đỗ] |
| Cảnh báo khi bãi đóng đột xuất | [Gửi cảnh báo khẩn] →`<<extend>>`→ [Đóng/mở bãi đỗ] |
| Yêu cầu xác nhận khi xóa bãi đỗ có đặt chỗ đang hoạt động | [Kiểm tra đặt chỗ active] →`<<extend>>`→ [Xóa bãi đỗ] |

Không có một `<<extend>>` nào → diagram mô hình hóa chức năng quá "lý tưởng", thiếu hẳn các luồng ngoại lệ và điều kiện.

#### Lỗi 3: "Đồng bộ dữ liệu" — Use case hay Sub-function?

"Đồng bộ dữ liệu" nằm trong system boundary, có cả Admin và System kết nối vào → **mơ hồ về bản chất**:
- Nếu là use case → Admin có thể kích hoạt đồng bộ thủ công → cần mô tả rõ hơn.
- Nếu là tác vụ nội bộ (system function) → không nên là use case độc lập, chỉ nên là sub-step của các UC khác qua `<<include>>`.

---

### Tiêu Chí 3 – Tính Đúng Đắn của Actor — **0.7 / 1.5** ⚠️

#### Vấn đề 1: Actor "System" quá chung chung (lỗi tương tự diagram IoT)

"System" tham gia vào "Đồng bộ dữ liệu" — nhưng "System" ở đây là gì?

| Câu hỏi | Cần trả lời |
|---|---|
| Hệ thống backend của smart parking? | Vậy nó KHÔNG phải actor — nó là chính hệ thống đang mô tả |
| Hệ thống bên ngoài (external DB, cloud service)? | Cần đặt tên rõ: "Cloud Database", "Central Platform", "Mobile App Backend" |
| Scheduled job / cron? | Thì không phải actor hướng người dùng, cần ghi chú |

> Việc đặt tên actor là "System" là **thiếu tư duy phân tích nghiệp vụ**. Ai là stakeholder thực sự tương tác với hệ thống?

#### Vấn đề 2: Thiếu actor "Người Dùng / Driver"

Mặc dù UC này tên là "Quản lý bãi đỗ" và tập trung vào Admin, nhưng một số UC (đặc biệt "Tìm kiếm thông tin bãi đỗ" mà đã bị bỏ sót ở Tiêu chí 1) đòi hỏi phải có actor "Driver/User" để mô hình hóa đầy đủ. Thiếu actor này phần nào giải thích tại sao nhiều use case bị bỏ sót.

---

### Tiêu Chí 4 – Mức Độ Phân Rã / Granularity — **0.5 / 1.5** ❌

#### Lỗi 1: Gộp cặp hành động đối lập — **vi phạm nghiêm trọng**

| Use case gộp | Tại sao cần tách |
|---|---|
| **"Thêm/Xóa bãi đỗ"** | "Thêm" yêu cầu nhập thông tin, validate tọa độ, kiểm tra trùng lặp. "Xóa" yêu cầu kiểm tra đặt chỗ đang hoạt động, xác nhận, cascade delete thiết bị IoT liên quan. Hai luồng hoàn toàn khác nhau. |
| **"Đóng/mở bãi đỗ"** | "Đóng" yêu cầu thông báo cho driver đang trong bãi, ngừng nhận đặt chỗ mới, ghi lý do. "Mở" yêu cầu khôi phục capacity, thông báo bãi available. Preconditions và postconditions khác nhau hoàn toàn. |

Cả hai trường hợp, sinh viên gộp 2 UC thành 1 chỉ vì chúng là "hành động ngược nhau" — đây là cách nghĩ **sai** trong UML Use Case modeling. Hai mục tiêu người dùng khác nhau = hai use case khác nhau.

#### Lỗi 2: "Cập nhật thông tin & sơ đồ" — quá mơ hồ

"Thông tin" và "sơ đồ" có thể là hai use case tách biệt với luồng khác nhau:
- **Cập nhật thông tin**: tên, địa chỉ, giờ hoạt động, sức chứa → form đơn giản
- **Cập nhật sơ đồ**: upload file sơ đồ tầng, định vị slot trên map → quy trình phức tạp hơn nhiều

Gộp hai nghiệp vụ này vào một use case làm mờ đi độ phức tạp thực sự.

#### Lỗi 3: Thiếu phân biệt use case chủ động vs. bị động

- "Cập nhật tình trạng bãi đỗ" — Admin tự làm hay hệ thống IoT tự cập nhật? Nếu IoT sensor tự cập nhật thì đây là system event, không phải user-initiated UC của Admin.

---

### Tiêu Chí 5 – Ký Hiệu UML & Layout — **1.0 / 1.5** ⚠️

| Điểm kiểm tra | Đánh giá |
|---|---|
| Hình ellipse cho use case | ✓ Đúng |
| Hình người que cho actor | ✓ Đúng |
| System boundary (hình chữ nhật) | ✓ Có và đúng |
| Tên use case bên trong boundary | ✓ Đúng |
| Đường `<<include>>` là nét đứt với mũi tên mở | ✓ Đúng |
| Hướng mũi tên `<<include>>` | ✓ Đúng (từ UC chính → UC được include) |
| Stereotype `<<include>>` có ghi nhãn | ✓ Đúng |
| Không có `<<extend>>` nào | ⚠️ Không sai về ký hiệu nhưng thiếu mô hình hóa hành vi điều kiện |
| "Đồng bộ dữ liệu" — vị trí trong diagram | ⚠️ Nằm bên phải system boundary, gần System actor — gây nhầm lẫn về việc nó có nằm trong boundary hay không |
| Layout tổng thể | ⚠️ Chấp nhận được — use case trái (Admin-driven) và đồng bộ phải (System) rõ ràng, nhưng thiếu visual alignment |

---

## Tổng Hợp Điểm Số

| # | Tiêu chí | Điểm tối đa | Điểm đạt |
|---|----------|-------------|----------|
| 1 | Tính đầy đủ (Completeness) | 3.0 | **1.2** |
| 2 | Quan hệ include/extend | 2.5 | **1.0** |
| 3 | Actor | 1.5 | **0.7** |
| 4 | Granularity | 1.5 | **0.5** |
| 5 | UML Notation & Layout | 1.5 | **1.0** |
| | **TỔNG** | **10.0** | **4.4 / 10** |

> ### 🔴 Điểm: **4.4 / 10**

---

## So Sánh Hai Diagram

| Tiêu chí | Quản lý bãi đỗ | Quản lý thiết bị IoT |
|---|---|---|
| Tính đầy đủ | 1.2 / 3.0 | 1.5 / 3.0 |
| Quan hệ include/extend | 1.0 / 2.5 | 0.8 / 2.5 |
| Actor | 0.7 / 1.5 | 0.8 / 1.5 |
| Granularity | 0.5 / 1.5 | 0.7 / 1.5 |
| UML Notation | 1.0 / 1.5 | 0.8 / 1.5 |
| **Tổng** | **4.4 / 10** | **4.6 / 10** |

> Cả hai diagram ở mức **dưới trung bình**. Diagram "Quản lý bãi đỗ" tốt hơn về UML notation (chiều mũi tên `<<include>>` đúng) nhưng kém hơn về granularity và completeness.

---

## Những Điểm Đáng Ghi Nhận

- ✅ Mũi tên `<<include>>` đúng chiều — tốt hơn diagram IoT.
- ✅ Ý tưởng đưa "Đồng bộ dữ liệu" vào như một use case dùng chung (shared UC) là đúng hướng.
- ✅ Xác định được các tác vụ CRUD cơ bản của Admin.
- ✅ Tách riêng diagram "Quản lý bãi đỗ" và "Quản lý thiết bị IoT" là phân nhóm logic.

---

## Hướng Sửa Ưu Tiên Cao

Theo thứ tự cần sửa ngay:

1. **[NGHIÊM TRỌNG]** Tách "Thêm/Xóa bãi đỗ" thành hai UC riêng: "Thêm bãi đỗ mới" và "Xóa / Gỡ bãi đỗ".

2. **[NGHIÊM TRỌNG]** Tách "Đóng/mở bãi đỗ" thành hai UC riêng: "Đóng cửa bãi đỗ" và "Mở cửa / Kích hoạt bãi đỗ".

3. **[QUAN TRỌNG]** Thêm `<<include>>` từ "Thêm bãi đỗ", "Đóng cửa bãi đỗ", "Mở cửa bãi đỗ", và "Cập nhật thông tin & sơ đồ" → "Đồng bộ dữ liệu". Hiện tại chỉ có 1/4 UC đồng bộ là không hợp lý.

4. **[QUAN TRỌNG]** Thêm ít nhất 2 use case còn thiếu: "Tìm kiếm / xem thông tin bãi đỗ" và "Quản lý khu vực / slot đỗ xe".

5. **[QUAN TRỌNG]** Thêm ít nhất một `<<extend>>` để mô hình hóa hành vi điều kiện — ví dụ: [Gửi thông báo bãi đầy/mở lại] →`<<extend>>`→ [Cập nhật tình trạng bãi đỗ].

6. **[TRUNG BÌNH]** Đổi tên actor "System" thành tên cụ thể hơn (VD: "Mobile App Backend" hoặc "Cloud Platform").

7. **[TRUNG BÌNH]** Làm rõ "Đồng bộ dữ liệu" nằm hoàn toàn bên trong system boundary và không có Admin trực tiếp trigger (hoặc nếu có, mô tả rõ luồng thủ công vs. tự động).

---

## Diagram Đề Xuất Cải Tiến (PlantUML)

Xem file [`UC_QuanLyBaiDo_Improved.puml`](./UC_QuanLyBaiDo_Improved.puml) trong cùng thư mục.

---

*Đánh giá hoàn thành — điểm trung bình của hai diagram: **(4.4 + 4.6) / 2 = 4.5 / 10***
