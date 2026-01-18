// src/algorithms/bfs.ts

export function bfs(adjList: any, start: string, end: string) {
  console.log(`running BFS from ${start} to ${end}`);

  if (!adjList[start]) return { error: `Không tìm thấy điểm ${start}` };
  if (!adjList[end]) return { error: `Không tìm thấy điểm ${end}` };

  const queue: string[] = [start];
  const visited = new Set<string>();
  const previous: Record<string, string | null> = {};
  
  visited.add(start);
  previous[start] = null;

  let found = false;
  let safety = 0;

  while (queue.length > 0) {
    safety++;
    if(safety > 5000) return { error: "Lỗi vòng lặp!" };

    const u = queue.shift()!; // Lấy đầu hàng đợi

    if (u === end) {
      found = true;
      break;
    }

    const neighbors = adjList[u] || [];
    for (const [v, _weight] of neighbors) {
      if (!visited.has(v)) {
        visited.add(v);
        previous[v] = u; // Lưu vết: v được đi tới từ u
        queue.push(v);
      }
    }
  }

  if (!found) return { path: [], cost: 0 };

  // Truy vết đường đi
  const path: string[] = [];
  let curr: string | null = end;
  while (curr) {
    path.unshift(curr);
    curr = previous[curr];
  }

  // Cost của BFS tính bằng số bước (số cạnh)
  return { path, cost: path.length - 1 };
}