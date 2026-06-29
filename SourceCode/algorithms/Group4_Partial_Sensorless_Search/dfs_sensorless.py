# -*- coding: utf-8 -*-

def dfs_planning(belief_matrix, start, end, stats):
    """HÀM PHỤ TRỢ: Tìm đường giả định bằng DFS trong trí nhớ."""
    if start == end: 
        return [start]
        
    rows, cols = len(belief_matrix), len(belief_matrix[0])
    stack = [(start, [start])]
    visited = {start}
    
    if len(stack) > stats['max_frontier_size']:
        stats['max_frontier_size'] = len(stack)
        
    while stack:
        curr, path = stack.pop()
        stats['nodes_expanded'] += 1
        
        if curr == end:
            return path
            
        r, c = curr
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if belief_matrix[nr][nc] != 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append(((nr, nc), path + [(nr, nc)]))
                    
                    stats['total_reached'] += 1
                    if len(stack) > stats['max_frontier_size']:
                        stats['max_frontier_size'] = len(stack)
    return None

def solve_sensorless_dfs(matrix, start_pos, victims, gates):
    """THUẬT TOÁN CHÍNH: DFS Không cảm biến (Sensorless DFS)"""
    rows, cols = len(matrix), len(matrix[0])
    belief_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    
    stats = {'nodes_expanded': 0, 'max_frontier_size': 0, 'total_reached': 1, 'reason': ''}
    
    current_pos = start_pos
    full_path = [start_pos]
    rescue_order = []
    remaining_victims = list(victims)
    
    while remaining_victims:
        # 1. Mục tiêu: Nạn nhân
        remaining_victims.sort(key=lambda v: abs(current_pos[0]-v[0]) + abs(current_pos[1]-v[1]))
        target_victim = remaining_victims[0]
        
        while current_pos != target_victim:
            planned_path = dfs_planning(belief_matrix, current_pos, target_victim, stats)
            if not planned_path or len(planned_path) < 2:
                stats['reason'] = f"Bị cô lập hoàn toàn - Không tìm thấy lối tới nạn nhân tại {target_victim}!"
                return rescue_order, full_path, len(full_path) - 1, stats
                
            for step_idx in range(1, len(planned_path)):
                next_step = planned_path[step_idx]
                
                if matrix[next_step[0]][next_step[1]] == 1:
                    belief_matrix[next_step[0]][next_step[1]] = 1
                    full_path.extend([next_step, current_pos])
                    break # Dừng lại ngay lập tức để lập kế hoạch khác
                    
                current_pos = next_step
                full_path.append(current_pos)
                
                if current_pos == target_victim: 
                    break # Đã đến được chỗ nạn nhân, ngưng đi mù quáng
                    
        rescue_order.append(target_victim)
        remaining_victims.remove(target_victim)
        
        # 2. Mục tiêu: Cửa thoát hiểm
        gates.sort(key=lambda g: abs(current_pos[0]-g[0]) + abs(current_pos[1]-g[1]))
        target_gate = gates[0]
        
        while current_pos != target_gate:
            planned_path = dfs_planning(belief_matrix, current_pos, target_gate, stats)
            if not planned_path or len(planned_path) < 2:
                stats['reason'] = "Đã cứu nạn nhân nhưng không tìm thấy đường ra cửa thoát hiểm!"
                return rescue_order, full_path, len(full_path) - 1, stats
                
            for step_idx in range(1, len(planned_path)):
                next_step = planned_path[step_idx]
                
                if matrix[next_step[0]][next_step[1]] == 1:
                    belief_matrix[next_step[0]][next_step[1]] = 1
                    full_path.extend([next_step, current_pos])
                    break
                    
                current_pos = next_step
                full_path.append(current_pos)
                
                if current_pos == target_gate:
                    break
                    
    stats['reason'] = "Giải cứu thành công tất cả nạn nhân!"
    return rescue_order, full_path, len(full_path) - 1, stats