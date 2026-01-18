// src/algorithms/dfs.ts

export function dfs(adjList: any, start: string, end: string) {
  console.log(`running DFS from ${start} to ${end}`);

  if (!adjList[start]) return { error: `Không tìm thấy điểm ${start}` };
  if (!adjList[end]) return { error: `Không tìm thấy điểm ${end}` };

  const stack: string[] = [start];
  const visited = new Set<string>();
  const previous: Record<string, string | null> = {};

  // Khởi tạo
  previous[start] = null;
  
  let found = false;
  let safety = 0;

  while (stack.length > 0) {
    safety++;
    if (safety > 5000) return { error: "Lỗi vòng lặp!" };

    const u = stack.pop()!; // Lấy từ đỉnh ngăn xếp

    if (!visited.has(u)) {
      visited.add(u);

      if (u === end) {
        found = true;
        break;
      }

      const neighbors = adjList[u] || [];
      // Đảo ngược thứ tự để DFS duyệt theo thứ tự trực quan hơn khi dùng Stack
      // (Không bắt buộc, nhưng giúp thứ tự duyệt giống recursion hơn)
      for (let i = neighbors.length - 1; i >= 0; i--) {
        const [v, _weight] = neighbors[i];
        if (!visited.has(v)) {
          // Lưu ý: Trong DFS, ta ghi nhận cha (previous) ngay khi đẩy vào stack 
          // để có đường đi duy nhất, mặc dù logic này đơn giản hóa so với DFS chuẩn.
          if (!previous[v]) previous[v] = u; 
          stack.push(v);
        }
      }
    }
  }

  if (!found) return { path: [], cost: 0 };

  // Truy vết
  const path: string[] = [];
  let curr: string | null = end;
  // Giới hạn while để tránh loop vô tận nếu đồ thị có chu trình phức tạp
  let check = 0;
  while (curr && check < 1000) {
    path.unshift(curr);
    curr = previous[curr];
    check++;
  }

  return { path, cost: path.length - 1 };
}