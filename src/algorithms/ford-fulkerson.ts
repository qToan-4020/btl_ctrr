// src/algorithms/ford-fulkerson.ts

export function fordFulkerson(adjList: any, s: string, t: string) {
  console.log(`Running Max Flow from ${s} to ${t}`);

  // 1. Tạo đồ thị thặng dư (Residual Graph)
  // Copy cấu trúc từ adjList, capacity là weight ban đầu
  const capacity: Record<string, Record<string, number>> = {};
  const graph: Record<string, string[]> = {}; // Danh sách kề để duyệt

  // Init graph
  for (let u in adjList) {
    graph[u] = [];
    capacity[u] = {};
    for (let node in adjList) {
       capacity[u][node] = 0; // Mặc định 0
    }
  }

  // Fill capacity & build graph connections
  for (let u in adjList) {
    for (const [v, w] of adjList[u]) {
      // Cạnh xuôi
      capacity[u][v] = w;
      if (!graph[u].includes(v)) graph[u].push(v);
      
      // Cạnh ngược (để undo luồng), ban đầu cap = 0
      if (!graph[v]) graph[v] = [];
      if (!graph[v].includes(u)) graph[v].push(u);
    }
  }

  let maxFlow = 0;
  const parent: Record<string, string | null> = {};
  const flowEdges: { from: string, to: string, flow: number }[] = [];

  // 2. Vòng lặp tìm đường tăng luồng (Augmenting Path) bằng BFS
  while (true) {
    // Reset parent
    for (let node in graph) parent[node] = null;
    
    const queue = [s];
    parent[s] = s; // Đánh dấu đã thăm start

    // BFS tìm đường từ s -> t trong đồ thị thặng dư
    while (queue.length > 0) {
      const u = queue.shift()!;
      if (u === t) break; // Tìm thấy đích

      for (const v of graph[u]) {
        // Nếu chưa thăm VÀ còn khả năng chứa luồng (Residual Capacity > 0)
        if (parent[v] === null && capacity[u][v] > 0) {
          parent[v] = u;
          queue.push(v);
        }
      }
    }

    // Nếu không tìm thấy đường đến t -> Dừng (Đã đạt Max Flow)
    if (parent[t] === null) break;

    // 3. Tính luồng bottleneck (nhỏ nhất trên đường vừa tìm)
    let pathFlow = Infinity;
    let curr = t;
    while (curr !== s) {
      const prev = parent[curr]!;
      pathFlow = Math.min(pathFlow, capacity[prev][curr]);
      curr = prev;
    }

    // 4. Cập nhật đồ thị thặng dư
    curr = t;
    while (curr !== s) {
      const prev = parent[curr]!;
      capacity[prev][curr] -= pathFlow; // Giảm cạnh xuôi
      capacity[curr][prev] += pathFlow; // Tăng cạnh ngược
      curr = prev;
    }

    maxFlow += pathFlow;
  }

  // 5. Tổng hợp kết quả để hiển thị
  // Luồng thực tế trên cạnh (u, v) = Capacity gốc - Capacity thặng dư còn lại
  for (let u in adjList) {
    for (const [v, w] of adjList[u]) {
      const remainingCap = capacity[u][v];
      const actualFlow = w - remainingCap;
      if (actualFlow > 0) {
        flowEdges.push({ from: u, to: v, flow: actualFlow });
      }
    }
  }

  return { maxFlow, flowEdges };
}