from models.pet_data_manager import PetDataManager


class PetController:

    """Controller xử lý logic giữa giao diện và lớp quản lý dữ liệu."""

    def __init__(self):

        # Khởi tạo model để thao tác với dữ liệu thú cưng.
        self.model = PetDataManager()

    def add_pet(
        self,
        name,
        species,
        dob,
        status,
        vac
    ):

        """Thêm thú cưng mới vào dữ liệu."""
        return self.model.add_pet(
            name,
            species,
            dob,
            status,
            vac
        )

    def delete_pet(self, pet_id):

        """Xóa thú cưng theo ID và xóa luôn dữ liệu cân nặng liên quan."""
        self.model.delete_pet(pet_id)

    def get_pets(self):

        """Lấy danh sách tất cả thú cưng."""
        return self.model.get_pets()

    def search_pets(self, query, species=None):

        """Tìm thú cưng theo tên hoặc loài, hỗ trợ lọc theo loài cụ thể."""
        return self.model.search_pets(query, species)

    def update_pet(
        self,
        pet_id,
        name,
        species,
        dob,
        status,
        vac
    ):

        """Cập nhật dữ liệu thú cưng đã tồn tại."""
        self.model.update_pet(
            pet_id,
            name,
            species,
            dob,
            status,
            vac
        )

    def add_weight(
        self,
        pet_id,
        date,
        weight
    ):

        """Ghi nhận cân nặng mới cho một thú cưng."""
        self.model.add_weight(
            pet_id,
            date,
            weight
        )

    def get_weight_history(
        self,
        pet_id
    ):

        """Lấy lịch sử cân nặng cho thú cưng theo ID."""
        return self.model.get_weight_history(
            pet_id
        )

    def get_monthly_weight_trend(
        self,
        pet_id
    ):

        """Tính xu hướng cân nặng theo tháng cho thú cưng."""
        return self.model.get_monthly_weight_trend(
            pet_id
        )

    def get_latest_weight(
        self,
        pet_id
    ):

        """Lấy cân nặng mới nhất của thú cưng theo ID."""
        return self.model.get_latest_weight(
            pet_id
        )

    def get_statistics(self):

        """Lấy các thống kê tổng hợp cho dashboard."""
        return self.model.get_statistics()
