# project/main.py
from graph.graph_model import GraphModel
from controller.graph_controller import GraphController
from ui.main_window import MainWindow
# === THÊM ĐOẠN NÀY ĐỂ FIX LỖI MỜ GIAO DIỆN TRÊN WINDOWS ===
try:
    from ctypes import windll
    # Mức 1: Process_System_DPI_Aware (Cơ bản)
    # Mức 2: Process_Per_Monitor_DPI_Aware (Tốt nhất)
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass
def main():
    # 1. Khởi tạo Model
    model = GraphModel(is_directed=False)

    # 2. Khởi tạo UI (Truyền Controller Class và Model vào)
    # Controller sẽ được khởi tạo bên trong MainWindow để đảm bảo liên kết 2 chiều
    app = MainWindow(GraphController, model)

    # 3. Chạy vòng lặp sự kiện
    app.mainloop()

if __name__ == "__main__":
    main()
