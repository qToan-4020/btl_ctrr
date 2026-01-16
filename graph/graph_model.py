# project/graph/graph_model.py
from .vertex import Vertex
from .edge import Edge
import copy # <--- THÊM IMPORT NÀY

class GraphModel:
    def __init__(self, is_directed=False):
        self.vertices = {}
        self.edges = []
        self.is_directed = is_directed
        self.next_id = 0
        self.naming_mode = "1, 2, 3..."

    # ... (Giữ nguyên các phương thức set_naming_mode, _generate_label, add_vertex, add_edge, remove_vertex, remove_edge, clear) ...
    def set_naming_mode(self, mode):
        self.naming_mode = mode

    def _generate_label(self, current_id):
        if self.naming_mode == "0, 1, 2...":
            return str(current_id)
        elif self.naming_mode == "A, B, C...":
            if current_id < 26:
                return chr(65 + current_id)
            return str(current_id)
        else:
            return str(current_id + 1)

    def add_vertex(self, x, y):
        label = self._generate_label(self.next_id)
        v = Vertex(self.next_id, x, y, label)
        self.vertices[self.next_id] = v
        self.next_id += 1
        return v

    def add_edge(self, start_id, end_id, weight=1):
        if start_id not in self.vertices or end_id not in self.vertices:
            return None
        start_v = self.vertices[start_id]
        end_v = self.vertices[end_id]

        for edge in self.edges:
            if edge.start_vertex == start_v and edge.end_vertex == end_v:
                return None
            if not self.is_directed:
                if edge.start_vertex == end_v and edge.end_vertex == start_v:
                    return None

        new_edge = Edge(start_v, end_v, weight, self.is_directed)
        self.edges.append(new_edge)
        return new_edge

    def remove_vertex(self, vertex_id):
        if vertex_id in self.vertices:
            del self.vertices[vertex_id]
            self.edges = [
                e for e in self.edges
                if e.start_vertex.id != vertex_id and e.end_vertex.id != vertex_id
            ]
            if len(self.vertices) == 0:
                self.next_id = 0

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)

    def clear(self):
        self.vertices = {}
        self.edges = []
        self.next_id = 0

    # === MỚI: Hàm tạo bản sao dữ liệu để lưu trữ cho Undo ===
    def get_state(self):
        """Trả về một bản sao sâu (deep copy) của dữ liệu đồ thị hiện tại."""
        # Sử dụng copy.deepcopy để đảm bảo bản sao hoàn toàn độc lập
        return copy.deepcopy(self.vertices), copy.deepcopy(self.edges), self.next_id

    def restore_state(self, state):
        """Khôi phục đồ thị về một trạng thái đã lưu."""
        vertices_copy, edges_copy, next_id_copy = state
        self.vertices = vertices_copy
        self.edges = edges_copy
        self.next_id = next_id_copy
