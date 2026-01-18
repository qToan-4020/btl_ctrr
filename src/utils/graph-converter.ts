// src/utils/graph-converter.ts

export function getRepresentations(nodes: any[], edges: any[], isDirected: boolean) {
  // 1. Sắp xếp Node ID để hiển thị đẹp (1, 2, 3...)
  const nodeIds = nodes.map(n => String(n.id)).sort((a, b) => Number(a) - Number(b));
  
  const idToIndex: Record<string, number> = {};
  nodeIds.forEach((id, idx) => idToIndex[id] = idx);
  const n = nodeIds.length;

  // --- A. MA TRẬN KỀ (Adjacency Matrix) ---
  const matrix = Array(n).fill(null).map(() => Array(n).fill(0));
  
  edges.forEach(e => {
    const u = idToIndex[String(e.from)];
    const v = idToIndex[String(e.to)];
    const w = Number(e.weight !== undefined ? e.weight : (e.label || 1));
    
    if (u !== undefined && v !== undefined) {
      matrix[u][v] = w; // Luôn có chiều xuôi
      if (!isDirected) {
        matrix[v][u] = w; // Nếu vô hướng thì có chiều ngược
      }
    }
  });

  // Tạo chuỗi hiển thị Ma trận
  let matrixStr = "      " + nodeIds.map(id => id.padEnd(3)).join(" ") + "\n";
  matrixStr += "      " + nodeIds.map(() => "---").join("-") + "\n";
  
  matrix.forEach((row, idx) => {
    const rowStr = row.map(val => String(val).padEnd(3)).join(" ");
    matrixStr += `${nodeIds[idx].padEnd(3)} | ${rowStr}\n`;
  });

  // --- B. DANH SÁCH KỀ (Adjacency List) ---
  let adjListStr = "";
  nodeIds.forEach(u => {
    const neighbors: string[] = [];
    edges.forEach(e => {
      const from = String(e.from);
      const to = String(e.to);
      const w = Number(e.weight !== undefined ? e.weight : (e.label || 1));
      
      // Chiều xuôi: u -> v
      if (from === u) neighbors.push(`${to}(${w})`);
      
      // Chiều ngược: v -> u (Chỉ thêm nếu Vô hướng)
      if (!isDirected && to === u) neighbors.push(`${from}(${w})`);
    });
    
    neighbors.sort();
    if (neighbors.length > 0) adjListStr += `${u} -> [ ${neighbors.join(", ")} ]\n`;
    else adjListStr += `${u} -> []\n`;
  });

  // --- C. DANH SÁCH CẠNH (Edge List) ---
  let edgeListStr = "";
  if (edges.length === 0) {
      edgeListStr = "(Chưa có cạnh nào)";
  } else {
      edges.forEach((e, idx) => {
         const w = Number(e.weight !== undefined ? e.weight : (e.label || 1));
         const arrow = isDirected ? "->" : "--"; // Đổi ký hiệu dựa trên hướng
         edgeListStr += `${idx + 1}. (${e.from} ${arrow} ${e.to}) : w=${w}\n`;
      });
  }

  return { matrixStr, adjListStr, edgeListStr };
}