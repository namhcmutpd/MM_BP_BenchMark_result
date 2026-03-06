# Đánh Giá Phân Rã Use Case – Quản Lý Bãi Đỗ (Smart Parking)

> **Người đánh giá:** AI Reviewer (chế độ khó tính)
> **Đối tượng chấm điểm:** Diagram *Quản lý bãi đỗ* — **phiên bản v2** (cập nhật theo feedback)
> **Thang điểm:** 10 (cộng điểm từng tiêu chí; không làm tròn có lợi cho sinh viên)

---

## 📋 Lịch Sử Phiên Bản

| Phiên bản | Thay đổi chính | Điểm |
|---|---|---|
| **v1** | Bản nộp đầu tiên | **4.4 / 10** |
| **v2** (hiện tại) | Đổi "Cập nhật tình trạng bãi đỗ" → "Giám sát chỗ trống"; xóa actor "System" | **4.7 / 10** (+0.3) |

---

## Quan Sát Diagram v2

Từ hình v2, diagram "Quản lý bãi đỗ" bao gồm:

**Actors:** Admin (trái) — *(actor "System" đã được xóa — cải thiện so với v1)*

**Use cases (bên trong system boundary):**
1. Thêm/Xóa bãi đỗ
2. Đóng/mở bãi đỗ
3. Cập nhật thông tin & sơ đồ
4. **Giám sát chỗ trống** *(v1 là "Cập nhật tình trạng bãi đỗ")*
5. Đồng bộ dữ liệu *(phía phải, bên ngoài hoặc trên biên system boundary)*

**Quan hệ:**
- Admin → tất cả 4 use case chính
- `<<include>>`: "Giám sát chỗ trống" → "Đồng bộ dữ liệu"

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

### Tiêu Chí 1 – Tính Đầy Đủ (Completeness) — **1.3 / 3.0** ❌ *(v1: 1.2)*

#### Thay đổi từ v1 → v2 ✓
- Đổi tên "Cập nhật tình trạng bãi đỗ" → **"Giám sát chỗ trống"**: tên mới chuẩn xác hơn về mặt nghiệp vụ. "Giám sát" (monitoring) thể hiện rõ hành động quan sát liên tục real-time, phù hợp với đặc tính của smart parking hơn "cập nhật". +0.1 điểm.

#### Những gì đã có ✓
Diagram bắt trúng 4 tác vụ cơ bản:
- Thêm / xóa bãi đỗ (quản lý vòng đời bãi)
- Đóng / mở bãi đỗ (quản lý trạng thái vận hành)
- Cập nhật thông tin & sơ đồ (quản lý metadata)
- Giám sát chỗ trống (real-time occupancy monitoring)

#### Những gì vẫn còn thiếu ✗

| Use case thiếu | Mức độ | Lý do bắt buộc phải có |
|---|---|---|
| **Tìm kiếm / xem thông tin bãi đỗ** | 🔴 Bắt buộc | Không có read operation là thiếu CRUD cơ bản nhất. |
| **Phân chia / quản lý khu vực đỗ (zone/slot)** | 🔴 Bắt buộc | Bãi đỗ smart parking có nhiều tầng, khu vực, loại xe — thiếu UC quản lý zone là thiếu nghiệp vụ cốt lõi. |
| **Đặt giá / phí đỗ xe** | 🟡 Quan trọng | Admin thiết lập bảng giá theo giờ, loại xe, ngày. |
| **Xem báo cáo / thống kê bãi đỗ** | 🟡 Quan trọng | Tỷ lệ lấp đầy, doanh thu, giờ cao điểm — nhu cầu quản lý thiết yếu. |
| **Xem lịch sử hoạt động bãi đỗ** | 🟠 Trung bình | Log audit trail cho vận hành và debug. |

> ⚠️ **Kết luận:** Diagram v2 vẫn chỉ bao phủ ~35-40% nghiệp vụ thực tế. Việc đổi tên 1 UC không bổ sung được nghiệp vụ còn thiếu.

---

### Tiêu Chí 2 – Quan Hệ `<<include>>` / `<<extend>>` — **1.0 / 2.5** ❌ *(v1: 1.0 — không đổi)*

#### Thay đổi từ v1 → v2
Không có thay đổi nào ở tiêu chí này. Điểm giữ nguyên.

#### Điểm tích cực ✓

Chiều mũi tên `<<include>>` **đúng**: từ "Giám sát chỗ trống" → "Đồng bộ dữ liệu".

```
✓ Đúng: [Giám sát chỗ trống] ──<<include>>──> [Đồng bộ dữ liệu]
```

#### Lỗi 1: Thiếu `<<include>>` từ các use case khác đến "Đồng bộ dữ liệu" — **Lỗi logic nghiêm trọng** *(chưa sửa)*

Nếu "Cập nhật tình trạng bãi đỗ" cần đồng bộ dữ liệu, thì TẤT CẢ các hành động thay đổi trạng thái bãi đỗ đều phải đồng bộ:

| Use case | Có cần đồng bộ không? | Diagram hiện tại |
|---|---|---|
| Thêm/Xóa bãi đỗ | ✅ Có — thêm bãi mới vào hệ thống phải sync | ❌ Không có `<<include>>` *(chưa sửa)* |
| Đóng/mở bãi đỗ | ✅ Có — trạng thái vận hành phải sync để driver app biết | ❌ Không có `<<include>>` *(chưa sửa)* |
| Cập nhật thông tin & sơ đồ | ✅ Có — thay đổi sơ đồ/thông tin phải phản ánh lên app | ❌ Không có `<<include>>` *(chưa sửa)* |
| Giám sát chỗ trống | ✅ Có | ✓ Có `<<include>>` |

**Hệ quả:** Diagram ngụ ý rằng chỉ "Cập nhật tình trạng" mới cần đồng bộ — điều này sai về mặt nghiệp vụ. Admin thêm một bãi đỗ mới mà không sync → driver app không biết bãi tồn tại.

#### Lỗi 2: Hoàn toàn vắng mặt của `<<extend>>` — **Thiếu hành vi điều kiện** *(chưa sửa)*

Trong nghiệp vụ quản lý bãi đỗ, có nhiều tình huống điều kiện (conditional behavior) cần mô hình hóa bằng `<<extend>>`:

| Tình huống | Extend từ đâu → vào đâu |
|---|---|
| Gửi thông báo đến driver khi bãi đầy hoặc mở lại | [Gửi thông báo] →`<<extend>>`→ [Giám sát chỗ trống] |
| Cảnh báo khi bãi đóng đột xuất | [Gửi cảnh báo khẩn] →`<<extend>>`→ [Đóng/mở bãi đỗ] |
| Yêu cầu xác nhận khi xóa bãi đỗ có đặt chỗ đang hoạt động | [Kiểm tra đặt chỗ active] →`<<extend>>`→ [Xóa bãi đỗ] |

Không có một `<<extend>>` nào → diagram mô hình hóa chức năng quá "lý tưởng", thiếu hẳn các luồng ngoại lệ và điều kiện.

#### Lỗi 3: "Đồng bộ dữ liệu" — Use case hay Sub-function? *(chưa sửa)*

"Đồng bộ dữ liệu" vẫn nằm trên/ngoài biên system boundary → **vẫn mơ hồ về bản chất**:
- Nếu là use case → cần nằm rõ ràng bên trong boundary.
- Nếu là tác vụ nội bộ → không nên là use case độc lập.

---

### Tiêu Chí 3 – Tính Đúng Đắn của Actor — **0.9 / 1.5** ⚠️ *(v1: 0.7 — cải thiện)*

#### Thay đổi từ v1 → v2 ✓ *(đã sửa theo feedback)*

Actor **"System"** đã được **xóa khỏi diagram** — đây là cải thiện quan trọng. Việc đặt tên actor là "System" là mơ hồ và sai về nguyên tắc (hệ thống không thể là actor của chính nó). +0.2 điểm.

#### Vấn đề còn lại ✗

Diagram v2 chỉ có một actor duy nhất là "Admin". Đối với một hệ thống smart parking đầy đủ, còn thiếu:

| Actor thiếu | Mức độ | Giải thích |
|---|---|---|
| **Người dùng / Driver** | 🟡 Quan trọng | Xem thông tin bãi, tìm kiếm chỗ trống — những UC bị thiếu ở Tiêu chí 1 đều cần actor này |
| **Hệ thống IoT / Sensor** | 🟡 Quan trọng | "Giám sát chỗ trống" thực tế được trigger bởi sensor, không phải Admin thủ công — cần actor thứ hai để mô hình hóa đúng |

---

### Tiêu Chí 4 – Mức Độ Phân Rã / Granularity — **0.5 / 1.5** ❌ *(v1: 0.5 — không đổi)*

#### Thay đổi từ v1 → v2
Không có thay đổi nào ở tiêu chí này. Điểm giữ nguyên.

#### Lỗi 1: Gộp cặp hành động đối lập — **vi phạm nghiêm trọng** *(chưa sửa)*

| Use case gộp | Tại sao cần tách |
|---|---|
| **"Thêm/Xóa bãi đỗ"** | "Thêm" yêu cầu nhập thông tin, validate tọa độ, kiểm tra trùng lặp. "Xóa" yêu cầu kiểm tra đặt chỗ đang hoạt động, xác nhận, cascade delete thiết bị IoT liên quan. Hai luồng hoàn toàn khác nhau. |
| **"Đóng/mở bãi đỗ"** | "Đóng" yêu cầu thông báo cho driver đang trong bãi, ngừng nhận đặt chỗ mới, ghi lý do. "Mở" yêu cầu khôi phục capacity, thông báo bãi available. Preconditions và postconditions khác nhau hoàn toàn. |

Cả hai trường hợp, sinh viên gộp 2 UC thành 1 chỉ vì chúng là "hành động ngược nhau" — đây là cách nghĩ **sai** trong UML Use Case modeling. Hai mục tiêu người dùng khác nhau = hai use case khác nhau.

#### Lỗi 2: "Cập nhật thông tin & sơ đồ" — quá mơ hồ *(chưa sửa)*

"Thông tin" và "sơ đồ" có thể là hai use case tách biệt với luồng khác nhau:
- **Cập nhật thông tin**: tên, địa chỉ, giờ hoạt động, sức chứa → form đơn giản
- **Cập nhật sơ đồ**: upload file sơ đồ tầng, định vị slot trên map → quy trình phức tạp hơn nhiều

Gộp hai nghiệp vụ này vào một use case làm mờ đi độ phức tạp thực sự.

#### Lỗi 3: "Giám sát chỗ trống" — Use case của Admin hay sự kiện hệ thống IoT?

*(v1 cũng có lỗi tương đương với "Cập nhật tình trạng bãi đỗ")*

- Tên mới "Giám sát chỗ trống" ngụ ý đây là **hành động thụ động (passive monitoring)** của hệ thống IoT, không phải hành động chủ động của Admin.
- Nếu Admin chủ động xem tình trạng chỗ trống → UC nên là "Xem tình trạng chỗ trống" (query) với Admin là initiator.
- Nếu hệ thống IoT tự cập nhật → cần thêm actor "IoT Sensor" làm initiator, không phải Admin.

---

### Tiêu Chí 5 – Ký Hiệu UML & Layout — **1.0 / 1.5** ⚠️ *(v1: 1.0 — không đổi)*

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
| "Đồng bộ dữ liệu" — vị trí trong diagram | ⚠️ Vẫn nằm sát biên phải system boundary — chưa rõ ràng là inside hay outside |
| Layout tổng thể | ✓ Sạch hơn v1 (không còn actor bên phải gây rối) |

---

## Tổng Hợp Điểm Số — v2

| # | Tiêu chí | Điểm tối đa | v1 | v2 | Delta |
|---|----------|-------------|----|----|-------|
| 1 | Tính đầy đủ (Completeness) | 3.0 | 1.2 | **1.3** | +0.1 |
| 2 | Quan hệ include/extend | 2.5 | 1.0 | **1.0** | = |
| 3 | Actor | 1.5 | 0.7 | **0.9** | +0.2 |
| 4 | Granularity | 1.5 | 0.5 | **0.5** | = |
| 5 | UML Notation & Layout | 1.5 | 1.0 | **1.0** | = |
| | **TỔNG** | **10.0** | **4.4** | **4.7** | **+0.3** |

> ### 🟠 Điểm v2: **4.7 / 10** *(tăng 0.3 điểm so với v1)*

---

## So Sánh Hai Diagram — Phiên Bản v2

| Tiêu chí | Quản lý bãi đỗ v2 | Quản lý thiết bị IoT v2 |
|---|---|---|
| Tính đầy đủ | 1.3 / 3.0 | *xem review IoT* |
| Quan hệ include/extend | 1.0 / 2.5 | *xem review IoT* |
| Actor | 0.9 / 1.5 | *xem review IoT* |
| Granularity | 0.5 / 1.5 | *xem review IoT* |
| UML Notation | 1.0 / 1.5 | *xem review IoT* |
| **Tổng** | **4.7 / 10** | **5.1 / 10** |

---

## Những Điểm Đáng Ghi Nhận

- ✅ Mũi tên `<<include>>` đúng chiều — duy trì từ v1.
- ✅ Ý tưởng đưa "Đồng bộ dữ liệu" vào như một use case dùng chung (shared UC) là đúng hướng.
- ✅ Xóa actor "System" mơ hồ — cải thiện đúng theo feedback.
- ✅ Đổi tên "Cập nhật tình trạng" → "Giám sát chỗ trống" — tên chuẩn hơn về nghiệp vụ.
- ✅ Tách riêng diagram "Quản lý bãi đỗ" và "Quản lý thiết bị IoT" là phân nhóm logic.

---

## Hướng Sửa Ưu Tiên Cao (v2 → v3)

Những lỗi **chưa sửa**, cần ưu tiên theo thứ tự:

1. **[NGHIÊM TRỌNG]** Tách "Thêm/Xóa bãi đỗ" thành hai UC riêng: "Thêm bãi đỗ mới" và "Xóa / Gỡ bãi đỗ".

2. **[NGHIÊM TRỌNG]** Tách "Đóng/mở bãi đỗ" thành hai UC riêng: "Đóng cửa bãi đỗ" và "Mở cửa / Kích hoạt bãi đỗ".

3. **[QUAN TRỌNG]** Thêm `<<include>>` từ "Thêm bãi đỗ", "Đóng/mở bãi đỗ", và "Cập nhật thông tin & sơ đồ" → "Đồng bộ dữ liệu". Hiện tại chỉ có 1/4 UC đồng bộ là không hợp lý.

4. **[QUAN TRỌNG]** Thêm ít nhất 2 use case còn thiếu: "Tìm kiếm / xem thông tin bãi đỗ" và "Quản lý khu vực / slot đỗ xe".

5. **[QUAN TRỌNG]** Thêm ít nhất một `<<extend>>` — ví dụ: [Gửi thông báo bãi đầy/mở lại] →`<<extend>>`→ [Giám sát chỗ trống].

6. **[TRUNG BÌNH]** Đặt "Đồng bộ dữ liệu" rõ ràng bên trong system boundary.

---

## Diagram Đề Xuất Cải Tiến (PlantUML)

Xem file [`UC_QuanLyBaiDo_Improved.puml`](./UC_QuanLyBaiDo_Improved.puml) trong cùng thư mục.

---

*Đánh giá v2 hoàn thành — điểm trung bình hai diagram v2: **(4.7 + 5.1) / 2 = 4.9 / 10***
