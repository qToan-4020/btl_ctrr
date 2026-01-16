# project/ui/canvas.py
import tkinter as tk
from utils.constants import *
import math

class GraphCanvas(tk.Canvas):
    # ... (Giữ nguyên __init__, set_controller, các hàm event handle...)
    def __init__(self, master, controller_ref=None, **kwargs):
        super().__init__(master, bg=CANVAS_BG_COLOR, **kwargs)
        self.controller = controller_ref
        self.bind("<Button-1>", self.on_click_press)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_click_release)

    def set_controller(self, controller):
        self.controller = controller

    def on_click_press(self, event):
        if self.controller: self.controller.handle_click_press(event.x, event.y)
    def on_drag(self, event):
        if self.controller: self.controller.handle_drag(event.x, event.y)
    def on_click_release(self, event):
        if self.controller: self.controller.handle_click_release(event.x, event.y)

    def redraw(self, graph_model, selected_vertex_id=None):
        self.delete("all")
        for edge in graph_model.edges:
            self._draw_edge(edge)
        for v_id, vertex in graph_model.vertices.items():
            is_selected = (v_id == selected_vertex_id)
            self._draw_vertex(vertex, is_selected)

    def _draw_vertex(self, vertex, is_selected):
        x, y = vertex.x, vertex.y
        r = VERTEX_RADIUS
        color = SELECTED_COLOR if is_selected else VERTEX_COLOR
        self.create_oval(x - r, y - r, x + r, y + r,
                         fill=color, outline=VERTEX_BORDER_COLOR, width=2)
        self.create_text(x, y, text=vertex.label, fill=VERTEX_TEXT_COLOR, font=("Arial", 12, "bold"))

    def _draw_edge(self, edge):
        x1, y1 = edge.start_vertex.x, edge.start_vertex.y
        x2, y2 = edge.end_vertex.x, edge.end_vertex.y

        # Vẽ dây
        if edge.is_directed:
            angle = math.atan2(y2 - y1, x2 - x1)
            end_x = x2 - VERTEX_RADIUS * math.cos(angle)
            end_y = y2 - VERTEX_RADIUS * math.sin(angle)
            self.create_line(x1, y1, end_x, end_y, fill=EDGE_COLOR, width=2, arrow=tk.LAST)
        else:
            self.create_line(x1, y1, x2, y2, fill=EDGE_COLOR, width=2)

        # === CHỈ VẼ TRỌNG SỐ NẾU NÓ TỒN TẠI (KHÁC NONE) ===
        if edge.weight is not None:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            text_str = str(edge.weight)
            # Vẽ nền trắng để số dễ đọc
            self.create_rectangle(mid_x - 10, mid_y - 10, mid_x + 10, mid_y + 10,
                                  fill="white", outline="", tags="weight_bg")
            # Vẽ số
            self.create_text(mid_x, mid_y, text=text_str, fill="red", font=("Arial", 10, "bold"))
