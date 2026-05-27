# Hướng dẫn sử dụng

## 1. Giới thiệu

`QLTC` là ứng dụng quản lý thông tin thú cưng với giao diện đồ họa, giúp:
- Quản lý danh sách thú cưng.
- Thêm, sửa, xóa và tìm kiếm thú cưng.
- Theo dõi lịch sử cân nặng và xu hướng cân nặng.
- Lưu trữ dữ liệu dưới dạng CSV.

## 2. Yêu cầu hệ thống

### 2.1 Phần mềm
- Python 3.8 hoặc mới hơn.
- Thư viện Python:
  - `pandas`
  - `tkinter` (thường đã có sẵn trên Windows).

### 2.2 Dữ liệu
- `data/pets.csv`
- `data/weights.csv`

> Nếu các tệp này chưa tồn tại, ứng dụng sẽ tự động tạo lại khi khởi động.

## 3. Cài đặt

### 3.1 Tạo môi trường ảo

Trên Windows PowerShell:

```powershell
cd C:\Users\yughi\Downloads\QLTC
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3.2 Cài đặt thư viện

```powershell
pip install -r requirements.txt
```

## 4. Chạy ứng dụng

Trong thư mục dự án, chạy:

```powershell
python main.py
```

Ứng dụng sẽ mở giao diện người dùng và tải dữ liệu từ thư mục `data/`.

## 5. Sử dụng giao diện

### 5.1 Thêm thú cưng mới

1. Nhập tên thú cưng.
2. Chọn loài.
3. Nhập ngày sinh (ví dụ: `2024-01-15`).
4. Nhập trạng thái hiện tại.
5. Nhập ngày tiêm phòng tiếp theo.
6. Nhấn nút "Thêm" để lưu thông tin.

### 5.2 Chỉnh sửa thú cưng

1. Chọn thú cưng trong danh sách.
2. Thông tin sẽ được hiển thị trên form.
3. Sửa các trường cần thiết.
4. Nhấn nút cập nhật để lưu.

### 5.3 Xóa thú cưng

1. Chọn thú cưng muốn xóa.
2. Nhấn nút xóa.
3. Dữ liệu cân nặng liên quan cũng sẽ được xóa.

### 5.4 Tìm kiếm và lọc

- Nhập tên hoặc loài vào ô tìm kiếm.
- Ứng dụng hỗ trợ tìm gần đúng và không phân biệt dấu.

### 5.5 Xem lịch sử cân nặng

- Chọn thú cưng để xem lịch sử cân nặng.
- Ứng dụng tính xu hướng thay đổi cân nặng theo thời gian.

## 6. Cấu trúc thư mục

- `main.py`: điểm khởi chạy ứng dụng.
- `controllers/pet_controller.py`: xử lý logic nghiệp vụ.
- `models/pet_data_manager.py`: quản lý đọc/ghi dữ liệu CSV.
- `views/gui_view.py`: giao diện người dùng TKinter.
- `utils/validator.py`: kiểm tra dữ liệu đầu vào.
- `data/`: lưu trữ tệp CSV.

## 7. Lưu ý

- `requirements.txt` chỉ định phụ thuộc `pandas`.
- `tkinter` thường có sẵn trên Windows; nếu không, cài thêm gói Python phù hợp.
- Sao lưu dữ liệu CSV trước khi chỉnh sửa thủ công nếu bạn muốn giữ lại bản cũ.
