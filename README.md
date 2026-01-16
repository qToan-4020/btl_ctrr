## thằng nào làm phần sau thì dựa theo cấu trúc tao chia file mà làm tiếp nha 

project/
│
├── main.py                  # [Cửa chính] Nơi khởi chạy ứng dụng
│
├── graph/                   # [Dữ liệu] Nơi chứa cấu trúc đồ thị (Quan trọng cho thuật toán)
│   ├── graph_model.py       # Chứa danh sách đỉnh (vertices) và cạnh (edges)
│   ├── vertex.py            # Định nghĩa 1 Đỉnh (x, y, id, label)
│   └── edge.py              # Định nghĩa 1 Cạnh (start, end, weight)
│
├── ui/                      # [Giao diện] Chỉ lo việc hiển thị, không tính toán
│   ├── main_window.py       # Cửa sổ chính, chứa thanh công cụ (Toolbar) và nút bấm
│   └── canvas.py            # Bảng vẽ, chịu trách nhiệm vẽ hình tròn, đường thẳng, số...
│
├── controller/              # [Điều khiển] Bộ não xử lý logic
│   └── graph_controller.py  # Nhận click chuột -> Sửa dữ liệu -> Yêu cầu vẽ lại
│
└── utils/                   # [Tiện ích] Cấu hình chung
    ├── constants.py         # Màu sắc, kích thước, tên các chế độ (MODE_...)
    └── helpers.py           # Hàm toán học (tính khoảng cách, kiểm tra va chạm)
