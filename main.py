import tkinter as tk
from views.gui_view import PetApp

# Entry point của ứng dụng: khởi tạo cửa sổ chính và chạy giao diện.
if __name__ == "__main__":

    root = tk.Tk()

    app = PetApp(root)

    root.mainloop()