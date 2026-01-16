# project/controller/graph_controller.py

import tkinter.font as tkfont # <--- THÊM DÒNG QUAN TRỌNG NÀY
from utils.constants import *
import tkinter as tk  # <--- THÊM DÒNG NÀY (QUAN TRỌNG)
from utils.constants import *
from utils.helpers import is_point_in_circle
import tkinter.messagebox as messagebox
# import tkinter.simpledialog as simpledialog  <-- CÓ THỂ BỎ DÒNG NÀY VÌ KHÔNG DÙNG NỮA

class GraphController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_mode = MODE_ADD_VERTEX
        self.selected_vertex_id = None
        self.dragged_vertex = None

        # === MỚI: Stack để lưu các trạng thái cho Undo ===
        self.undo_stack = []

    # === MỚI: Các hàm quản lý Undo ===
    def save_state(self):
        """Lưu trạng thái hiện tại của đồ thị vào stack."""
        state = self.model.get_state()
        self.undo_stack.append(state)
        # Giới hạn số lần undo (ví dụ: 20 lần) để tránh tốn bộ nhớ
        if len(self.undo_stack) > 20:
            self.undo_stack.pop(0)

    def undo(self):
        """Quay lại trạng thái trước đó."""
        if self.undo_stack:
            # Lấy trạng thái gần nhất
            last_state = self.undo_stack.pop()
            # Khôi phục model
            self.model.restore_state(last_state)
            # Vẽ lại
            self.view.canvas_area.redraw(self.model)
            self.view.update_status("Undid last action.")
        else:
            self.view.update_status("Nothing to undo.")

    # ... (Các hàm set_mode, change_naming_mode giữ nguyên) ...
    def set_mode(self, mode):
        self.current_mode = mode
        self.selected_vertex_id = None
        self.dragged_vertex = None
        self.view.update_status(f"Mode: {mode}")
        self.view.update_active_button(mode)
        self.view.update_context_toolbar(mode)
        self.view.canvas_area.redraw(self.model)

    def change_naming_mode(self, event):
        mode = self.view.enum_combo.get()
        self.model.set_naming_mode(mode)
        self.view.update_status(f"Naming mode changed to: {mode}")

    def clear_graph(self):
        if messagebox.askyesno("Confirm", "Create new graph?"):
            # Lưu trạng thái trước khi xóa sạch
            self.save_state()
            self.model.clear()
            self.view.canvas_area.redraw(self.model)
            self.view.update_status("Graph cleared.")
            self.set_mode(MODE_ADD_VERTEX)

    # ... (Hàm save_graph giữ nguyên) ...
    def save_graph(self):
        print("--- SAVING GRAPH ---")
        data_to_save = {
            "vertices": [{"id": v.id, "x": v.x, "y": v.y, "label": v.label} for v in self.model.vertices.values()],
            "edges": [{"start": e.start_vertex.id, "end": e.end_vertex.id, "weight": e.weight} for e in self.model.edges]
        }
        print("Data:", data_to_save)
        messagebox.showinfo("Save", "Check console for graph data structure.")

    # === CẬP NHẬT LOGIC CHUỘT ĐỂ GỌI save_state() ===
    def handle_click_press(self, x, y):
        clicked_vertex = self._get_vertex_at(x, y)

        if self.current_mode == MODE_MOVE:
            if clicked_vertex:
                # Lưu trạng thái TRƯỚC KHI bắt đầu di chuyển
                self.save_state()
                self.dragged_vertex = clicked_vertex
                self.view.update_status(f"Moving vertex {clicked_vertex.label}...")

        elif self.current_mode == MODE_ADD_VERTEX:
            if clicked_vertex is None:
                # Lưu trạng thái TRƯỚC KHI thêm đỉnh
                self.save_state()
                self.model.add_vertex(x, y)
                self.view.canvas_area.redraw(self.model)

        elif self.current_mode == MODE_ADD_EDGE:
            if clicked_vertex:
                if self.selected_vertex_id is None:
                    # Click lần 1: Chọn đỉnh đầu
                    self.selected_vertex_id = clicked_vertex.id
                else:
                    # Click lần 2: Chọn đỉnh đích
                    if self.selected_vertex_id != clicked_vertex.id:
                        is_weighted = self.view.is_weighted_var.get()
                        weight_value = None

                        if is_weighted:
                            # === SỬA TẠI ĐÂY: Dùng hộp thoại Custom to đẹp ===
                            # Gọi hàm _ask_weight_custom mà ta vừa viết
                            w_input = self._ask_weight_custom()

                            if w_input is not None:
                                weight_value = w_input
                            else:
                                # Nếu người dùng ấn Cancel -> Hủy nối
                                self.selected_vertex_id = None
                                self.view.canvas_area.redraw(self.model, self.selected_vertex_id)
                                return

                        # Lưu trạng thái TRƯỚC KHI nối cạnh
                        self.save_state()
                        self.model.add_edge(self.selected_vertex_id, clicked_vertex.id, weight_value)

                    self.selected_vertex_id = None
            else:
                self.selected_vertex_id = None
            self.view.canvas_area.redraw(self.model, self.selected_vertex_id)

        elif self.current_mode == MODE_REMOVE:
            if clicked_vertex:
                # Lưu trạng thái TRƯỚC KHI xóa đỉnh
                self.save_state()
                self.model.remove_vertex(clicked_vertex.id)
                self.view.canvas_area.redraw(self.model)

    # ... (Các hàm còn lại giữ nguyên) ...
    def handle_drag(self, x, y):
        if self.current_mode == MODE_MOVE and self.dragged_vertex:
            self.dragged_vertex.x = x
            self.dragged_vertex.y = y
            self.view.canvas_area.redraw(self.model)

    def handle_click_release(self, x, y):
        if self.current_mode == MODE_MOVE and self.dragged_vertex:
            self.dragged_vertex = None

    def _get_vertex_at(self, x, y):
        for v_id, vertex in reversed(list(self.model.vertices.items())):
            if is_point_in_circle(x, y, vertex.x, vertex.y, VERTEX_RADIUS):
                return vertex
        return None

    def toggle_directed(self):
        self.model.is_directed = not self.model.is_directed
        for edge in self.model.edges:
            edge.is_directed = self.model.is_directed
        self.view.canvas_area.redraw(self.model)
# === HÀM TẠO HỘP THOẠI NHẬP TRỌNG SỐ TO & ĐẸP ===
# === THAY THẾ TOÀN BỘ HÀM NÀY ===
# === DÙNG HÀM NÀY ĐỂ KHẮC PHỤC LỖI FONT ===
    def _ask_weight_custom(self):
        """Tự tạo hộp thoại nhập số liệu kích thước lớn"""
        dialog = tk.Toplevel(self.view)
        dialog.title("Weight")
        dialog.geometry("350x250")
        dialog.resizable(False, False)

        # Căn giữa màn hình
        x = self.view.winfo_x() + (self.view.winfo_width() // 2) - 175
        y = self.view.winfo_y() + (self.view.winfo_height() // 2) - 125
        dialog.geometry(f"+{x}+{y}")

        # Label tiêu đề
        lbl = tk.Label(dialog, text="Enter Weight:", font=("Segoe UI", 14, "bold"))
        lbl.pack(pady=(20, 10))

        # === PHẦN SỬA LỖI QUAN TRỌNG ===
        # 1. Tạo đối tượng Font riêng biệt, size 30 siêu to
        large_font = tkfont.Font(family="Helvetica", size=30, weight="bold")

        # 2. Gán font này vào Entry
        var = tk.StringVar(value="1")
        entry = tk.Entry(dialog, textvariable=var,
                         font=large_font,   # Dùng biến font vừa tạo
                         width=6, justify='center',
                         bd=2, relief=tk.SUNKEN)

        # 3. Pack không dùng ipady để tránh giãn con trỏ ảo
        entry.pack(pady=10)

        # Bôi đen số mặc định
        entry.select_range(0, tk.END)
        entry.focus_set()

        result = {"value": None}

        def on_ok(event=None):
            try:
                text_val = var.get()
                if not text_val: raise ValueError # Chặn ô trống
                val = int(text_val)
                if val < 0: raise ValueError
                result["value"] = val
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.", parent=dialog)

        dialog.bind('<Return>', on_ok)
        dialog.bind('<Escape>', lambda e: dialog.destroy())

        # Nút bấm
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)

        btn_ok = tk.Button(btn_frame, text="OK", command=on_ok,
                           font=("Segoe UI", 11, "bold"), width=10,
                           bg="#2ecc71", fg="white", relief=tk.RAISED, bd=2)
        btn_ok.pack(side=tk.LEFT, padx=10)

        btn_cancel = tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                               font=("Segoe UI", 11), width=10)
        btn_cancel.pack(side=tk.LEFT, padx=10)

        dialog.transient(self.view)
        dialog.grab_set()
        self.view.wait_window(dialog)

        return result["value"]
