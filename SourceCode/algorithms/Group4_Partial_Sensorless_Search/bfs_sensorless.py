# -*- coding: utf-8 -*-
from collections import deque

def bfs_planning(belief_matrix, start, end, stats):
    """HÀM PHỤ TRỢ: Tìm đường ngắn nhất trong trí nhớ giả định bằng BFS."""
    if start == end:
        return [start]
        
    rows = len(belief_matrix)
    cols = len(belief_matrix[0])
    
    queue = deque([(start, [start])])
    visited = {start}
    
    if len(queue) > stats['max_frontier_size']:
        stats['max_frontier_size'] = len(queue)
        
    while queue:
        curr, path = queue.popleft()
        stats['nodes_expanded'] += 1
        
        if curr == end:
            return path
            
        r, c = curr
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if belief_matrix[nr][nc] != 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))
                    
                    stats['total_reached'] += 1
                    if len(queue) > stats['max_frontier_size']:
                        stats['max_frontier_size'] = len(queue)
    return None

def solve_sensorless_bfs(matrix, start_pos, victims, gates):
    """THUẬT TOÁN CHÍNH: BFS Không cảm biến (Sensorless BFS)"""
    rows, cols = len(matrix), len(matrix[0])
    belief_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    
    stats = {'nodes_expanded': 0, 'max_frontier_size': 0, 'total_reached': 1, 'reason': ''}
    
    current_pos = start_pos
    full_path = [start_pos]
    rescue_order = []
    remaining_victims = list(victims)
    
    while remaining_victims:
        # 1. Mục tiêu: Nạn nhân gần nhất
        remaining_victims.sort(key=lambda v: abs(current_pos[0]-v[0]) + abs(current_pos[1]-v[1]))
        target_victim = remaining_victims[0]
        
        while current_pos != target_victim:
            planned_path = bfs_planning(belief_matrix, current_pos, target_victim, stats)
            if not planned_path or len(planned_path) < 2:
                stats['reason'] = f"Bị bao vây trong trí nhớ - Không tìm thấy đường tới nạn nhân tại {target_victim}!"
                return rescue_order, full_path, len(full_path) - 1, stats
                
            next_step = planned_path[1] # Bước 1 bước để dò đường
            
            if matrix[next_step[0]][next_step[1]] == 1:
                belief_matrix[next_step[0]][next_step[1]] = 1 # Nhớ tường
                full_path.extend([next_step, current_pos])    # Va chạm và giật lùi
                continue
                
            current_pos = next_step
            full_path.append(current_pos)
            
        # Đã cứu được nạn nhân
        rescue_order.append(target_victim)
        remaining_victims.remove(target_victim)
        
        # 2. Mục tiêu: Cửa thoát hiểm gần nhất
        gates.sort(key=lambda g: abs(current_pos[0]-g[0]) + abs(current_pos[1]-g[1]))
        target_gate = gates[0]
        
        while current_pos != target_gate:
            planned_path = bfs_planning(belief_matrix, current_pos, target_gate, stats)
            if not planned_path or len(planned_path) < 2:
                stats['reason'] = f"Đã cứu nạn nhân tại {target_victim} nhưng bị kẹt, không thể ra cửa thoát hiểm!"
                return rescue_order, full_path, len(full_path) - 1, stats
                
            next_step = planned_path[1]
            
            if matrix[next_step[0]][next_step[1]] == 1:
                belief_matrix[next_step[0]][next_step[1]] = 1
                full_path.extend([next_step, current_pos])
                continue
                
            current_pos = next_step
            full_path.append(current_pos)
            
    stats['reason'] = "Giải cứu thành công tất cả nạn nhân!"
    return rescue_order, full_path, len(full_path) - 1, stats