// src/algorithms/bipartite.ts

export interface BipartiteResult {
  isBipartite: boolean;
  setA: string[]; // Tập hợp đỉnh màu Đỏ
  setB: string[]; // Tập hợp đỉnh màu Xanh
  conflictNode?: string; // Điểm gây xung đột (nếu có)
  error?: string;
}

export function checkBipartite(adjList: any): BipartiteResult {
  console.log("Kiểm tra đồ thị 2 phía...");

  const colors: Record<string, number> = {}; // 0: chưa tô, 1: Đỏ, -1: Xanh
  const setA: string[] = [];
  const setB: string[] = [];

  // Khởi tạo màu = 0 (Chưa tô)
  for (let node in adjList) {
    colors[node] = 0;
  }

  // Duyệt qua tất cả các đỉnh (đề phòng đồ thị không liên thông)
  for (let startNode in adjList) {
    if (colors[startNode] !== 0) continue; // Đã tô rồi thì bỏ qua

    const queue: string[] = [startNode];
    colors[startNode] = 1; // Tô màu Đỏ cho điểm bắt đầu
    setA.push(startNode);

    while (queue.length > 0) {
      const u = queue.shift()!;
      
      const neighbors = adjList[u] || [];
      for (const [v, _weight] of neighbors) {
        if (colors[v] === 0) {
          // Nếu chưa tô màu -> Tô màu ngược lại với u
          colors[v] = -colors[u];
          if (colors[v] === 1) setA.push(v);
          else setB.push(v);
          queue.push(v);
        } else if (colors[v] === colors[u]) {
          // Nếu đã tô màu mà TRÙNG màu với u -> Xung đột!
          return { 
            isBipartite: false, 
            setA: [], 
            setB: [], 
            conflictNode: v,
            error: `Xung đột màu tại điểm ${u} và ${v}` 
          };
        }
      }
    }
  }

  return { isBipartite: true, setA, setB };
}