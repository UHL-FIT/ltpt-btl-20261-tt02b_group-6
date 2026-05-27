# Software Requirements Specification (SRS)

## 1. Giới thiệu

### 1.1 Mục đích

Tài liệu này mô tả các yêu cầu chức năng và phi chức năng của hệ thống `QLTC` - một ứng dụng quản lý thông tin thú cưng. Mục tiêu là cung cấp cơ sở để phát triển, kiểm thử và đánh giá hệ thống.

### 1.2 Phạm vi hệ thống

Hệ thống `QLTC` cho phép người dùng:

- Quản lý danh sách thú cưng.
- Nhập và lưu trữ thông tin thú cưng.
- Hiển thị dữ liệu thú cưng thông qua giao diện người dùng.
- Xác thực dữ liệu trước khi lưu.

Hệ thống hoạt động trên máy tính cá nhân, sử dụng tệp CSV làm nguồn dữ liệu chính.

## 2. Mô tả Tổng quan

### 2.1 Đặc điểm Người dùng (Actors)

- Người dùng chính: Người quản lý hoặc người dùng cuối nhập dữ liệu thú cưng.
- Hệ thống: Xử lý dữ liệu, xác thực và lưu trữ thông tin.

### 2.2 Môi trường Hoạt động

- Nền tảng: Máy tính chạy Python 3.x.
- Dữ liệu: Tệp CSV (`data/pets.csv`, `data/weights.csv`).
- Giao diện: Ứng dụng GUI (nếu có) hoặc giao diện dòng lệnh nhẹ.

## 3. Yêu cầu Chức năng (Functional Requirements)

1. Hệ thống phải cho phép người dùng xem danh sách thú cưng hiện có.
2. Hệ thống phải cho phép người dùng nhập thông tin thú cưng mới.
3. Hệ thống phải xác thực dữ liệu nhập trước khi lưu.
4. Hệ thống phải lưu thông tin thú cưng vào tệp CSV.
5. Hệ thống phải cung cấp khả năng đọc dữ liệu từ các tệp CSV để hiển thị và xử lý.
6. Hệ thống phải xử lý lỗi khi tệp dữ liệu bị thiếu hoặc định dạng không chính xác.

## 4. Yêu cầu Phi chức năng (Non-Functional Requirements)

- Hiệu năng: Hệ thống phải phản hồi các thao tác cơ bản trong vòng vài giây.
- Độ tin cậy: Dữ liệu phải được lưu chính xác và không bị mất khi thực hiện thao tác thêm mới.
- Khả năng mở rộng: Cấu trúc mã nguồn phải cho phép bổ sung các chức năng mới như tìm kiếm hoặc cập nhật dữ liệu.
- Bảo trì: Mã nguồn phải được tổ chức rõ ràng theo mô hình MVC nhẹ để dễ dàng bảo trì.
- Tính tương thích: Ứng dụng phải chạy trên môi trường Python 3.x và tương thích với Windows.
