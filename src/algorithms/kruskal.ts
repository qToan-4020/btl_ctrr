// src/algorithms/kruskal.ts

// Helper: Union-Find
class UnionFind {
  parent: Record<string, string> = {};
  constructor(nodes: string[]) {
    nodes.forEach(n => this.parent[n] = n);
  }
  find(i: string): string {
    if (this.parent[i] === i) return i;
    return this.parent[i] = this.find(this.parent[i]);
  }
  union(i: string, j: string): boolean {
    const rootI = this.find(i);
    const rootJ = this.find(j);
    if (rootI !== rootJ) {
      this.parent[rootI] = rootJ;
      return true; // Nối thành công
    }
    return false; // Đã nối rồi (tạo chu trình)
  }
}

export function kruskal(nodes: string[], edges: { from: string, to: string, weight: number }[]) {
  // 1. Sắp xếp cạnh theo trọng số tăng dần
  edges.sort((a, b) => a.weight - b.weight);

  const uf = new UnionFind(nodes);
  const mstEdges: { from: string, to: string }[] = [];
  let totalWeight = 0;
  const steps: any[] = []; // Lưu lại từng bước để làm animation

  for (const edge of edges) {
    // 2. Nếu nối 2 đỉnh không tạo chu trình -> Chọn
    if (uf.union(edge.from, edge.to)) {
      mstEdges.push(edge);
      totalWeight += edge.weight;
      steps.push({ ...edge, added: true }); // Ghi lại bước thêm
    } else {
      steps.push({ ...edge, added: false }); // Ghi lại bước bỏ qua
    }
  }

  return { cost: totalWeight, mstEdges, steps };
}