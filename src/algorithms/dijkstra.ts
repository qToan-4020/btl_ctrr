export interface DijkstraResult {
  path: string[];
  cost: number;
  visitedOrder: string[];
  error?: string;
}

export function dijkstra(adjList: any, start: string, end: string): DijkstraResult {
  console.log(`🏁 Dijkstra chạy từ "${start}" đến "${end}"`);
  
  if (!adjList[start]) return { path: [], cost: 0, visitedOrder: [], error: `❌ Không tìm thấy điểm "${start}"` };
  if (!adjList[end]) return { path: [], cost: 0, visitedOrder: [], error: `❌ Không tìm thấy điểm "${end}"` };

  const distances: Record<string, number> = {};
  const previous: Record<string, string | null> = {};
  const visitedOrder: string[] = [];
  
  for (let node in adjList) {
    distances[node] = Infinity;
    previous[node] = null;
  }
  distances[start] = 0;

  let pq = [{ id: start, dist: 0 }];
  let safety = 0;

  while (pq.length > 0) {
    safety++;
    if(safety > 5000) return { path: [], cost: 0, visitedOrder: [], error: "Lỗi vòng lặp vô hạn!" };

    pq.sort((a, b) => a.dist - b.dist);
    const item = pq.shift();
    if (!item) break;
    const { id: u, dist: currentDist } = item;

    if (currentDist > distances[u]) continue;
    visitedOrder.push(u);
    if (u === end) break; 

    const neighbors = adjList[u] || [];
    for (const [v, weight] of neighbors) {
      // Ép kiểu lại lần nữa cho chắc chắn
      const w = Number(weight); 
      const newDist = currentDist + w;
      
      if (newDist < distances[v]) {
        distances[v] = newDist;
        previous[v] = u;
        pq.push({ id: v, dist: newDist });
      }
    }
  }

  if (distances[end] === Infinity) return { path: [], cost: Infinity, visitedOrder };

  const path: string[] = [];
  let curr: string | null = end;
  while (curr) {
    path.unshift(curr);
    curr = previous[curr];
  }

  return { path, cost: distances[end], visitedOrder };
}