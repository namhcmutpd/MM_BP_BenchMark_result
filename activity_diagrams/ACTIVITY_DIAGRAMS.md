# Activity Diagrams – Ứng dụng theo dõi sức khỏe

Tài liệu này chứa **Activity Diagram** cho 4 usecase phân rã chính của ứng dụng theo dõi sức khỏe.

> **Ghi chú**: Các file `.puml` trong thư mục này có thể mở và render bằng [PlantUML](https://plantuml.com/), plugin PlantUML trong VS Code / IntelliJ, hoặc [PlantText online](https://www.planttext.com/).

---

## Danh sách Usecase

| # | Tên Usecase |
|---|-------------|
| 1 | Quản lí thiết bị |
| 2 | Đồng bộ dữ liệu |
| 3 | Live Tracking |
| 4 | Xử lí và cảnh báo rủi ro |

---

## 1 – Quản lí thiết bị

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[Mở ứng dụng và đăng nhập thành công]
    B --> C[Chọn mục 'Thiết bị']
    C --> D[Hiển thị danh sách thiết bị đã ghép nối]
    D --> E{Chọn hành động}

    E -- Thêm thiết bị mới --> F[Bật Bluetooth / WiFi trên điện thoại]
    F --> G[Quét các thiết bị gần đó]
    G --> H{Tìm thấy\nthiết bị?}
    H -- Không --> I[Hiển thị: 'Không tìm thấy thiết bị nào']
    I --> J[Người dùng kiểm tra nguồn điện và kết nối lại]
    J --> G
    H -- Có --> K[Hiển thị danh sách thiết bị tìm thấy]
    K --> L[Người dùng chọn thiết bị muốn ghép nối]
    L --> M[Thực hiện bắt tay kết nối - pairing]
    M --> N{Kết nối\nthành công?}
    N -- Không --> O[Hiển thị: 'Ghép nối thất bại']
    O --> P[Người dùng thử lại hoặc bỏ qua]
    N -- Có --> Q[Lưu thông tin thiết bị vào CSDL\nID, tên, loại, trạng thái]
    Q --> R[Hiển thị: 'Ghép nối thành công!']
    R --> S[Bắt đầu nhận dữ liệu từ thiết bị mới]

    E -- Xem chi tiết --> T[Hiển thị thông tin thiết bị\ntên, loại, firmware, mức pin, lần đồng bộ cuối]

    E -- Đổi tên --> U[Người dùng nhập tên mới]
    U --> V[Cập nhật tên thiết bị trong CSDL]
    V --> W[Hiển thị tên mới trong danh sách]

    E -- Xoá thiết bị --> X[Hiển thị hộp thoại xác nhận 'Bạn có chắc muốn xoá?']
    X --> Y{Xác nhận\nxoá?}
    Y -- Không --> Z[Huỷ thao tác]
    Y -- Có --> AA[Huỷ kết nối Bluetooth/WiFi với thiết bị]
    AA --> AB[Xoá thiết bị khỏi CSDL]
    AB --> AC[Xoá toàn bộ dữ liệu liên quan]
    AC --> AD[Hiển thị: 'Đã xoá thiết bị thành công']

    S --> AE([Kết thúc])
    T --> AE
    W --> AE
    Z --> AE
    AD --> AE
    P --> AE
```

---

## 2 – Đồng bộ dữ liệu

```mermaid
flowchart TD
    A([Bắt đầu]) --> B{Nguồn kích hoạt}
    B -- Thủ công --> C[Người dùng nhấn 'Đồng bộ ngay']
    B -- Tự động / thiết bị vừa kết nối --> C

    C --> D{Có kết nối\nInternet?}
    D -- Không --> E[Hiển thị: 'Không có kết nối mạng.\nDữ liệu sẽ đồng bộ khi có mạng']
    E --> F[Lưu yêu cầu vào hàng chờ - queue]
    F --> G([Dừng - chờ kết nối])

    D -- Có --> H[Kiểm tra trạng thái kết nối với các thiết bị đã ghép nối]

    H --> I[Đồng bộ từ thiết bị đeo → App]
    I --> J{Thiết bị đang\nkết nối?}
    J -- Không --> K[Ghi log: thiết bị offline]
    J -- Có --> L[Gửi lệnh yêu cầu truyền dữ liệu]
    L --> M[Nhận dữ liệu thô từ thiết bị\nnhịp tim, bước chân, SpO2, huyết áp, giấc ngủ]
    M --> N{Dữ liệu\nhợp lệ?}
    N -- Không --> O[Ghi log lỗi - yêu cầu thiết bị gửi lại]
    N -- Có --> P[Giải mã và chuẩn hoá dữ liệu thô]
    P --> Q[Lưu vào CSDL cục bộ]

    H --> R[Đồng bộ App → Máy chủ đám mây]
    R --> S[Lấy tất cả dữ liệu mới chưa đồng bộ lên server]
    S --> T{Có dữ liệu\ncần đẩy lên?}
    T -- Không --> U[Bỏ qua bước này]
    T -- Có --> V[Nén và mã hoá dữ liệu]
    V --> W[Gửi payload lên API máy chủ]
    W --> X{Server nhận\nthành công?}
    X -- Có --> Y[Cập nhật timestamp đồng bộ cuối thành công]
    X -- Không --> Z[Thử lại tối đa 3 lần với back-off delay]
    Z --> AA{Thành công\nsau retry?}
    AA -- Có --> Y
    AA -- Không --> AB[Lưu vào hàng chờ - hiển thị cảnh báo]

    Q --> AC[Kiểm tra dữ liệu mới từ server để kéo về]
    K --> AC
    U --> AC
    Y --> AC
    AB --> AC

    AC --> AD{Có dữ liệu mới\ntừ server?}
    AD -- Có --> AE[Tải dữ liệu mới về và cập nhật CSDL cục bộ]
    AE --> AF[Làm mới giao diện ứng dụng]
    AD -- Không --> AF

    AF --> AG[Ghi lại thời gian đồng bộ thành công]
    AG --> AH[Cập nhật trạng thái 'Đồng bộ lúc hh:mm' trên màn hình chính]
    AH --> AI[Người dùng nhận thông báo 'Đồng bộ hoàn tất']
    AI --> AJ([Kết thúc])
```

---

## 3 – Live Tracking

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[Mở ứng dụng và đăng nhập]
    B --> C[Chọn mục 'Live Tracking']
    C --> D{Thiết bị đang\nkết nối?}
    D -- Không --> E[Hiển thị cảnh báo 'Không tìm thấy thiết bị']
    E --> F[Người dùng kiểm tra thiết bị và thử lại]
    F --> D
    D -- Có --> G[Khởi tạo phiên Live Tracking]
    G --> H[Thiết bị bắt đầu thu thập dữ liệu liên tục\nmỗi 1–5 giây tuỳ cảm biến]

    H --> I[Nhận gói dữ liệu từ thiết bị qua BLE/WiFi]
    I --> J[Giải mã và xác thực gói dữ liệu]
    J --> K1[Cập nhật nhịp tim\nthời gian thực]
    J --> K2[Cập nhật SpO2]
    J --> K3[Cập nhật nhịp thở]
    J --> K4[Cập nhật vị trí GPS\nvà quãng đường]
    J --> K5[Cập nhật biểu đồ rolling chart]
    K1 & K2 & K3 & K4 & K5 --> L[Lưu snapshot vào buffer]
    L --> M{Phát hiện\nbất thường?}
    M -- Không --> N{Người dùng\nnhấn 'Dừng'?}
    M -- Có --> O[Kích hoạt cảnh báo\nđèn đỏ + âm thanh + rung]
    O --> P[Hiển thị popup cảnh báo và lời khuyên]
    P --> Q{Người dùng\nxác nhận đã xem?}
    Q -- Có --> R[Ghi nhận cảnh báo đã xác nhận]
    Q -- Không phản hồi trong 30s --> S[Gửi thông báo khẩn đến liên hệ khẩn cấp]
    R --> N
    S --> N

    N -- Không --> I
    N -- Có --> T[Dừng nhận dữ liệu từ thiết bị]
    T --> U[Tổng hợp kết quả phiên\nthời lượng, nhịp tim TB/Max/Min,\nSpO2 TB, quãng đường, calories]
    U --> V[Lưu kết quả phiên vào CSDL]
    V --> W[Đẩy dữ liệu phiên lên máy chủ]
    W --> X[Hiển thị màn hình Tổng kết phiên]
    X --> Y[Người dùng xem kết quả\nvà tuỳ chọn thêm ghi chú / chia sẻ]
    Y --> Z([Kết thúc])
```

---

## 4 – Xử lí và cảnh báo rủi ro

```mermaid
flowchart TD
    A([Bắt đầu - kích hoạt khi có dữ liệu mới]) --> B[Nhận dữ liệu sinh trắc học mới\nnhịp tim, huyết áp, SpO2, đường huyết, nhiệt độ]
    B --> C[Xác định loại dữ liệu và profile người dùng\ntuổi, giới tính, bệnh nền]
    C --> D[Truy xuất bộ quy tắc cảnh báo - rule engine\ncho người dùng này]

    D --> E[Phân tích ngưỡng tức thời]
    E --> F{So sánh với ngưỡng\nbình thường - WHO}
    F -- Vượt ngưỡng nguy hiểm cấp cao --> G[Phân loại: RỦI RO CAO - Critical]
    F -- Vượt ngưỡng cảnh báo --> H[Phân loại: CẢNH BÁO - Warning]
    F -- Bình thường --> I[Phân loại: BÌNH THƯỜNG]

    D --> J[Phân tích xu hướng]
    J --> K[Truy xuất lịch sử 24 giờ qua của chỉ số này]
    K --> L[Chạy thuật toán phát hiện xu hướng bất thường\ntăng/giảm liên tục, bất ổn định]
    L --> M{Phát hiện xu hướng\nbất thường?}
    M -- Có --> N[Đánh dấu cờ: TREND ALERT]
    M -- Không --> O[Không có cảnh báo xu hướng]

    G --> P[Tổng hợp kết quả phân tích ngưỡng + xu hướng]
    H --> P
    I --> P
    N --> P
    O --> P

    P --> Q{Phân loại\nkết quả}
    Q -- Critical --> R[Tạo bản ghi cảnh báo khẩn cấp trong CSDL]
    R --> S[Gửi push notification ngay lập tức\nđộ ưu tiên cao - vượt qua chế độ im lặng]
    S --> T[Người dùng nhận cảnh báo\nvới hướng dẫn sơ cứu]
    T --> U{Không phản hồi\ntrong 2 phút?}
    U -- Có --> V[Gửi SMS / cuộc gọi đến liên hệ khẩn cấp]
    V --> W[Gửi thông báo đến bác sĩ phụ trách - nếu có]
    U -- Đã phản hồi --> X[Ghi nhận người dùng đã xác nhận cảnh báo]

    Q -- Warning hoặc TREND ALERT --> Y[Tạo bản ghi cảnh báo thường trong CSDL]
    Y --> Z[Gửi push notification thông thường\nvà hiển thị biểu tượng cảnh báo trên Dashboard]
    Z --> AA[Người dùng xem thông báo\nvà lời khuyên y tế cơ bản]
    AA --> AB[Người dùng nhấn 'Đã hiểu']
    AB --> AC[Đánh dấu cảnh báo đã được đọc]

    Q -- Bình thường --> AD[Không tạo cảnh báo]
    AD --> AE[Cập nhật Dashboard với chỉ số màu xanh ✓]

    W --> AF[Lưu toàn bộ kết quả phân tích vào log sự kiện]
    X --> AF
    AC --> AF
    AE --> AF

    AF --> AG{Cần đề xuất\ngặp bác sĩ?\ndựa trên tần suất\ncảnh báo 7 ngày qua}
    AG -- Có --> AH[Người dùng nhận gợi ý đặt lịch hẹn bác sĩ]
    AG -- Không --> AI([Kết thúc])
    AH --> AI
```

---

*Tài liệu: Activity Diagrams – Ứng dụng theo dõi sức khỏe*
