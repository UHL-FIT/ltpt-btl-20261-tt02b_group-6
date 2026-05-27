import tkinter as tk

from tkinter import ttk
from tkinter import messagebox

from datetime import datetime
from pathlib import Path

from controllers.pet_controller import PetController
from utils.validator import validate_date, validate_name


class PetApp:

    """Giao diện chính của ứng dụng quản lý thú cưng.

    Quản lý form nhập, tìm kiếm, danh sách thú cưng, và các hành động
    liên quan đến cân nặng, sửa/xóa, xuất báo cáo.
    """

    def __init__(self, root):

        """Khởi tạo cửa sổ chính, cấu hình giao diện và tải dữ liệu ban đầu."""
        self.root = root

        self.root.title(
            "Quản Lý Thú Cưng"
        )

        self.root.geometry(
            "1000x650"
        )

        self.controller = PetController()
        self.editing_pet_id = None

        self.create_widgets()

        self.refresh_data()

    def create_widgets(self):

        """Tạo tất cả widget giao diện người dùng: dashboard, form, tìm kiếm, bảng dữ liệu."""
        top_frame = ttk.Frame(self.root)
        top_frame.pack(
            fill=tk.BOTH,
            expand=False,
            padx=10,
            pady=10
        )

        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)

        dashboard = ttk.LabelFrame(
            top_frame,
            text="Dashboard"
        )

        dashboard.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 5),
            pady=0
        )

        form = ttk.LabelFrame(
            top_frame,
            text="Thêm thú cưng"
        )

        form.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 0),
            pady=0
        )

        self.lbl_total = ttk.Label(
            dashboard,
            text="Tổng số thú cưng: 0",
            font=('Arial', 10, 'bold')
        )

        self.lbl_total.pack(
            anchor=tk.W,
            padx=10,
            pady=5
        )

        self.lbl_avg_age = ttk.Label(
            dashboard,
            text="Tuổi trung bình: 0 năm",
            font=('Arial', 10, 'bold')
        )

        self.lbl_avg_age.pack(
            anchor=tk.W,
            padx=10,
            pady=5
        )

        ttk.Label(
            dashboard,
            text="Cảnh báo tiêm phòng:",
            foreground='red'
        ).pack(
            anchor=tk.W,
            padx=10
        )

        self.warning_listbox = tk.Listbox(
            dashboard,
            height=5,
            fg='red'
        )

        self.warning_listbox.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=5
        )

        form.columnconfigure(1, weight=1)

        ttk.Label(
            form,
            text="Tên"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky=tk.W
        )

        self.ent_name = ttk.Entry(form)

        self.ent_name.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        ttk.Label(
            form,
            text="Loài"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky=tk.W
        )

        self.species_options = [
            "Chó",
            "Mèo",
            "Thỏ",
            "Chim",
            "Chuột"
        ]

        self.ent_species = ttk.Combobox(
            form,
            values=self.species_options,
            state="readonly"
        )

        self.ent_species.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        self.ent_species.current(0)

        ttk.Label(
            form,
            text="Ngày sinh"
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky=tk.W
        )

        dob_frame = ttk.Frame(form)
        dob_frame.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        day_options = [str(i).zfill(2) for i in range(1, 32)]
        month_options = [str(i).zfill(2) for i in range(1, 13)]
        year_options = [str(i) for i in range(2000, datetime.today().year + 1)]

        self.ent_dob_day = ttk.Combobox(
            dob_frame,
            values=day_options,
            width=4,
            state="readonly"
        )
        self.ent_dob_day.pack(
            side=tk.LEFT,
            padx=(0, 5)
        )
        self.ent_dob_day.current(0)

        self.ent_dob_month = ttk.Combobox(
            dob_frame,
            values=month_options,
            width=4,
            state="readonly"
        )
        self.ent_dob_month.pack(
            side=tk.LEFT,
            padx=(0, 5)
        )
        self.ent_dob_month.current(0)

        self.ent_dob_year = ttk.Combobox(
            dob_frame,
            values=year_options,
            width=6,
            state="readonly"
        )
        self.ent_dob_year.pack(
            side=tk.LEFT
        )
        self.ent_dob_year.current(len(year_options) - 1)

        ttk.Label(
            form,
            text="Tình trạng"
        ).grid(
            row=3,
            column=0,
            padx=5,
            pady=5
        )

        self.cmb_status = ttk.Combobox(
            form,
            values=[
                "Khỏe mạnh",
                "Cần theo dõi",
                "Đang điều trị",
                "Bị thương"
            ],
            state="readonly"
        )

        self.cmb_status.grid(
            row=3,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        self.cmb_status.current(0)

        ttk.Label(
            form,
            text="Ngày tiêm"
        ).grid(
            row=4,
            column=0,
            padx=5,
            pady=5,
            sticky=tk.W
        )

        vac_frame = ttk.Frame(form)
        vac_frame.grid(
            row=4,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        self.ent_vac_day = ttk.Combobox(
            vac_frame,
            values=day_options,
            width=4,
            state="readonly"
        )
        self.ent_vac_day.pack(
            side=tk.LEFT,
            padx=(0, 5)
        )
        self.ent_vac_day.current(0)

        self.ent_vac_month = ttk.Combobox(
            vac_frame,
            values=month_options,
            width=4,
            state="readonly"
        )
        self.ent_vac_month.pack(
            side=tk.LEFT,
            padx=(0, 5)
        )
        self.ent_vac_month.current(0)

        self.ent_vac_year = ttk.Combobox(
            vac_frame,
            values=year_options,
            width=6,
            state="readonly"
        )
        self.ent_vac_year.pack(
            side=tk.LEFT
        )
        self.ent_vac_year.current(len(year_options) - 1)

        ttk.Label(
            form,
            text="Cân nặng (kg)"
        ).grid(
            row=5,
            column=0,
            padx=5,
            pady=5,
            sticky=tk.W
        )

        self.ent_weight = ttk.Entry(form)
        self.ent_weight.grid(
            row=5,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        form_btn_frame = ttk.Frame(form)
        form_btn_frame.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=10
        )

        self.add_pet_button = ttk.Button(
            form_btn_frame,
            text="Thêm thú cưng",
            command=self.add_pet
        )
        self.add_pet_button.pack(
            fill=tk.X,
            expand=True
        )

        columns = (
            'ID',
            'Name',
            'Species',
            'DOB',
            'Status',
            'Weight',
            'NextVac'
        )

        pets_frame = ttk.LabelFrame(
            self.root,
            text="Thú cưng"
        )

        pets_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        search_frame = ttk.Frame(pets_frame)
        search_frame.pack(
            fill=tk.X,
            padx=10,
            pady=(10, 5)
        )

        ttk.Label(
            search_frame,
            text="Tên hoặc loài"
        ).pack(
            side=tk.LEFT,
            padx=(0, 5)
        )

        self.ent_search = ttk.Entry(search_frame)
        self.ent_search.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            padx=(0, 5)
        )

        ttk.Label(
            search_frame,
            text="Loài"
        ).pack(
            side=tk.LEFT,
            padx=(10, 5)
        )

        self.search_species_options = [
            "Tất cả",
            *self.species_options
        ]

        self.cmb_search_species = ttk.Combobox(
            search_frame,
            values=self.search_species_options,
            state="readonly",
            width=12
        )
        self.cmb_search_species.pack(
            side=tk.LEFT,
            padx=(0, 5)
        )
        self.cmb_search_species.current(0)

        ttk.Button(
            search_frame,
            text="Tìm",
            command=self.search_pets
        ).pack(
            side=tk.LEFT
        )

        btn_frame = ttk.Frame(pets_frame)

        btn_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

        ttk.Button(
            btn_frame,
            text="Sửa",
            command=self.prepare_edit_pet
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        ttk.Button(
            btn_frame,
            text="Xóa",
            command=self.delete_pet
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        ttk.Button(
            btn_frame,
            text="Xem lịch sử cân nặng",
            command=self.view_weight_history
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        ttk.Button(
            btn_frame,
            text="Xuất Excel",
            command=self.export_to_excel
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        self.tree = ttk.Treeview(
            pets_frame,
            columns=columns,
            show='headings'
        )

        heading_map = {
            'ID': 'ID',
            'Name': 'Tên',
            'Species': 'Loài',
            'DOB': 'Ngày sinh',
            'Status': 'Trạng thái',
            'Weight': 'Cân nặng',
            'NextVac': 'Ngày tiêm'
        }

        for col in columns:

            self.tree.heading(
                col,
                text=heading_map.get(col, col)
            )
            self.tree.column(
                col,
                width=100 if col != 'ID' else 60,
                anchor=tk.W,
                stretch=True
            )

        self.tree.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=(10, 10)
        )

    def add_pet(self):

        """Xử lý sự kiện thêm/cập nhật thú cưng và ghi cân nặng nếu có."""
        name = self.ent_name.get()

        species = self.ent_species.get()

        dob = f"{self.ent_dob_year.get()}-{self.ent_dob_month.get()}-{self.ent_dob_day.get()}"

        status = self.cmb_status.get()

        vac = f"{self.ent_vac_year.get()}-{self.ent_vac_month.get()}-{self.ent_vac_day.get()}"

        if not validate_name(name):

            messagebox.showerror(
                "Lỗi",
                "Tên thú cưng không được chứa số hoặc ký tự đặc biệt"
            )

            return

        if not validate_date(dob):

            messagebox.showerror(
                "Lỗi",
                "Sai ngày sinh"
            )

            return

        if species not in self.species_options:

            messagebox.showerror(
                "Lỗi",
                "Loài phải là Chó, Mèo, Thỏ, Chim hoặc Chuột"
            )

            return

        if not validate_date(vac):

            messagebox.showerror(
                "Lỗi",
                "Sai ngày tiêm"
            )

            return

        weight_text = self.ent_weight.get().strip()
        weight = None

        if weight_text:
            try:
                weight = float(weight_text)
            except ValueError:
                messagebox.showerror(
                    "Lỗi",
                    "Cân nặng phải là số"
                )
                return

            if weight <= 0:
                messagebox.showerror(
                    "Lỗi",
                    "Cân nặng phải lớn hơn 0"
                )
                return

        if self.editing_pet_id is not None:
            self.controller.update_pet(
                self.editing_pet_id,
                name,
                species,
                dob,
                status,
                vac
            )
            self.editing_pet_id = None
            self.add_pet_button.config(text="Thêm thú cưng")
        else:
            new_pet_id = self.controller.add_pet(
                name,
                species,
                dob,
                status,
                vac
            )

            if weight is not None:
                today = datetime.today().strftime('%Y-%m-%d')
                self.controller.add_weight(
                    new_pet_id,
                    today,
                    weight
                )

        self.ent_weight.delete(0, tk.END)
        self.refresh_data()

    def refresh_data(self, pets=None):

        """Làm mới dữ liệu trên bảng và dashboard, hiển thị kết quả tìm kiếm nếu có."""
        for i in self.tree.get_children():

            self.tree.delete(i)

        if pets is None:
            pets = self.controller.get_pets()

        stats = self.controller.get_statistics()

        self.lbl_total.config(
            text=f"Tổng số thú cưng: {stats['total']}"
        )

        self.lbl_avg_age.config(
            text=f"Tuổi trung bình: {stats['avg_age']} năm"
        )

        self.warning_listbox.delete(
            0,
            tk.END
        )

        for warn in stats['warnings']:

            self.warning_listbox.insert(
                tk.END,
                warn
            )

        for _, row in pets.iterrows():

            latest_weight = self.controller.get_latest_weight(
                row['ID']
            )

            self.tree.insert(
                '',
                tk.END,
                values=(
                    row['ID'],
                    row['Name'],
                    row['Species'],
                    row['DOB'],
                    row['Status'],
                    latest_weight,
                    row['NextVaccinationDate']
                )
            )

    def get_selected_pet(self):

        """Trả về dữ liệu của thú cưng đang được chọn trên bảng."""
        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Cảnh báo",
                "Chọn thú cưng"
            )

            return None

        item = self.tree.item(
            selected[0]
        )

        return item['values']

    def delete_pet(self):

        """Xóa thú cưng đã chọn khỏi danh sách và cập nhật giao diện."""
        pet = self.get_selected_pet()

        if not pet:
            return

        self.controller.delete_pet(
            pet[0]
        )

        self.refresh_data()

    def add_weight(self):

        """Ghi nhận cân nặng mới cho thú cưng đang được chọn."""
        pet = self.get_selected_pet()

        if not pet:
            return

        weight_text = self.ent_weight.get().strip()

        if not weight_text:
            messagebox.showerror(
                "Lỗi",
                "Nhập cân nặng"
            )
            return

        try:
            weight = float(weight_text)
        except ValueError:
            messagebox.showerror(
                "Lỗi",
                "Cân nặng phải là số"
            )
            return

        if weight <= 0:
            messagebox.showerror(
                "Lỗi",
                "Cân nặng phải lớn hơn 0"
            )
            return

        date = datetime.today().strftime(
            '%Y-%m-%d'
        )

        self.controller.add_weight(
            pet[0],
            date,
            weight
        )

        self.ent_weight.delete(0, tk.END)
        self.refresh_data()

    def prepare_edit_pet(self):

        """Chuẩn bị form để chỉnh sửa thông tin thú cưng đang chọn."""
        pet = self.get_selected_pet()

        if not pet:
            return

        self.editing_pet_id = pet[0]
        self.add_pet_button.config(text="Cập nhật thú cưng")

        self.ent_name.delete(0, tk.END)
        self.ent_name.insert(0, pet[1])

        if pet[2] in self.species_options:
            self.ent_species.set(pet[2])
        else:
            self.ent_species.set(self.species_options[0])

        dob_parts = str(pet[3]).split('-')
        if len(dob_parts) == 3:
            self.ent_dob_year.set(dob_parts[0])
            self.ent_dob_month.set(dob_parts[1])
            self.ent_dob_day.set(dob_parts[2])

        self.cmb_status.set(pet[4])

        vac_parts = str(pet[6]).split('-')
        if len(vac_parts) == 3:
            self.ent_vac_year.set(vac_parts[0])
            self.ent_vac_month.set(vac_parts[1])
            self.ent_vac_day.set(vac_parts[2])

        self.ent_weight.delete(0, tk.END)

    def search_pets(self):

        """Tìm kiếm thú cưng theo tên/loài và cập nhật bảng kết quả."""
        query = self.ent_search.get().strip()
        species = self.cmb_search_species.get()

        if species == "Tất cả":
            species = None

        pets = self.controller.search_pets(query, species)

        self.refresh_data(pets)

    def view_weight_history(self):

        """Hiển thị cửa sổ lịch sử và xu hướng cân nặng của thú cưng đã chọn."""
        pet = self.get_selected_pet()

        if not pet:
            return

        history = self.controller.get_weight_history(
            pet[0]
        )

        win = tk.Toplevel(self.root)

        win.title(
            "Lịch sử cân nặng"
        )

        win.geometry(
            "400x400"
        )

        text = tk.Text(win)

        text.pack(
            fill=tk.BOTH,
            expand=True
        )

        if history.empty:

            text.insert(
                tk.END,
                "Chưa có dữ liệu"
            )

        else:

            text.insert(
                tk.END,
                "Lịch sử cân nặng:\n"
            )

            for _, row in history.iterrows():

                text.insert(
                    tk.END,
                    f"{row['Date'].strftime('%Y-%m-%d')} "
                    f"- {row['Weight']} kg\n"
                )

            text.insert(
                tk.END,
                "\nXu hướng cân nặng theo tháng:\n"
            )

            trend = self.controller.get_monthly_weight_trend(
                pet[0]
            )

            if trend.empty:
                text.insert(
                    tk.END,
                    "Chưa có đủ dữ liệu để theo dõi theo tháng"
                )
            else:
                for _, row in trend.iterrows():
                    text.insert(
                        tk.END,
                        f"{row['Month']} - {row['Weight']} kg\n"
                    )

    def export_to_excel(self):

        """Xuất dữ liệu thú cưng ra file Excel kèm cân nặng mới nhất."""
        try:
            import pandas as pd
        except Exception:
            messagebox.showerror(
                "Lỗi",
                "Cần cài đặt pandas để xuất Excel.\nChạy: pip install pandas openpyxl"
            )
            return

        pets = self.controller.get_pets()

        if pets is None or pets.empty:
            messagebox.showinfo(
                "Thông báo",
                "Không có dữ liệu để xuất"
            )
            return

        df = pets.copy()

        # Thêm cột cân nặng mới nhất
        df['LatestWeight'] = df['ID'].apply(lambda pid: self.controller.get_latest_weight(pid))

        out_path = Path('Danh_sach_thu_cung.xlsx')

        try:
            df.to_excel(out_path, index=False)
            messagebox.showinfo(
                "Hoàn tất",
                f"Đã xuất file: {out_path}"
            )
        except Exception as e:
            messagebox.showerror(
                "Lỗi",
                f"Không thể lưu file Excel: {e}"
            )