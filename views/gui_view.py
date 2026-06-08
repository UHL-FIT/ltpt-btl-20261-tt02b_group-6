import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from datetime import datetime
from pathlib import Path

from controllers.pet_controller import PetController
from utils.validator import validate_date, validate_name

# --- HỆ THỐNG MÀU SẮC MODERN PREMIUM LIGHT THEME ---
BG_COLOR = "#F3F4F6"          # Nền cửa sổ chính (Slate-light)
CARD_BG = "#FFFFFF"           # Nền các thẻ/form (White)
BORDER_COLOR = "#E5E7EB"      # Màu đường viền nhẹ (Gray)
TEXT_PRIMARY = "#1F2937"      # Chữ chính (Charcoal)
TEXT_SECONDARY = "#4B5563"    # Chữ phụ (Muted gray)

COLOR_PRIMARY = "#4F46E5"     # Indigo (Accent chính)
COLOR_PRIMARY_HOVER = "#4338CA"
COLOR_SUCCESS = "#10B981"     # Emerald (Thành công, Khỏe mạnh, Thêm mới)
COLOR_SUCCESS_HOVER = "#059669"
COLOR_WARNING = "#F59E0B"     # Amber (Cần theo dõi, Cảnh báo nhẹ)
COLOR_DANGER = "#EF4444"      # Crimson/Red (Bị thương, Đang điều trị, Xóa)
COLOR_DANGER_HOVER = "#DC2626"
COLOR_INFO = "#3B82F6"        # Blue (Thông tin, Sửa)
COLOR_INFO_HOVER = "#2563EB"

class PetApp:
    """Giao diện chính của ứng dụng quản lý thú cưng.
    
    Quản lý form nhập, tìm kiếm, danh sách thú cưng, và các hành động
    liên quan đến cân nặng, sửa/xóa, xuất báo cáo.
    """

    def __init__(self, root):
        """Khởi tạo cửa sổ chính, cấu hình giao diện và tải dữ liệu ban đầu."""
        self.root = root
        self.root.title("🐾 HỆ THỐNG QUẢN LÝ THÚ CƯNG 🐾")
        self.root.geometry("1150x720")
        
        self.controller = PetController()
        self.species_options = ["Chó", "Mèo", "Thỏ", "Chim", "Chuột"]

        self.setup_styles()
        self.create_widgets()
        self.refresh_data()

    def setup_styles(self):
        """Thiết lập hệ thống style hiện đại sử dụng clam theme."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.root.configure(bg=BG_COLOR)
        
        # TFrame
        self.style.configure("TFrame", background=BG_COLOR)
        
        # TLabel
        self.style.configure("TLabel", background=BG_COLOR, foreground=TEXT_PRIMARY, font=("Segoe UI", 10))
        
        # Nút bấm Primary (Indigo)
        self.style.configure("Primary.TButton", background=COLOR_PRIMARY, foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0, padding=(12, 6))
        self.style.map("Primary.TButton", background=[("active", COLOR_PRIMARY_HOVER), ("pressed", COLOR_PRIMARY_HOVER)])
        
        # Nút bấm Success (Emerald)
        self.style.configure("Success.TButton", background=COLOR_SUCCESS, foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0, padding=(12, 6))
        self.style.map("Success.TButton", background=[("active", COLOR_SUCCESS_HOVER), ("pressed", COLOR_SUCCESS_HOVER)])
        
        # Nút bấm Danger (Crimson)
        self.style.configure("Danger.TButton", background=COLOR_DANGER, foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0, padding=(12, 6))
        self.style.map("Danger.TButton", background=[("active", COLOR_DANGER_HOVER), ("pressed", COLOR_DANGER_HOVER)])
        
        # Nút bấm Info (Blue)
        self.style.configure("Info.TButton", background=COLOR_INFO, foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0, padding=(12, 6))
        self.style.map("Info.TButton", background=[("active", COLOR_INFO_HOVER), ("pressed", COLOR_INFO_HOVER)])
        
        # Nút bấm Secondary (Gray)
        self.style.configure("Secondary.TButton", background="#E5E7EB", foreground=TEXT_PRIMARY, font=("Segoe UI", 10), borderwidth=0, padding=(12, 6))
        self.style.map("Secondary.TButton", background=[("active", "#D1D5DB"), ("pressed", "#D1D5DB")])

        # Nhãn cho Form
        self.style.configure("FormLabel.TLabel", background=CARD_BG, foreground=TEXT_PRIMARY, font=("Segoe UI", 10, "bold"))

        # Entries & Comboboxes
        self.style.configure("TEntry", fieldbackground="#FFFFFF", bordercolor=BORDER_COLOR, lightcolor=BORDER_COLOR, darkcolor=BORDER_COLOR, padding=5)
        self.style.configure("TCombobox", fieldbackground="#FFFFFF", bordercolor=BORDER_COLOR, lightcolor=BORDER_COLOR, darkcolor=BORDER_COLOR, padding=5)
        
        # Treeview (Bảng danh sách)
        self.style.configure("Treeview", 
                             background=CARD_BG, 
                             foreground=TEXT_PRIMARY, 
                             rowheight=32, 
                             fieldbackground=CARD_BG,
                             font=("Segoe UI", 10),
                             borderwidth=0)
        self.style.map("Treeview",
                       background=[("selected", COLOR_PRIMARY)],
                       foreground=[("selected", "white")])
                       
        self.style.configure("Treeview.Heading", 
                             background="#F3F4F6", 
                             foreground=TEXT_PRIMARY, 
                             font=("Segoe UI", 10, "bold"),
                             borderwidth=1,
                             bordercolor=BORDER_COLOR,
                             padding=8)

    def create_card(self, parent, title="", highlight_color=None):
        """Hàm trợ giúp tạo thẻ (Card) trắng hiện đại với viền nhẹ và thanh đánh dấu màu."""
        card = tk.Frame(parent, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightcolor=BORDER_COLOR, highlightthickness=1, bd=0)
        
        if highlight_color:
            accent = tk.Frame(card, bg=highlight_color, width=4)
            accent.pack(side=tk.LEFT, fill=tk.Y)
            
        content = tk.Frame(card, bg=CARD_BG, padx=15, pady=12)
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        if title:
            lbl_title = tk.Label(content, text=title, font=("Segoe UI", 10, "bold"), fg=TEXT_SECONDARY, bg=CARD_BG, anchor="w")
            lbl_title.pack(fill=tk.X, pady=(0, 6))
            
        return card, content

    def create_widgets(self):
        """Tạo tất cả widget giao diện người dùng theo phong cách thiết kế hiện đại."""
        # 1. Header Bar cực đẹp
        header_frame = tk.Frame(self.root, bg=COLOR_PRIMARY, height=70)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        header_title = tk.Label(header_frame, text="🐾 HỆ THỐNG QUẢN LÝ THÚ CƯNG 🐾", fg="white", bg=COLOR_PRIMARY, font=("Segoe UI", 15, "bold"))
        header_title.pack(side=tk.LEFT, padx=20, pady=15)
        
        header_subtitle = tk.Label(header_frame, text="Theo dõi sức khỏe, tiêm phòng và lịch sử cân nặng", fg="#E0E7FF", bg=COLOR_PRIMARY, font=("Segoe UI", 9, "italic"))
        header_subtitle.pack(side=tk.LEFT, padx=10, pady=22)

        # Container chính
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # 2. Layout chính: trái = Danh sách thú cưng (co dãn), phải = Form (trên) + Dashboard (dưới)
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        # Cho phép hàng và cột co dãn
        content_frame.columnconfigure(0, weight=3)
        content_frame.columnconfigure(1, weight=1, minsize=360)
        content_frame.rowconfigure(0, weight=1)

        # Khu vực phải: chứa Form ở trên và Dashboard ở dưới
        right_panel = ttk.Frame(content_frame)
        right_panel.grid(row=0, column=1, sticky="nsew")
        # Right panel layout: form on row 0 (fixed), dashboard on row 1 (expandable)
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=0)
        right_panel.rowconfigure(1, weight=1)

        # --- PHẦN PHÍA TRÊN BÊN PHẢI: Dashboard (sẽ đặt dưới Form) ---
        dashboard_frame = ttk.Frame(right_panel)
        dashboard_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 0))
        
        # Thẻ Tổng số thú cưng
        card_total, total_content = self.create_card(dashboard_frame, title="TỔNG SỐ THÚ CƯNG", highlight_color=COLOR_PRIMARY)
        card_total.pack(fill=tk.X, pady=(0, 8))
        
        self.lbl_total = tk.Label(total_content, text="Tổng số thú cưng: 0", font=("Segoe UI", 13, "bold"), fg=TEXT_PRIMARY, bg=CARD_BG, anchor="w")
        self.lbl_total.pack(fill=tk.X)

        # Thẻ Tuổi trung bình
        card_avg, avg_content = self.create_card(dashboard_frame, title="TUỔI TRUNG BÌNH", highlight_color=COLOR_SUCCESS)
        card_avg.pack(fill=tk.X, pady=(0, 8))
        
        self.lbl_avg_age = tk.Label(avg_content, text="Tuổi trung bình: 0 năm", font=("Segoe UI", 13, "bold"), fg=TEXT_PRIMARY, bg=CARD_BG, anchor="w")
        self.lbl_avg_age.pack(fill=tk.X)

        # Thẻ Cảnh báo tiêm phòng
        card_warn, warn_content = self.create_card(dashboard_frame, title="⚠️ CẢNH BÁO TIÊM PHÒNG (TRONG 14 NGÀY)", highlight_color=COLOR_DANGER)
        card_warn.pack(fill=tk.BOTH, expand=True)

        list_frame = tk.Frame(warn_content, bg=CARD_BG)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        scrollbar_warn = ttk.Scrollbar(list_frame)
        scrollbar_warn.pack(side=tk.RIGHT, fill=tk.Y)

        self.warning_listbox = tk.Listbox(
            list_frame,
            height=3,
            fg="#B91C1C",
            bg="#FEF2F2",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            highlightthickness=0,
            selectbackground="#FCA5A5",
            yscrollcommand=scrollbar_warn.set
        )
        self.warning_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_warn.config(command=self.warning_listbox.yview)


        # Danh sách thú cưng đặt ở cột trái, co dãn theo chiều ngang và dọc
        pets_card, pets_content = self.create_card(content_frame, title="📋 DANH SÁCH THÚ CƯNG")
        pets_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Khung tìm kiếm nâng cao
        search_frame = tk.Frame(pets_content, bg=CARD_BG)
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        search_frame.columnconfigure(1, weight=1)
        search_frame.columnconfigure(3, weight=1)

        # 1. Từ khóa
        tk.Label(search_frame, text="🔍 Từ khóa:", font=("Segoe UI", 9, "bold"), fg=TEXT_SECONDARY, bg=CARD_BG).grid(row=0, column=0, padx=(0, 5), pady=5, sticky=tk.W)
        self.ent_search = ttk.Entry(search_frame)
        self.ent_search.grid(row=0, column=1, padx=(0, 15), pady=5, sticky="ew")

        # 2. Tiêu chí tìm kiếm (Tất cả, Tên, Loài, Trạng thái, Ngày sinh, Cân nặng, Hạn tiêm)
        tk.Label(search_frame, text="Tìm theo:", font=("Segoe UI", 9, "bold"), fg=TEXT_SECONDARY, bg=CARD_BG).grid(row=0, column=2, padx=(0, 5), pady=5, sticky=tk.W)
        self.search_criteria_options = ["Tất cả", "Tên", "Loài", "Trạng thái", "Ngày sinh", "Cân nặng", "Hạn tiêm"]
        self.cmb_search_criteria = ttk.Combobox(search_frame, values=self.search_criteria_options, state="readonly", width=12)
        self.cmb_search_criteria.grid(row=0, column=3, padx=(0, 15), pady=5, sticky="ew")
        self.cmb_search_criteria.current(0)

        # 3. Nút tìm kiếm nâng cao
        ttk.Button(
            search_frame,
            text="Tìm kiếm 🔍",
            style="Primary.TButton",
            command=self.search_pets
        ).grid(row=0, column=4, padx=(5, 0), pady=5, sticky="ew")

        # Khung các nút thao tác
        btn_frame = tk.Frame(pets_content, bg=CARD_BG)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        # Nút Thêm thú cưng di chuyển vào đây
        ttk.Button(
            btn_frame,
            text="➕ Thêm thú cưng",
            style="Primary.TButton",
            command=self.open_add_pet_window
        ).pack(side=tk.LEFT, padx=(0, 8))

        ttk.Button(
            btn_frame,
            text="✏️ Chỉnh sửa",
            style="Info.TButton",
            command=self.open_edit_window
        ).pack(side=tk.LEFT, padx=(0, 8))

        ttk.Button(
            btn_frame,
            text="🗑️ Xóa",
            style="Danger.TButton",
            command=self.delete_pet
        ).pack(side=tk.LEFT, padx=8)

        ttk.Button(
            btn_frame,
            text="📈 Lịch sử cân nặng",
            style="Primary.TButton",
            command=self.view_weight_history
        ).pack(side=tk.LEFT, padx=8)

        ttk.Button(
            btn_frame,
            text="📤 Xuất file báo cáo",
            style="Success.TButton",
            command=self.export_to_excel
        ).pack(side=tk.LEFT, padx=8)

        # Khung bảng Treeview kèm Scrollbar
        tree_container = tk.Frame(pets_content, bg=CARD_BG)
        tree_container.pack(fill=tk.BOTH, expand=True)

        scrollbar_tree = ttk.Scrollbar(tree_container)
        scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ('ID', 'Name', 'Species', 'DOB', 'Status', 'Weight', 'NextVac')
        self.tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show='headings',
            selectmode='browse',
            yscrollcommand=scrollbar_tree.set
        )
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_tree.config(command=self.tree.yview)
        self.tree.bind('<Double-1>', lambda event: self.open_edit_window())

        heading_map = {
            'ID': 'ID',
            'Name': 'Tên',
            'Species': 'Loài',
            'DOB': 'Ngày sinh',
            'Status': 'Trạng thái',
            'Weight': 'Cân nặng',
            'NextVac': 'Hạn tiêm tiếp'
        }

        # Thiết lập header và kích thước cột (dùng khoảng trắng nhất quán)
        for col in columns:
            self.tree.heading(col, text=heading_map.get(col, col))
            if col == 'ID':
                self.tree.column(col, width=60, anchor=tk.CENTER, stretch=False)
            elif col == 'Name':
                # Giảm `Name` xuống còn ~70% của giá trị trước (từ 180 -> ~126)
                self.tree.column(col, width=126, anchor=tk.W, stretch=True)
            elif col == 'Species':
                self.tree.column(col, width=140, anchor=tk.CENTER, stretch=False)
            elif col == 'DOB':
                self.tree.column(col, width=130, anchor=tk.CENTER, stretch=False)
            elif col == 'Status':
                self.tree.column(col, width=160, anchor=tk.CENTER, stretch=False)
            elif col == 'Weight':
                # Tăng độ rộng mặc định cho cột Cân nặng
                self.tree.column(col, width=150, anchor=tk.CENTER, stretch=False)
            elif col == 'NextVac':
                self.tree.column(col, width=160, anchor=tk.CENTER, stretch=False)

        # Tự động điều chỉnh độ rộng cột theo kích thước Treeview (Name ~50% cũ)
        proportions = {
            'ID': 0.084,
            'Name': 0.154,
            'Species': 0.167,
            'DOB': 0.139,
            'Status': 0.167,
            'Weight': 0.15,
            'NextVac': 0.139
        }

        def _auto_resize(event=None):
            try:
                total = self.tree.winfo_width()
                if total <= 0:
                    return
                for col, frac in proportions.items():
                    w = max(60, int(total * frac))
                    self.tree.column(col, width=w)
            except Exception:
                pass

        # Gắn sự kiện thay đổi kích thước của cửa sổ
        self.root.bind('<Configure>', _auto_resize)

        # Cấu hình màu cho dòng Treeview
        self.tree.tag_configure('evenrow', background='#FFFFFF')
        self.tree.tag_configure('oddrow', background='#F9FAFB')
        
        # Cấu hình màu sắc của chữ dựa trên trạng thái
        self.tree.tag_configure('status_khoe_manh', foreground='#059669', font=('Segoe UI', 10, 'bold'))
        self.tree.tag_configure('status_can_theo_doi', foreground='#D97706', font=('Segoe UI', 10, 'bold'))
        self.tree.tag_configure('status_dang_dieu_tri', foreground='#2563EB', font=('Segoe UI', 10, 'bold'))
        self.tree.tag_configure('status_bi_thuong', foreground='#DC2626', font=('Segoe UI', 10, 'bold'))

        # Thêm footer spacer (khoảng cách ~3 dòng) ở đáy để căn chỉnh giao diện
        footer_spacer = tk.Frame(self.root, height=48, bg=BG_COLOR)
        footer_spacer.pack(side=tk.BOTTOM, fill=tk.X)

    def open_add_pet_window(self):
        """Mở cửa sổ thêm thú cưng mới (form nằm trong cửa sổ riêng)."""
        win = tk.Toplevel(self.root)
        win.title("Thêm thú cưng mới")
        win.geometry("520x420")
        win.configure(bg=BG_COLOR)
        win.resizable(False, False)

        header = tk.Label(
            win,
            text="➕ Thêm thú cưng mới",
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 12, "bold")
        )
        header.pack(fill=tk.X, pady=(12, 8), padx=12)

        form_frame = tk.Frame(win, bg=CARD_BG, bd=0, highlightbackground=BORDER_COLOR, highlightthickness=1)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Tên thú cưng", style="FormLabel.TLabel").grid(row=0, column=0, padx=10, pady=8, sticky=tk.W)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=1, padx=10, pady=8, sticky="ew")

        ttk.Label(form_frame, text="Loài", style="FormLabel.TLabel").grid(row=1, column=0, padx=10, pady=8, sticky=tk.W)
        species_options = getattr(self, 'species_options', ["Chó", "Mèo", "Thỏ", "Chim", "Chuột"])
        species_combo = ttk.Combobox(form_frame, values=species_options, state="readonly")
        species_combo.grid(row=1, column=1, padx=10, pady=8, sticky="ew")
        species_combo.current(0)

        ttk.Label(form_frame, text="Ngày sinh", style="FormLabel.TLabel").grid(row=2, column=0, padx=10, pady=8, sticky=tk.W)
        dob_frame = tk.Frame(form_frame, bg=CARD_BG)
        dob_frame.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

        day_options = [str(i).zfill(2) for i in range(1, 32)]
        month_options = [str(i).zfill(2) for i in range(1, 13)]
        year_options = [str(i) for i in range(2000, datetime.today().year + 1)]

        dob_day = ttk.Combobox(dob_frame, values=day_options, width=5, state="readonly")
        dob_day.pack(side=tk.LEFT, padx=(0, 5))
        dob_day.current(0)

        dob_month = ttk.Combobox(dob_frame, values=month_options, width=5, state="readonly")
        dob_month.pack(side=tk.LEFT, padx=(0, 5))
        dob_month.current(0)

        dob_year = ttk.Combobox(dob_frame, values=year_options, width=7, state="readonly")
        dob_year.pack(side=tk.LEFT)
        dob_year.current(len(year_options) - 1)

        ttk.Label(form_frame, text="Tình trạng", style="FormLabel.TLabel").grid(row=3, column=0, padx=10, pady=8, sticky=tk.W)
        status_combo = ttk.Combobox(form_frame, values=["Khỏe mạnh", "Cần theo dõi", "Đang điều trị", "Bị thương"], state="readonly")
        status_combo.grid(row=3, column=1, padx=10, pady=8, sticky="ew")
        status_combo.current(0)

        ttk.Label(form_frame, text="Cân nặng (kg)", style="FormLabel.TLabel").grid(row=4, column=0, padx=10, pady=8, sticky=tk.W)
        weight_entry = ttk.Entry(form_frame)
        weight_entry.grid(row=4, column=1, padx=10, pady=8, sticky="ew")

        ttk.Label(form_frame, text="Hạn tiêm tiếp", style="FormLabel.TLabel").grid(row=5, column=0, padx=10, pady=8, sticky=tk.W)
        vac_frame = tk.Frame(form_frame, bg=CARD_BG)
        vac_frame.grid(row=5, column=1, padx=10, pady=8, sticky="ew")

        vac_day = ttk.Combobox(vac_frame, values=day_options, width=5, state="readonly")
        vac_day.pack(side=tk.LEFT, padx=(0, 5))
        vac_day.current(0)

        vac_month = ttk.Combobox(vac_frame, values=month_options, width=5, state="readonly")
        vac_month.pack(side=tk.LEFT, padx=(0, 5))
        vac_month.current(0)

        vac_year = ttk.Combobox(vac_frame, values=year_options, width=7, state="readonly")
        vac_year.pack(side=tk.LEFT)
        vac_year.current(len(year_options) - 1)

        action_frame = tk.Frame(win, bg=BG_COLOR)
        action_frame.pack(fill=tk.X, padx=12, pady=(0, 12))

        def submit_new_pet():
            name = name_entry.get().strip()
            species = species_combo.get()
            dob = f"{dob_year.get()}-{dob_month.get()}-{dob_day.get()}"
            status = status_combo.get()
            vac = f"{vac_year.get()}-{vac_month.get()}-{vac_day.get()}"

            if not validate_name(name):
                messagebox.showerror("Lỗi", "Tên thú cưng không được để trống và không được chứa số hoặc ký tự đặc biệt")
                return

            if not validate_date(dob):
                messagebox.showerror("Lỗi", "Ngày sinh không hợp lệ")
                return

            if species not in species_options:
                messagebox.showerror("Lỗi", "Loài phải thuộc danh sách hỗ trợ")
                return

            if not validate_date(vac):
                messagebox.showerror("Lỗi", "Ngày hẹn tiêm phòng tiếp theo không hợp lệ")
                return

            weight_text = weight_entry.get().strip()
            weight = None
            if weight_text:
                try:
                    weight = float(weight_text)
                except ValueError:
                    messagebox.showerror("Lỗi", "Cân nặng phải là số")
                    return
                if weight <= 0:
                    messagebox.showerror("Lỗi", "Cân nặng phải lớn hơn 0")
                    return

            new_pet_id = self.controller.add_pet(name, species, dob, status, vac)
            if weight is not None:
                today = datetime.today().strftime('%Y-%m-%d')
                self.controller.add_weight(new_pet_id, today, weight)

            self.refresh_data()
            win.destroy()
            messagebox.showinfo("Hoàn tất", f"Đã thêm thú cưng '{name}'")

        ttk.Button(action_frame, text="Thêm", style="Success.TButton", command=submit_new_pet).pack(side=tk.RIGHT)

    def refresh_data(self, pets=None):
        """Làm mới dữ liệu trên bảng và dashboard, hiển thị kết quả tìm kiếm nếu có."""
        for i in self.tree.get_children():
            self.tree.delete(i)

        if pets is None:
            pets = self.controller.get_pets()

        stats = self.controller.get_statistics()

        self.lbl_total.config(text=f"Tổng số thú cưng: {stats['total']}")
        self.lbl_avg_age.config(text=f"Tuổi trung bình: {stats['avg_age']} năm")

        self.warning_listbox.delete(0, tk.END)
        for warn in stats['warnings']:
            self.warning_listbox.insert(tk.END, warn)

        for idx, row in pets.reset_index(drop=True).iterrows():
            latest_weight = self.controller.get_latest_weight(row['ID'])
            
            # Phân bổ sọc hàng xen kẽ
            bg_tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            
            # Áp dụng màu sắc chữ theo trạng thái sức khỏe
            status = row['Status']
            status_tag = 'status_khoe_manh'
            if status == "Cần theo dõi":
                status_tag = 'status_can_theo_doi'
            elif status == "Đang điều trị":
                status_tag = 'status_dang_dieu_tri'
            elif status == "Bị thương":
                status_tag = 'status_bi_thuong'

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
                ),
                tags=(bg_tag, status_tag)
            )

    def get_selected_pet(self):
        """Trả về dữ liệu của thú cưng đang được chọn trên bảng."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một thú cưng từ danh sách!")
            return None

        item = self.tree.item(selected[0])
        return item['values']

    def delete_pet(self):
        """Xóa thú cưng đã chọn khỏi danh sách và cập nhật giao diện."""
        pet = self.get_selected_pet()
        if not pet:
            return

        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa thú cưng '{pet[1]}' khỏi hệ thống không?")
        if not confirm:
            return

        self.controller.delete_pet(pet[0])
        self.refresh_data()

    def add_weight(self):
        """Ghi nhận cân nặng mới cho thú cưng đang được chọn."""
        pet = self.get_selected_pet()
        if not pet:
            return
        # Nếu không có ô nhập cân nặng trên main window, mở prompt để nhập
        if hasattr(self, 'ent_weight'):
            weight_text = self.ent_weight.get().strip()
        else:
            weight_text = simpledialog.askstring("Cân nặng", "Nhập cân nặng (kg):", parent=self.root)

        if not weight_text:
            messagebox.showerror("Lỗi", "Vui lòng nhập cân nặng!")
            return

        try:
            weight = float(weight_text)
        except ValueError:
            messagebox.showerror("Lỗi", "Cân nặng phải là số!")
            return

        if weight <= 0:
            messagebox.showerror("Lỗi", "Cân nặng phải lớn hơn 0!")
            return

        date = datetime.today().strftime('%Y-%m-%d')
        self.controller.add_weight(pet[0], date, weight)
        if hasattr(self, 'ent_weight'):
            self.ent_weight.delete(0, tk.END)
        self.refresh_data()

    def open_edit_window(self):
        """Mở một cửa sổ mới để chỉnh sửa thông tin thú cưng được chọn."""
        pet = self.get_selected_pet()
        if not pet:
            return

        edit_win = tk.Toplevel(self.root)
        edit_win.title(f"Chỉnh sửa thông tin: {pet[1]}")
        edit_win.geometry("520x460")
        edit_win.configure(bg=BG_COLOR)
        edit_win.resizable(False, False)

        header = tk.Label(
            edit_win,
            text=f"✏️ Chỉnh sửa thông tin thú cưng: {pet[1]}",
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 12, "bold")
        )
        header.pack(fill=tk.X, pady=(15, 8), padx=15)

        form_frame = tk.Frame(edit_win, bg=CARD_BG, bd=0, highlightbackground=BORDER_COLOR, highlightthickness=1)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Tên thú cưng", style="FormLabel.TLabel").grid(row=0, column=0, padx=10, pady=8, sticky=tk.W)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
        name_entry.insert(0, pet[1])

        ttk.Label(form_frame, text="Loài", style="FormLabel.TLabel").grid(row=1, column=0, padx=10, pady=8, sticky=tk.W)
        species_options = getattr(self, 'species_options', ["Chó", "Mèo", "Thỏ", "Chim", "Chuột"])
        species_combo = ttk.Combobox(form_frame, values=species_options, state="readonly")
        species_combo.grid(row=1, column=1, padx=10, pady=8, sticky="ew")
        species_combo.set(pet[2] if pet[2] in species_options else species_options[0])

        ttk.Label(form_frame, text="Ngày sinh", style="FormLabel.TLabel").grid(row=2, column=0, padx=10, pady=8, sticky=tk.W)
        dob_frame = tk.Frame(form_frame, bg=CARD_BG)
        dob_frame.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

        day_options = [str(i).zfill(2) for i in range(1, 32)]
        month_options = [str(i).zfill(2) for i in range(1, 13)]
        year_options = [str(i) for i in range(2000, datetime.today().year + 1)]

        dob_day = ttk.Combobox(dob_frame, values=day_options, width=5, state="readonly")
        dob_day.pack(side=tk.LEFT, padx=(0, 5))
        dob_month = ttk.Combobox(dob_frame, values=month_options, width=5, state="readonly")
        dob_month.pack(side=tk.LEFT, padx=(0, 5))
        dob_year = ttk.Combobox(dob_frame, values=year_options, width=7, state="readonly")
        dob_year.pack(side=tk.LEFT)

        dob_parts = str(pet[3]).split('-')
        if len(dob_parts) == 3:
            dob_year.set(dob_parts[0])
            dob_month.set(dob_parts[1])
            dob_day.set(dob_parts[2])
        else:
            dob_day.current(0)
            dob_month.current(0)
            dob_year.current(len(year_options) - 1)

        ttk.Label(form_frame, text="Tình trạng", style="FormLabel.TLabel").grid(row=3, column=0, padx=10, pady=8, sticky=tk.W)
        status_combo = ttk.Combobox(form_frame, values=["Khỏe mạnh", "Cần theo dõi", "Đang điều trị", "Bị thương"], state="readonly")
        status_combo.grid(row=3, column=1, padx=10, pady=8, sticky="ew")
        status_combo.set(pet[4])

        ttk.Label(form_frame, text="Cân nặng (kg)", style="FormLabel.TLabel").grid(row=4, column=0, padx=10, pady=8, sticky=tk.W)
        latest_weight = self.controller.get_latest_weight(pet[0])
        weight_value = "" if latest_weight == "Chưa có" else str(latest_weight).replace(' kg', '')
        weight_entry = ttk.Entry(form_frame)
        weight_entry.grid(row=4, column=1, padx=10, pady=8, sticky="ew")
        weight_entry.insert(0, weight_value)

        ttk.Label(form_frame, text="Hạn tiêm tiếp", style="FormLabel.TLabel").grid(row=5, column=0, padx=10, pady=8, sticky=tk.W)
        vac_frame = tk.Frame(form_frame, bg=CARD_BG)
        vac_frame.grid(row=5, column=1, padx=10, pady=8, sticky="ew")

        vac_day = ttk.Combobox(vac_frame, values=day_options, width=5, state="readonly")
        vac_day.pack(side=tk.LEFT, padx=(0, 5))
        vac_month = ttk.Combobox(vac_frame, values=month_options, width=5, state="readonly")
        vac_month.pack(side=tk.LEFT, padx=(0, 5))
        vac_year = ttk.Combobox(vac_frame, values=year_options, width=7, state="readonly")
        vac_year.pack(side=tk.LEFT)

        vac_parts = str(pet[6]).split('-')
        if len(vac_parts) == 3:
            vac_year.set(vac_parts[0])
            vac_month.set(vac_parts[1])
            vac_day.set(vac_parts[2])
        else:
            vac_day.current(0)
            vac_month.current(0)
            vac_year.current(len(year_options) - 1)

        action_frame = tk.Frame(edit_win, bg=BG_COLOR)
        action_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        def save_changes():
            name = name_entry.get().strip()
            species = species_combo.get()
            dob = f"{dob_year.get()}-{dob_month.get()}-{dob_day.get()}"
            status = status_combo.get()
            vac = f"{vac_year.get()}-{vac_month.get()}-{vac_day.get()}"

            if not validate_name(name):
                messagebox.showerror("Lỗi", "Tên thú cưng không được để trống và không được chứa số hoặc ký tự đặc biệt")
                return

            if not validate_date(dob):
                messagebox.showerror("Lỗi", "Ngày sinh không hợp lệ")
                return

            species_options = getattr(self, 'species_options', ["Chó", "Mèo", "Thỏ", "Chim", "Chuột"])
            if species not in species_options:
                messagebox.showerror("Lỗi", "Loài phải thuộc danh sách hỗ trợ")
                return

            if not validate_date(vac):
                messagebox.showerror("Lỗi", "Ngày hẹn tiêm phòng tiếp theo không hợp lệ")
                return

            weight_value = weight_entry.get().strip()
            if weight_value:
                try:
                    weight_val = float(weight_value)
                except ValueError:
                    messagebox.showerror("Lỗi", "Cân nặng phải là số")
                    return
                if weight_val <= 0:
                    messagebox.showerror("Lỗi", "Cân nặng phải lớn hơn 0")
                    return
                weight_date = datetime.today().strftime('%Y-%m-%d')
                self.controller.add_weight(pet[0], weight_date, weight_val)

            self.controller.update_pet(pet[0], name, species, dob, status, vac)
            self.refresh_data()
            edit_win.destroy()
            messagebox.showinfo("Hoàn tất", f"Đã cập nhật thông tin cho '{name}'")

        ttk.Button(
            action_frame,
            text="Lưu thay đổi",
            style="Success.TButton",
            command=save_changes
        ).pack(side=tk.RIGHT)

    def search_pets(self):
        """Tìm kiếm thú cưng nâng cao và cập nhật bảng kết quả."""
        import pandas as pd
        query = self.ent_search.get().strip()
        criteria = self.cmb_search_criteria.get()

        # Lấy tất cả thú cưng ban đầu
        pets = self.controller.get_pets()
        if pets.empty:
            self.refresh_data(pets)
            return

        # Thêm cột cân nặng mới nhất để hỗ trợ tìm kiếm cân nặng
        pets['LatestWeight'] = pets['ID'].apply(lambda pid: self.controller.get_latest_weight(pid))

        # Hàm chuẩn hóa văn bản tiếng Việt để tìm kiếm không dấu
        def normalize_text(text):
            import unicodedata
            text = str(text)
            normalized = unicodedata.normalize('NFKD', text)
            return ''.join(ch for ch in normalized if not unicodedata.combining(ch)).lower()

        mask = pd.Series(True, index=pets.index)

        # Lọc theo Từ khóa dựa trên Tiêu chí Tìm kiếm
        if query:
            query_normalized = normalize_text(query)
            if criteria == "Tên":
                mask &= pets['Name'].astype(str).apply(normalize_text).str.contains(query_normalized)
            elif criteria == "Loài":
                mask &= pets['Species'].astype(str).apply(normalize_text).str.contains(query_normalized)
            elif criteria == "Trạng thái":
                mask &= pets['Status'].astype(str).apply(normalize_text).str.contains(query_normalized)
            elif criteria == "Ngày sinh":
                mask &= pets['DOB'].astype(str).apply(normalize_text).str.contains(query_normalized)
            elif criteria == "Cân nặng":
                mask &= pets['LatestWeight'].astype(str).apply(normalize_text).str.contains(query_normalized)
            elif criteria == "Hạn tiêm":
                mask &= pets['NextVaccinationDate'].astype(str).apply(normalize_text).str.contains(query_normalized)
            else:  # "Tất cả" - khớp trên mọi cột (kể cả ID, Tên, Loài, Ngày sinh, Trạng thái, Ngày tiêm, Cân nặng)
                all_match = pd.Series(False, index=pets.index)
                for col in pets.columns:
                    col_match = pets[col].astype(str).apply(normalize_text).str.contains(query_normalized)
                    all_match |= col_match
                mask &= all_match

        filtered_pets = pets[mask]
        self.refresh_data(filtered_pets)

    def view_weight_history(self):
        """Hiển thị cửa sổ lịch sử và xu hướng cân nặng được thiết kế cực đẹp bằng bảng biểu Treeview."""
        pet = self.get_selected_pet()
        if not pet:
            return

        history = self.controller.get_weight_history(pet[0])

        win = tk.Toplevel(self.root)
        win.title(f"Lịch sử & Xu hướng cân nặng của {pet[1]}")
        win.geometry("560x520")
        win.configure(bg=BG_COLOR)
        win.resizable(False, False)

        # Tiêu đề cửa sổ
        title_lbl = tk.Label(
            win,
            text=f"📊 Cân Nặng & Xu Hướng của {pet[1]}",
            font=("Segoe UI", 12, "bold"),
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        )
        title_lbl.pack(pady=12)

        # 1. Thẻ Lịch sử chi tiết
        hist_card = tk.Frame(win, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightcolor=BORDER_COLOR, highlightthickness=1, bd=0)
        hist_card.pack(fill=tk.BOTH, expand=True, padx=15, pady=6)
        
        lbl_hist = tk.Label(hist_card, text="⏱️ Lịch sử các lần ghi nhận", font=("Segoe UI", 10, "bold"), bg=CARD_BG, fg=TEXT_SECONDARY, anchor="w")
        lbl_hist.pack(fill=tk.X, padx=12, pady=(10, 4))
        
        hist_frame = tk.Frame(hist_card, bg=CARD_BG)
        hist_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 10))
        
        scroll_hist = ttk.Scrollbar(hist_frame)
        scroll_hist.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_hist = ttk.Treeview(hist_frame, columns=('Date', 'Weight'), show='headings', height=5, yscrollcommand=scroll_hist.set)
        tree_hist.heading('Date', text='Ngày đo')
        tree_hist.heading('Weight', text='Cân nặng (kg)')
        tree_hist.column('Date', width=220, anchor=tk.CENTER)
        tree_hist.column('Weight', width=220, anchor=tk.CENTER)
        tree_hist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_hist.config(command=tree_hist.yview)
        
        # Nạp dữ liệu lịch sử
        if history.empty:
            tree_hist.insert('', tk.END, values=("Chưa có dữ liệu cân nặng nào", "-"))
        else:
            for idx, row in history.reset_index(drop=True).iterrows():
                bg_tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                tree_hist.insert('', tk.END, values=(row['Date'].strftime('%Y-%m-%d'), f"{row['Weight']} kg"), tags=(bg_tag,))
                
        # 2. Thẻ Xu hướng trung bình theo tháng
        trend_card = tk.Frame(win, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightcolor=BORDER_COLOR, highlightthickness=1, bd=0)
        trend_card.pack(fill=tk.BOTH, expand=True, padx=15, pady=(6, 15))
        
        lbl_trend = tk.Label(trend_card, text="📉 Trung bình cân nặng hàng tháng", font=("Segoe UI", 10, "bold"), bg=CARD_BG, fg=TEXT_SECONDARY, anchor="w")
        lbl_trend.pack(fill=tk.X, padx=12, pady=(10, 4))
        
        trend_frame = tk.Frame(trend_card, bg=CARD_BG)
        trend_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 10))
        
        scroll_trend = ttk.Scrollbar(trend_frame)
        scroll_trend.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_trend = ttk.Treeview(trend_frame, columns=('Month', 'AvgWeight'), show='headings', height=4, yscrollcommand=scroll_trend.set)
        tree_trend.heading('Month', text='Tháng')
        tree_trend.heading('AvgWeight', text='Cân nặng trung bình')
        tree_trend.column('Month', width=220, anchor=tk.CENTER)
        tree_trend.column('AvgWeight', width=220, anchor=tk.CENTER)
        tree_trend.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_trend.config(command=tree_trend.yview)
        
        # Nạp dữ liệu xu hướng
        trend = self.controller.get_monthly_weight_trend(pet[0])
        if trend.empty:
            tree_trend.insert('', tk.END, values=("Chưa đủ dữ liệu tháng để tổng hợp", "-"))
        else:
            for idx, row in trend.reset_index(drop=True).iterrows():
                bg_tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                tree_trend.insert('', tk.END, values=(row['Month'], f"{row['Weight']} kg"), tags=(bg_tag,))
                
        # Cấu hình các style bổ sung cho bảng con
        tree_hist.tag_configure('evenrow', background='#FFFFFF')
        tree_hist.tag_configure('oddrow', background='#F9FAFB')
        tree_trend.tag_configure('evenrow', background='#FFFFFF')
        tree_trend.tag_configure('oddrow', background='#F9FAFB')

    def export_to_excel(self):
        """Xuất dữ liệu thú cưng ra file Excel hoặc CSV thông qua hộp thoại chọn vị trí lưu."""
        try:
            import pandas as pd
        except Exception:
            messagebox.showerror(
                "Lỗi",
                "Cần cài đặt thư viện pandas và openpyxl để xuất báo cáo.\nChạy: pip install pandas openpyxl"
            )
            return

        pets = self.controller.get_pets()

        if pets is None or pets.empty:
            messagebox.showinfo("Thông báo", "Không có dữ liệu thú cưng để xuất!")
            return

        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[
                ("Excel Files (*.xlsx)", "*.xlsx"),
                ("CSV Files (*.csv)", "*.csv"),
                ("All Files (*.*)", "*.*")
            ],
            initialfile="Danh_sach_thu_cung.xlsx",
            title="Chọn nơi lưu file báo cáo"
        )

        if not file_path:
            return

        df = pets.copy()
        df['LatestWeight'] = df['ID'].apply(lambda pid: self.controller.get_latest_weight(pid))

        # Đổi tên cột sang tiếng Việt chuyên nghiệp
        df.rename(columns={
            'ID': 'Mã Thú Cưng',
            'Name': 'Tên Thú Cưng',
            'Species': 'Loài',
            'DOB': 'Ngày Sinh',
            'Status': 'Trạng Thái Sức Khỏe',
            'NextVaccinationDate': 'Hạn Tiêm Tiếp Theo',
            'LatestWeight': 'Cân Nặng Mới Nhất'
        }, inplace=True)

        try:
            path_ext = Path(file_path).suffix.lower()
            if path_ext == ".csv":
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
                messagebox.showinfo("Hoàn tất 🎉", f"Đã xuất file báo cáo CSV thành công tại:\n{file_path}")
            else:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Hoàn tất 🎉", f"Đã xuất file báo cáo Excel thành công tại:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file báo cáo: {e}")
