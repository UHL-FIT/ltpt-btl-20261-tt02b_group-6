# Hệ Thống Quản Lý Thú Cưng (QLTC)

## 1. Giới thiệu

QLTC là ứng dụng quản lý thú cưng bằng Python và Tkinter. Ứng dụng cung cấp giao diện trực quan để:
- Thêm, sửa, xóa thú cưng.
- Tìm kiếm và lọc danh sách thú cưng.
- Theo dõi lịch sử cân nặng và xu hướng cân nặng theo tháng.
- Xuất báo cáo ra file CSV hoặc Excel.

## 2. Yêu cầu

- Python 3.8 trở lên (khuyến nghị Python 3.14).
- Thư viện Python:
  - `pandas`
  - `openpyxl` (để xuất file Excel)
  - `tkinter` (thường đã có sẵn trên Windows)

## 3. Cài đặt

1. Mở terminal và chuyển đến thư mục dự án:

2. Tạo và kích hoạt môi trường ảo (nếu muốn):

python -m venv venv.\venv\Scripts\Activate.ps1

3. Cài đặt các thư viện:

pip install -r requirements.txt

## 4. Chạy ứng dụng

Trong thư mục dự án, chạy:

```powershell
python main.py
```

Ứng dụng sẽ mở cửa sổ GUI và tự động tạo `data/pets.csv` và `data/weights.csv` nếu chúng chưa tồn tại.

## 5. Hướng dẫn sử dụng

### 5.1 Thêm thú cưng

- Nhấn nút `➕ Thêm thú cưng`.
- Nhập tên, loài, ngày sinh, tình trạng, cân nặng và hạn tiêm tiếp theo.
- Nhấn `Thêm` để lưu.

### 5.2 Chỉnh sửa thú cưng

- Chọn thú cưng trong bảng danh sách.
- Nhấn `✏️ Chỉnh sửa`.
- Thay đổi thông tin, bao gồm cả cân nặng nếu muốn.
- Nhấn `Lưu thay đổi` để cập nhật.

### 5.3 Xóa thú cưng

- Chọn một thú cưng.
- Nhấn `🗑️ Xóa`.
- Thông tin cân nặng liên quan cũng sẽ bị xóa.

### 5.4 Tìm kiếm

- Sử dụng ô tìm kiếm và lựa chọn tiêu chí tìm kiếm.
- Có thể tìm theo: Tất cả, Tên, Loài, Trạng thái, Ngày sinh, Cân nặng, Hạn tiêm.
- Ứng dụng hỗ trợ tìm gần đúng và loại bỏ dấu tiếng Việt.

### 5.5 Xem lịch sử cân nặng

- Chọn thú cưng rồi bấm `📈 Lịch sử cân nặng`.
- Mở cửa sổ hiển thị lịch sử cân nặng và trung bình cân nặng theo tháng.

### 5.6 Xuất báo cáo

- Nhấn `📤 Xuất file báo cáo`.
- Chọn file CSV hoặc Excel để lưu dữ liệu hiện tại.

## 6. Cấu trúc thư mục

- `main.py`: điểm khởi chạy ứng dụng.
- `views/gui_view.py`: định nghĩa giao diện và tương tác người dùng.
- `controllers/pet_controller.py`: xử lý logic điều khiển.
- `models/pet_data_manager.py`: quản lý dữ liệu CSV và lịch sử cân nặng.
- `utils/validator.py`: kiểm tra dữ liệu đầu vào.
- `data/`: chứa các tệp dữ liệu `pets.csv` và `weights.csv`.
- `requirements.txt`: danh sách phụ thuộc cần cài.

## 7. Lưu ý

- Nếu `data/pets.csv` hoặc `data/weights.csv` không tồn tại, ứng dụng sẽ tự tạo.
- Nếu muốn sửa dữ liệu thủ công, hãy sao lưu các tệp CSV trước.
- `tkinter` thường đã có sẵn trên Windows; nếu không, cài đặt Python phiên bản có hỗ trợ GUI.

## 8. Ghi chú thêm

Ứng dụng hiện tại hỗ trợ tính năng:
- Hiển thị cảnh báo tiêm phòng sắp tới/hết hạn.
- Điều chỉnh kích thước bảng và giao diện tự co giãn.
- Lưu trữ cân nặng cuối cùng và sử dụng nó để tìm kiếm.
