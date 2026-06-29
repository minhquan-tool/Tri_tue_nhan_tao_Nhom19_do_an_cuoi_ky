# -*- coding: utf-8 -*-
from collections import deque

def simple_bfs_path(matrix, start, end):
    """Hàm phụ trợ tìm đường thực tế giữa 2 điểm (sau khi CSP đã chốt thứ tự)"""
    if start == end: return [start]
    rows, cols = len(matrix), len(matrix[0])
    q = deque([(start, [start])])
    visited = {start}
    while q:
        curr, path = q.popleft()
        if curr == end: return path
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = curr[0] + dr, curr[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] != 1 and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append(((nr, nc), path + [(nr, nc)]))
    return []

def solve_firefighter_backtracking(matrix, start_pos, victims, gates):
    """THUẬT TOÁN CSP 1: BACKTRACKING CƠ BẢN"""
    stats = {'assignments': 0, 'backtracks': 0, 'tree_log': [], 'reason': ''}
    n = len(victims)
    
    # Hàm đệ quy Backtracking
    def backtrack(assignment):
        stats['assignments'] += 1
        if len(assignment) == n:
            return assignment
            
        current_var = len(assignment) + 1 # Đang xét lượt thứ mấy
        
        for victim in victims:
            # Kiểm tra ràng buộc: Nạn nhân chưa được gán ở các lượt trước
            if victim not in assignment:
                stats['tree_log'].append(f"Thử gán Lượt {current_var} -> Nạn nhân tại {victim}")
                assignment.append(victim)
                
                result = backtrack(assignment)
                if result:
                    return result
                    
                # Hủy gán (Quay lui)
                stats['tree_log'].append(f"Quay lui: Rút nạn nhân {victim} khỏi Lượt {current_var}")
                assignment.pop()
                stats['backtracks'] += 1
                
        return None

    # Chạy CSP để tìm thứ tự cứu
    stats['tree_log'].append("GỐC: Bắt đầu dò cây Backtrack...")
    rescue_order = backtrack([])
    
    if not rescue_order:
        stats['reason'] = "CSP không thể tìm được phép gán thỏa mãn (Dead-end)."
        return [], [], 0, stats

    # LOGIC VẼ ĐƯỜNG ĐI ĐÃ ĐƯỢC SỬA LẠI
    full_path = [start_pos]
    curr = start_pos
    for v in rescue_order:
        # 1. Tới nạn nhân
        p = simple_bfs_path(matrix, curr, v)
        if not p:
            stats['reason'] = f"CSP đã chọn {v} nhưng thực tế bị tường bít kín!"
            return rescue_order, full_path, len(full_path)-1, stats
        full_path.extend(p[1:])
        curr = v
        
        # 2. Đưa nạn nhân thoát hiểm
        gates.sort(key=lambda g: abs(curr[0]-g[0]) + abs(curr[1]-g[1]))
        target_gate = gates[0]
        gate_path = simple_bfs_path(matrix, curr, target_gate)
        if not gate_path:
            stats['reason'] = f"Đã cứu nạn nhân tại {v} nhưng bít đường ra cửa!"
            return rescue_order, full_path, len(full_path)-1, stats
        full_path.extend(gate_path[1:])
        curr = target_gate
    
    stats['reason'] = "Thành công!"
    return rescue_order, full_path, len(full_path)-1, stats