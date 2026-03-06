# Activity Diagrams - Ứng dụng theo dõi sức khỏe

Tài liệu này chứa **Activity Diagram** cho tất cả các **Usecase phân rã** trong ứng dụng theo dõi sức khỏe.

---

## Danh sách Usecase

| Mã | Tên Usecase |
|----|-------------|
| UC01 | Đăng ký tài khoản |
| UC02 | Đăng nhập hệ thống |
| UC03 | Quên mật khẩu |
| UC04 | Cập nhật thông tin cá nhân |
| UC05 | Ghi nhận chỉ số sức khỏe |
| UC06 | Theo dõi hoạt động thể chất |
| UC07 | Đặt mục tiêu sức khỏe |
| UC08 | Xem lịch sử sức khỏe |
| UC09 | Xem báo cáo thống kê |
| UC10 | Nhận thông báo nhắc nhở |
| UC11 | Quản lý lịch uống thuốc |
| UC12 | Chia sẻ dữ liệu với bác sĩ |

> **Lưu ý**: Các file `.puml` trong thư mục này có thể mở bằng [PlantUML](https://plantuml.com/) hoặc plugin PlantUML trong VS Code / IntelliJ để xem/chỉnh sửa diagram.

---

## UC01 – Đăng ký tài khoản

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[Mở ứng dụng]
    B --> C[Chọn 'Đăng ký']
    C --> D[Nhập họ tên, email, mật khẩu\nvà thông tin cơ bản]
    D --> E{Dữ liệu\nhợp lệ?}
    E -- Không --> F[Hiển thị thông báo lỗi]
    F --> D
    E -- Có --> G{Email đã\nđăng ký?}
    G -- Có --> H[Hiển thị: 'Email đã được sử dụng']
    H --> D
    G -- Không --> I[Tạo tài khoản mới trong CSDL]
    I --> J[Gửi email xác thực]
    J --> K[Người dùng mở email\nvà nhấn liên kết xác thực]
    K --> L{Token\nhợp lệ?}
    L -- Không --> M[Hiển thị: 'Liên kết hết hạn']
    M --> N[Cho phép gửi lại email]
    N --> J
    L -- Có --> O[Kích hoạt tài khoản]
    O --> P[Chuyển về màn hình đăng nhập]
    P --> Q([Kết thúc])
```

---

## UC02 – Đăng nhập hệ thống

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[Mở ứng dụng]
    B --> C[Nhập email và mật khẩu]
    C --> D[Nhấn 'Đăng nhập']
    D --> E{Định dạng\nhợp lệ?}
    E -- Không --> F[Hiển thị lỗi định dạng]
    F --> C
    E -- Có --> G{Tài khoản\ntồn tại?}
    G -- Không --> H[Hiển thị: 'Email không tồn tại']
    H --> C
    G -- Có --> I{Mật khẩu\nđúng?}
    I -- Không --> J[Tăng bộ đếm thất bại]
    J --> K{Vượt quá\n5 lần?}
    K -- Có --> L[Khoá tài khoản 15 phút]
    L --> M[Hiển thị thông báo khoá]
    K -- Không --> N[Hiển thị: 'Sai mật khẩu']
    M --> C
    N --> C
    I -- Có --> O[Tạo phiên đăng nhập - token]
    O --> P[Chuyển đến Dashboard sức khỏe]
    P --> Q([Kết thúc])
```

---

## UC03 – Quên mật khẩu

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[Nhấn 'Quên mật khẩu?']
    B --> C[Nhập địa chỉ email đã đăng ký]
    C --> D[Nhấn 'Gửi yêu cầu đặt lại']
    D --> E{Email\ntồn tại?}
    E -- Không --> F[Hiển thị: 'Email không tồn tại']
    F --> C
    E -- Có --> G[Tạo token đặt lại mật khẩu\n - thời hạn 30 phút]
    G --> H[Gửi email chứa liên kết đặt lại]
    H --> I[Người dùng nhấn liên kết\ntrong email]
    I --> J{Token hợp lệ\nvà chưa hết hạn?}
    J -- Không --> K[Hiển thị: 'Liên kết đã hết hạn']
    K --> L[Gửi lại yêu cầu]
    L --> G
    J -- Có --> M[Hiển thị form nhập mật khẩu mới]
    M --> N[Người dùng nhập\nmật khẩu mới và xác nhận]
    N --> O{Mật khẩu mới\nhợp lệ?}
    O -- Không --> P[Hiển thị yêu cầu mật khẩu]
    P --> N
    O -- Có --> Q[Cập nhật mật khẩu mới vào CSDL]
    Q --> R[Vô hiệu hoá tất cả token cũ]
    R --> S[Chuyển về màn hình đăng nhập]
    S --> T([Kết thúc])
```

---

## UC04 – Cập nhật thông tin cá nhân

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[Đăng nhập thành công]
    B --> C[Chọn mục 'Hồ sơ cá nhân']
    C --> D[Hệ thống hiển thị thông tin hiện tại]
    D --> E[Nhấn nút 'Chỉnh sửa']
    E --> F[Sửa đổi thông tin\nhọ tên, ngày sinh, giới tính,\nchiều cao, cân nặng, ảnh đại diện]
    F --> G[Nhấn 'Lưu']
    G --> H{Dữ liệu\nhợp lệ?}
    H -- Không --> I[Hiển thị lỗi từng trường]
    I --> F
    H -- Có --> J{Thay đổi\nảnh đại diện?}
    J -- Có --> K[Upload ảnh lên máy chủ]
    K --> L[Xử lý và nén ảnh]
    L --> M[Lưu đường dẫn ảnh mới]
    M --> N[Cập nhật thông tin vào CSDL]
    J -- Không --> N
    N --> O[Tính toán lại BMI]
    O --> P[Làm mới hiển thị hồ sơ]
    P --> Q[Hiển thị: 'Cập nhật thành công!']
    Q --> R([Kết thúc])
```

---

## UC05 – Ghi nhận chỉ số sức khỏe

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[Đăng nhập thành công]
    B --> C[Chọn mục 'Ghi nhận chỉ số']
    C --> D[Chọn loại chỉ số\nhuyết áp / nhịp tim / đường huyết\n/ cân nặng / nhiệt độ / khác]
    D --> E[Hệ thống hiển thị form nhập liệu]
    E --> F[Nhập giá trị chỉ số]
    F --> G[Chọn thời điểm đo]
    G --> H[Thêm ghi chú - tùy chọn]
    H --> I[Nhấn 'Lưu']
    I --> J{Giá trị\nhợp lệ?}
    J -- Không --> K[Hiển thị lỗi giá trị]
    K --> F
    J -- Có --> L[Lưu chỉ số vào CSDL]
    L --> M[Phân tích so với ngưỡng bình thường]
    M --> N{Chỉ số\nbất thường?}
    N -- Không --> O[Hiển thị ✓ 'Chỉ số bình thường']
    N -- Có --> P[Hiển thị cảnh báo và lời khuyên]
    P --> Q{Nguy hiểm\ncấp độ cao?}
    Q -- Có --> R[Gợi ý liên hệ bác sĩ ngay]
    Q -- Không --> S[Cập nhật biểu đồ và Dashboard]
    O --> S
    R --> S
    S --> T{Đạt mục tiêu\nđã đặt?}
    T -- Có --> U[Gửi thông báo chúc mừng]
    T -- Không --> V([Kết thúc])
    U --> V
```

---

## UC06 – Theo dõi hoạt động thể chất

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[Đăng nhập thành công]
    B --> C[Chọn mục 'Hoạt động thể chất']
    C --> D[Chọn loại hoạt động\nchạy bộ / đi bộ / đạp xe\n/ bơi lội / gym / yoga / khác]
    D --> E[Hiển thị màn hình theo dõi]
    E --> F[Nhấn nút 'Bắt đầu']
    F --> G[Bắt đầu tính thời gian]
    F --> H[Kích hoạt cảm biến\nGPS / gia tốc kế / nhịp tim]
    F --> I[Hiển thị chỉ số thời gian thực]
    G & H & I --> J{Người dùng\nnhấn 'Dừng'?}
    J -- Không --> K[Cập nhật dữ liệu\nvà lưu điểm GPS]
    K --> J
    J -- Có --> L[Tính toán kết quả tổng hợp\ntổng quãng đường, thời gian,\ncalories, tốc độ TB, nhịp tim TB]
    L --> M[Lưu kết quả hoạt động vào CSDL]
    M --> N[Hiển thị màn hình tổng kết\nbiểu đồ tốc độ, nhịp tim, lộ trình]
    N --> O[Cập nhật tổng calories trong ngày]
    O --> P{Đạt thành tích\nmới?}
    P -- Có --> Q[Hiển thị huy hiệu thành tích]
    P -- Không --> R[Thêm ghi chú hoặc chia sẻ - tùy chọn]
    Q --> R
    R --> S([Kết thúc])
```

---

## UC07 – Đặt mục tiêu sức khỏe

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[Đăng nhập thành công]
    B --> C[Chọn mục 'Mục tiêu sức khỏe']
    C --> D[Hệ thống hiển thị mục tiêu hiện tại\nvà gợi ý mục tiêu phù hợp]
    D --> E[Nhấn 'Thêm mục tiêu mới']
    E --> F[Chọn loại mục tiêu\ncân nặng / huyết áp / số bước/ngày\n/ calories / thời gian tập luyện]
    F --> G[Nhập giá trị mục tiêu\nvà thời hạn đạt mục tiêu]
    G --> H[Nhấn 'Lưu mục tiêu']
    H --> I{Dữ liệu\nhợp lệ?}
    I -- Không --> J[Hiển thị lỗi]
    J --> G
    I -- Có --> K[So sánh mục tiêu với dữ liệu hiện tại]
    K --> L{Mục tiêu có\nthực tế và an toàn?}
    L -- Không thực tế --> M[Hiển thị cảnh báo và lời khuyên điều chỉnh]
    M --> N[Người dùng xem xét\nđiều chỉnh hoặc giữ nguyên]
    N --> O[Lưu mục tiêu vào CSDL]
    L -- Có --> O
    O --> P[Tính toán tiến độ hiện tại %]
    P --> Q[Thiết lập lịch nhắc nhở định kỳ]
    Q --> R[Hiển thị mục tiêu với thanh tiến độ]
    R --> S[Hiển thị: 'Đã lưu mục tiêu thành công!']
    S --> T([Kết thúc])
```

---

## UC08 – Xem lịch sử sức khỏe

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[Đăng nhập thành công]
    B --> C[Chọn mục 'Lịch sử sức khỏe']
    C --> D[Hệ thống truy xuất dữ liệu\n7 ngày gần nhất mặc định]
    D --> E[Hiển thị danh sách và biểu đồ đường]
    E --> F[Chọn loại chỉ số cần xem\nhuyết áp / nhịp tim / cân nặng\n/ đường huyết / hoạt động / tất cả]
    F --> G[Chọn khoảng thời gian\nhôm nay / 7 ngày / 30 ngày / tùy chọn]
    G --> H[Hệ thống truy xuất dữ liệu\ntheo khoảng thời gian]
    H --> I{Có dữ liệu\ntrong khoảng thời gian?}
    I -- Không --> J[Hiển thị: 'Chưa có dữ liệu\ntrong khoảng thời gian này']
    I -- Có --> K[Vẽ biểu đồ với điểm min/max]
    K --> L[Hiển thị thống kê\ntrung bình, cao nhất, thấp nhất]
    L --> M{Người dùng\nchọn hành động}
    J --> M
    M -- Xem chi tiết --> N[Hiển thị popup chi tiết\ngiá trị, thời điểm, ghi chú]
    M -- Xuất dữ liệu --> O[Xuất CSV hoặc PDF]
    O --> P[Cho phép chia sẻ / tải về]
    M -- Xoá bản ghi --> Q[Xác nhận xoá]
    Q --> R[Xoá khỏi CSDL\nvà cập nhật biểu đồ]
    N --> S([Kết thúc])
    P --> S
    R --> S
```

---

## UC09 – Xem báo cáo thống kê

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[Đăng nhập thành công]
    B --> C[Chọn mục 'Báo cáo & Thống kê']
    C --> D[Hiển thị màn hình báo cáo]
    D --> E[Chọn loại báo cáo\nTổng quan / Hoạt động / Chỉ số\n/ Dinh dưỡng / So sánh]
    E --> F[Chọn khoảng thời gian\ntuần / tháng / quý / năm / tùy chọn]
    F --> G[Hệ thống truy xuất toàn bộ dữ liệu]
    G --> H[Tính toán chỉ số thống kê\nTB, min, max, xu hướng, tỉ lệ đạt mục tiêu]
    H --> I{Đủ dữ liệu\nđể tạo báo cáo?}
    I -- Không --> J[Hiển thị: 'Cần thêm dữ liệu\nđể tạo báo cáo']
    I -- Có --> K[Tạo biểu đồ tổng hợp\ncột, đường, tròn]
    K --> L[Hiển thị nhận xét tự động\ntheo xu hướng dữ liệu]
    L --> M[Hiển thị điểm sức khỏe tổng thể\nvà so sánh kỳ trước]
    M --> N{Người dùng\nchọn hành động}
    J --> N
    N -- Xem chi tiết --> O[Xem chi tiết theo ngày/tuần\nkhi nhấn vào biểu đồ]
    N -- Xuất báo cáo --> P[Tạo file PDF báo cáo đầy đủ]
    P --> Q[Cho phép tải về hoặc chia sẻ]
    N -- Chia sẻ với bác sĩ --> R[Tạo liên kết chia sẻ có thời hạn\nhoặc gửi qua email]
    O --> S([Kết thúc])
    Q --> S
    R --> S
```

---

## UC10 – Nhận thông báo nhắc nhở

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[Đăng nhập thành công]
    B --> C[Vào 'Cài đặt thông báo']
    C --> D[Hiển thị danh sách loại thông báo]
    D --> E[Bật/tắt từng loại thông báo\nnhắc uống thuốc / đo chỉ số\n/ tập thể dục / uống nước]
    E --> F[Cài đặt thời gian nhắc\ncho mỗi loại]
    F --> G[Nhấn 'Lưu cài đặt']
    G --> H[Lưu cấu hình vào CSDL]
    H --> I[Lên lịch tác vụ thông báo]
    I --> J[Hiển thị xác nhận 'Đã lưu']

    K([Khi đến giờ nhắc]) --> L{Thông báo\nloại này bật?}
    L -- Không --> M([Bỏ qua])
    L -- Có --> N{Người dùng\nđã thực hiện rồi?}
    N -- Có --> O([Bỏ qua lần này])
    N -- Không --> P[Gửi push notification\nđến thiết bị]
    P --> Q{Người dùng\nnhấn vào thông báo?}
    Q -- Có --> R[Mở ứng dụng và chuyển thẳng\nđến màn hình liên quan]
    Q -- Không / Bỏ qua --> S[Lưu thông báo đã bỏ qua\ntrong trung tâm thông báo]
    R --> T([Kết thúc])
    S --> T
```

---

## UC11 – Quản lý lịch uống thuốc

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[Đăng nhập thành công]
    B --> C[Chọn mục 'Lịch uống thuốc']
    C --> D[Hiển thị danh sách thuốc đang dùng\nvà lịch uống thuốc hôm nay]
    D --> E[Nhấn 'Thêm thuốc mới']
    E --> F[Nhập thông tin thuốc\ntên, liều lượng, tần suất,\ngiờ uống, ngày bắt đầu/kết thúc]
    F --> G[Nhấn 'Lưu']
    G --> H{Thông tin\nhợp lệ?}
    H -- Không --> I[Hiển thị lỗi]
    I --> F
    H -- Có --> J[Lưu thông tin thuốc vào CSDL]
    J --> K[Tạo lịch nhắc uống thuốc]
    K --> L[Hiển thị thuốc trong Calendar]
    L --> M[Hiển thị: 'Đã thêm thuốc thành công!']

    N([Khi đến giờ uống thuốc]) --> O[Gửi push notification\nnhắc uống thuốc với tên và liều lượng]
    O --> P[Người dùng nhấn vào thông báo]
    P --> Q{Hành động\ncủa người dùng}
    Q -- Xác nhận đã uống --> R[Ghi nhận đã uống\nvào lịch sử]
    R --> S[Đánh dấu ✓ trong lịch]
    Q -- Nhắc lại sau --> T[Thiết lập nhắc lại sau 15 phút]
    S --> U[Tính toán tỉ lệ tuân thủ uống thuốc %]
    T --> U
    U --> V[Cập nhật màn hình Tổng quan]
    V --> W([Kết thúc])
```

---

## UC12 – Chia sẻ dữ liệu với bác sĩ

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[Đăng nhập thành công]
    B --> C[Chọn mục 'Chia sẻ dữ liệu']
    C --> D[Hiển thị các phương thức chia sẻ\nvà danh sách bác sĩ đã kết nối]
    D --> E{Chọn\nphương thức}

    E -- Liên kết bác sĩ trực tiếp --> F[Nhập mã bác sĩ\nhoặc tìm kiếm theo tên/email]
    F --> G[Hệ thống tìm kiếm bác sĩ]
    G --> H{Tìm thấy\nbác sĩ?}
    H -- Không --> I[Hiển thị: 'Không tìm thấy bác sĩ']
    I --> F
    H -- Có --> J[Hiển thị thông tin bác sĩ\nđể xác nhận]
    J --> K[Chọn dữ liệu muốn chia sẻ\nloại chỉ số và khoảng thời gian]
    K --> L[Gửi yêu cầu kết nối đến bác sĩ]
    L --> M[Bác sĩ chấp nhận yêu cầu]
    M --> N[Cấp quyền truy cập dữ liệu\ncho tài khoản bác sĩ]
    N --> O[Thông báo: 'Kết nối thành công']

    E -- Tạo báo cáo PDF --> P[Chọn loại dữ liệu\nvà khoảng thời gian]
    P --> Q[Tổng hợp dữ liệu\nvà tạo file PDF]
    Q --> R{Tải về\nhoặc Gửi email?}
    R -- Tải về --> S[Tải file PDF về thiết bị]
    R -- Gửi email --> T[Nhập email bác sĩ\nvà gửi báo cáo]

    O --> U([Kết thúc])
    S --> U
    T --> U
```

---

*Tài liệu được tạo bởi: Hoàng Nam & Thế Lộc*
