# project/ui/main_window.py
import tkinter as tk
from tkinter import ttk
from .canvas import GraphCanvas
from utils.constants import *

# === CẤU HÌNH GIAO DIỆN MỚI (TO HƠN & THOÁNG HƠN) ===
BUTTON_FONT = ("Segoe UI", 11, "bold") # Tăng size chữ lên 11
BTN_CONFIG = {
    "font": BUTTON_FONT,
    "relief": tk.RAISED,
    "bd": 1,              # Viền mỏng (1px) -> Trông phẳng và đỡ thô cứng hơn
    "padx": 20,           # Tăng chiều rộng nút (cho thoáng)
    "pady": 8,            # Tăng chiều cao nút
    "activebackground": "#dcdcdc",
    "cursor": "hand2"     # Thêm con trỏ tay khi di chuột vào nút
}

class MainWindow(tk.Tk):
    def __init__(self, controller_class, graph_model):
        super().__init__()
        self.title("Graph Visualization Tool - Final Interface")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.model = graph_model
        self.mode_buttons = {}

        # Toolbar: Tăng padding để thanh công cụ thoáng hơn
        self.toolbar = tk.Frame(self, bd=1, relief=tk.FLAT, bg="#f0f0f0", pady=8)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.status_label = tk.Label(self, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Segoe UI", 9))
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas_area = GraphCanvas(self)
        self.canvas_area.pack(fill=tk.BOTH, expand=True)

        self.controller = controller_class(self.model, self)
        self.canvas_area.set_controller(self.controller)

        self._create_toolbar_buttons()
        self._create_context_panels()

        self.update_active_button(MODE_MOVE)
        self.update_context_toolbar(MODE_MOVE)

    def _create_toolbar_buttons(self):
        # --- Group 1: File Menu (GỘP NEW & SAVE VÀO ĐÂY) ---
        # 1. Tạo nút Menu "File"
        mb_file = tk.Menubutton(self.toolbar, text="File", bg="#ecf0f1", **BTN_CONFIG)
        mb_file.pack(side=tk.LEFT, padx=5)

        # 2. Tạo danh sách menu xổ xuống
        file_menu = tk.Menu(mb_file, tearoff=0, font=("Segoe UI", 10))

        # 3. Thêm các mục vào menu
        file_menu.add_command(label="New Graph", command=self.controller.clear_graph)
        file_menu.add_separator() # Kẻ đường ngang ngăn cách
        file_menu.add_command(label="Save Graph", command=self.controller.save_graph)

        # 4. Gán menu vào nút File
        mb_file.config(menu=file_menu)

        # Vách ngăn
        tk.Label(self.toolbar, text="|", font=("Arial", 14), bg="#f0f0f0", fg="#bdc3c7").pack(side=tk.LEFT, padx=10)

        # --- Group 2: Tools (Move, Add, Connect, Remove) ---
        # 1. Move
        btn_move = tk.Button(self.toolbar, text="Move",
                             command=lambda: self.controller.set_mode(MODE_MOVE),
                             **BTN_CONFIG)
        btn_move.pack(side=tk.LEFT, padx=4)
        self.mode_buttons[MODE_MOVE] = btn_move

        # 2. Add Vertex
        btn_add = tk.Button(self.toolbar, text="Add Vertex",
                            command=lambda: self.controller.set_mode(MODE_ADD_VERTEX),
                            **BTN_CONFIG)
        btn_add.pack(side=tk.LEFT, padx=4)
        self.mode_buttons[MODE_ADD_VERTEX] = btn_add

        # 3. Connect
        btn_conn = tk.Button(self.toolbar, text="Connect",
                             command=lambda: self.controller.set_mode(MODE_ADD_EDGE),
                             **BTN_CONFIG)
        btn_conn.pack(side=tk.LEFT, padx=4)
        self.mode_buttons[MODE_ADD_EDGE] = btn_conn

        # 4. Remove
        btn_rem = tk.Button(self.toolbar, text="Remove",
                            command=lambda: self.controller.set_mode(MODE_REMOVE),
                            **BTN_CONFIG)
        btn_rem.pack(side=tk.LEFT, padx=4)
        self.mode_buttons[MODE_REMOVE] = btn_rem

        # --- Group 3: UNDO ---
        btn_undo = tk.Button(self.toolbar, text="Undo", command=self.controller.undo,
                             bg="#ecf0f1", **BTN_CONFIG)
        btn_undo.pack(side=tk.LEFT, padx=(15, 5))

        # Vách ngăn cuối
        tk.Label(self.toolbar, text="|", font=("Arial", 14), bg="#f0f0f0", fg="#bdc3c7").pack(side=tk.LEFT, padx=10)
    def _create_context_panels(self):
        # Cập nhật style cho các panel con để đồng bộ

        # --- Panel 1: Enum ---
        self.vertex_settings_frame = tk.Frame(self.toolbar, bg="#f0f0f0")
        tk.Label(self.vertex_settings_frame, text="Enum:", font=BUTTON_FONT, bg="#f0f0f0").pack(side=tk.LEFT, padx=2)

        self.enum_var = tk.StringVar()
        self.enum_combo = ttk.Combobox(self.vertex_settings_frame, textvariable=self.enum_var,
                                       state="readonly", width=10, font=("Segoe UI", 10))
        self.enum_combo['values'] = ("1, 2, 3...", "0, 1, 2...", "A, B, C...")
        self.enum_combo.current(0)
        self.enum_combo.bind("<<ComboboxSelected>>", self.controller.change_naming_mode)
        self.enum_combo.pack(side=tk.LEFT, padx=5, pady=5)

        # --- Panel 2: Checkbox ---
        self.edge_settings_frame = tk.Frame(self.toolbar, bg="#f0f0f0")
        chk_directed = tk.Checkbutton(self.edge_settings_frame, text="Directed", font=BUTTON_FONT, bg="#f0f0f0",
                                      variable=tk.BooleanVar(value=False),
                                      command=self.controller.toggle_directed)
        chk_directed.pack(side=tk.LEFT, padx=5)

        self.is_weighted_var = tk.BooleanVar(value=True)
        chk_weighted = tk.Checkbutton(self.edge_settings_frame, text="Weighted", font=BUTTON_FONT, bg="#f0f0f0",
                                      variable=self.is_weighted_var)
        chk_weighted.pack(side=tk.LEFT, padx=5)

        # --- Panel 3: Clear All ---
        self.remove_settings_frame = tk.Frame(self.toolbar, bg="#f0f0f0")
        btn_clear = tk.Button(self.remove_settings_frame, text="CLEAR ALL",
                              bg="#e74c3c", fg="white",
                              command=self.controller.clear_graph,
                              **BTN_CONFIG) # Dùng chung config cho đẹp
        btn_clear.pack(side=tk.LEFT, padx=5)

    def update_context_toolbar(self, mode):
        self.vertex_settings_frame.pack_forget()
        self.edge_settings_frame.pack_forget()
        self.remove_settings_frame.pack_forget()

        if mode == MODE_ADD_VERTEX:
            self.vertex_settings_frame.pack(side=tk.LEFT, padx=5)
        elif mode == MODE_ADD_EDGE:
            self.edge_settings_frame.pack(side=tk.LEFT, padx=5)
        elif mode == MODE_REMOVE:
            self.remove_settings_frame.pack(side=tk.LEFT, padx=5)

    def update_active_button(self, active_mode):
        for mode, btn in self.mode_buttons.items():
            if mode == active_mode:
                # Nút đang chọn: Xanh lá, chữ trắng, chìm xuống (SUNKEN)
                btn.config(bg=BUTTON_BG_ACTIVE, fg=BUTTON_TEXT_ACTIVE, relief=tk.SUNKEN)
            else:
                # Nút bình thường: Xám nhạt, chữ đen, nổi lên (RAISED)
                btn.config(bg=BUTTON_BG_DEFAULT, fg=BUTTON_TEXT_DEFAULT, relief=tk.RAISED)

    def update_status(self, message):
        self.status_label.config(text=message)
