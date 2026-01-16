# project/graph/vertex.py

class Vertex:
    def __init__(self, vertex_id, x, y, label=None):
        self.id = vertex_id
        self.x = x
        self.y = y
        self.label = label if label else str(vertex_id)

        # Thuộc tính hỗ trợ thuật toán sau này
        self.color = None
        self.visited = False

    def __repr__(self):
        return f"Vertex({self.id}, {self.label})"
