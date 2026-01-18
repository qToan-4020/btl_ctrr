// src/algorithms/prim.ts
export function prim(adjList: any) {
  const nodes = Object.keys(adjList);
  if (nodes.length === 0) return { path: [], cost: 0, mstEdges: [] };

  const startNode = nodes[0]; // Bắt đầu từ đỉnh đầu tiên bất kỳ
  const distances: Record<string, number> = {};
  const parent: Record<string, string | null> = {};
  const visited = new Set<string>();
  const mstEdges: { from: string, to: string }[] = [];

  nodes.forEach(n => {
    distances[n] = Infinity;
    parent[n] = null;
  });
  distances[startNode] = 0;

  // Priority Queue đơn giản
  let pq = [{ id: startNode, dist: 0 }];

  while (pq.length > 0) {
    pq.sort((a, b) => a.dist - b.dist);
    const { id: u } = pq.shift()!;

    if (visited.has(u)) continue;
    visited.add(u);

    // Nếu có cha, ghi nhận cạnh vào MST
    if (parent[u] !== null) {
      mstEdges.push({ from: parent[u]!, to: u });
    }

    const neighbors = adjList[u] || [];
    for (const [v, weight] of neighbors) {
      if (!visited.has(v) && weight < distances[v]) {
        distances[v] = weight;
        parent[v] = u;
        pq.push({ id: v, dist: weight });
      }
    }
  }

  // Tính tổng trọng số MST
  const totalWeight = Object.values(distances).reduce((sum, d) => (d !== Infinity ? sum + d : sum), 0);
  
  // Trả về danh sách cạnh để tô màu
  return { cost: totalWeight, mstEdges };
}