CẤU TRÚC DỰ ÁN GRAPH VISUALIZATION (MVC PATTERN)
================================================

# CẤU TRÚC DỰ ÁN GRAPH VISUALIZATION (MVC PATTERN)

```text
project/
│
├── main.py                  # [Cửa chính] Chạy file này để mở ứng dụng
│
├── algorithms/              # [MỚI - Dành cho PHẦN 2] Nơi viết thuật toán
│   ├── __init__.py
│   ├── bfs.py               # (Gợi ý) Viết thuật toán BFS
│   ├── dfs.py               # (Gợi ý) Viết thuật toán DFS
│   └── dijkstra.py          # (Gợi ý) Viết thuật toán Dijkstra
│
├── graph/                   # [Model] Chứa dữ liệu đồ thị
│   ├── __init__.py
│   ├── graph_model.py       # Quan trọng nhất: Chứa list vertices, edges
│   ├── vertex.py            # Class Đỉnh (x, y, id, label)
│   └── edge.py              # Class Cạnh (start, end, weight)
│
├── ui/                      # [View] Giao diện hiển thị
│   ├── __init__.py
│   ├── main_window.py       # Cửa sổ chính, Toolbar, Nút bấm
│   └── canvas.py            # Khu vực vẽ hình tròn, đường thẳng
│
├── controller/              # [Controller] Xử lý logic
│   ├── __init__.py
│   ├── graph_controller.py  # Điều phối: Nhận click -> Gọi thuật toán -> Vẽ lại
│   └── __init__.py
│
└── utils/                   # [Tiện ích] Cấu hình chung
    ├── __init__.py
    ├── constants.py         # Màu sắc, kích thước, font chữ
    └── helpers.py           # Hàm tính toán khoảng cách

=================================================
1. graph/graph_model.py (Quan trọng nhất)
Vai trò: Đây là "kho dữ liệu". Mọi thuật toán sẽ phải đọc dữ liệu từ đây.

Dữ liệu cần dùng:

self.vertices: Một Dictionary chứa các đỉnh {id: VertexObj}.

self.edges: Một List chứa các cạnh [EdgeObj, EdgeObj...].

self.is_directed: Biến boolean (True/False) để biết đồ thị có hướng hay không.

Gợi ý: Khi làm thuật toán, bạn sẽ viết hàm nhận vào GraphModel, sau đó chuyển đổi vertices và edges này thành Danh sách kề (Adjacency List) hoặc Ma trận kề để chạy thuật toán.

2. graph/vertex.py & graph/edge.py
Vai trò: Hiểu cấu trúc của một đối tượng.

Vertex: Có thuộc tính id (định danh duy nhất) và label (tên hiển thị).

Edge: Có start_vertex, end_vertex, và đặc biệt là weight (trọng số - quan trọng cho Dijkstra/Prim).

3. controller/graph_controller.py
Vai trò: Nơi bạn sẽ gắn các nút bấm kích hoạt thuật toán.

Hướng phát triển:

Hiện tại file này đang xử lý vẽ vời (Add, Connect...).

Sắp tới, bạn sẽ thêm các hàm như run_bfs(), run_dijkstra() vào đây.

Các hàm này sẽ gọi thuật toán, lấy kết quả, và cập nhật màu sắc (color) cho các Vertex/Edge để hiển thị đường đi.

4. ui/main_window.py
Vai trò: Nơi bạn thêm các nút bấm mới cho thuật toán.

Việc cần làm: Hiện tại đang có nút menu "File", "Move", "Connect"... Bạn sẽ cần thêm một menu hoặc nút mới tên là "Algorithms" để người dùng chọn chạy BFS hay DFS.
