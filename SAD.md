# Software Architecture Document (SAD)

## 1. Giới thiệu

Ứng dụng `QLTC` là một hệ thống quản lý dữ liệu thú cưng, bao gồm nhập liệu, xác thực thông tin và hiển thị giao diện. Mục tiêu của tài liệu này là mô tả kiến trúc tổng thể, cấu trúc mã nguồn, công nghệ sử dụng và luồng dữ liệu chính của hệ thống.

## 2. Kiến trúc Tổng thể

Ứng dụng được xây dựng theo mô hình phân tách trách nhiệm rõ ràng giữa các thành phần:

- `controllers/`: Điều phối logic nghiệp vụ và xử lý yêu cầu từ giao diện.
- `models/`: Quản lý dữ liệu và tương tác với nguồn dữ liệu (CSV).
- `views/`: Giao diện người dùng, hiển thị dữ liệu và nhận nhập liệu.
- `utils/`: Chứa các tiện ích hỗ trợ, như xác thực đầu vào.
- `data/`: Chứa các tệp dữ liệu CSV làm nguồn chính.
- `main.py`: Điểm khởi chạy ứng dụng, kết nối các thành phần lại với nhau.

Kiến trúc này phù hợp với mô hình MVC nhẹ (Model-View-Controller), giúp giữ mã nguồn dễ bảo trì và mở rộng.

## 3. Cấu trúc Source Code

- `main.py`
  - Khởi tạo ứng dụng và khởi chạy giao diện.

- `controllers/pet_controller.py`
  - Điều khiển luồng xử lý dữ liệu thú cưng.
  - Gọi `PetDataManager` để lấy/lưu dữ liệu.
  - Kết hợp với `validator` để kiểm tra dữ liệu nhập.

- `models/pet_data_manager.py`
  - Tải dữ liệu từ `data/pets.csv` và `data/weights.csv`.
  - Cung cấp API để truy vấn, thêm và cập nhật dữ liệu thú cưng.

- `views/gui_view.py`
  - Xây dựng giao diện người dùng (GUI).
  - Hiển thị danh sách thú cưng và nhận tương tác người dùng.
  - Giao tiếp với controller để thực thi hành động.

- `utils/validator.py`
  - Chứa các hàm kiểm tra dữ liệu hợp lệ.
  - Đảm bảo dữ liệu đầu vào tuân thủ định dạng mong muốn trước khi lưu.

- `data/pets.csv`
  - Lưu thông tin chính của thú cưng.

- `data/weights.csv`
  - Lưu lịch sử cân nặng hoặc thông tin liên quan khác.

## 4. Công nghệ sử dụng

- Python 3.x: Ngôn ngữ lập trình chính.
- CSV: Định dạng lưu trữ dữ liệu nhẹ, dễ sử dụng.
- GUI framework: Nếu giao diện sử dụng thư viện tiêu chuẩn như `tkinter`, thì đây là thành phần xây dựng giao diện.

Lưu ý: Nếu dự án đang sử dụng một thư viện GUI cụ thể thì file `views/gui_view.py` sẽ xác định chi tiết hơn.

## 5. Luồng dữ liệu

1. Người dùng tương tác với giao diện trong `views/gui_view.py`.
2. `gui_view` gửi yêu cầu đến `controllers/pet_controller.py`.
3. `pet_controller` kiểm tra dữ liệu đầu vào bằng `utils/validator.py`.
4. Nếu dữ liệu hợp lệ, controller gọi `models/pet_data_manager.py` để đọc/ghi dữ liệu CSV.
5. `PetDataManager` cập nhật dữ liệu trong bộ nhớ hoặc lưu trở lại tệp trong `data/`.
6. Kết quả trả về controller, sau đó giao diện cập nhật hiển thị cho người dùng.

## 6. Mở rộng và bảo trì

- Có thể mở rộng `models/` để hỗ trợ nguồn dữ liệu khác như SQLite hoặc JSON.
- Thêm các module controller mới để xử lý các chức năng quản lý bổ sung.
- Nâng cấp `views/` để dùng GUI hiện đại hơn nếu cần.

---

Tài liệu này cung cấp một bức tranh tổng quan giúp bảo trì, phát triển và mở rộng hệ thống dễ dàng hơn.