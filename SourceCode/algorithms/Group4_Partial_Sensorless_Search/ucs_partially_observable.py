# -*- coding: utf-8 -*-
import heapq

def ucs_planning(belief_matrix, actual_matrix, start, end, stats):
    """HÀM PHỤ TRỢ: Tìm đường tối ưu chi phí thấp nhất bằng UCS."""
    if start == end:
        return [start], 0
        
    rows, cols = len(belief_matrix), len(belief_matrix[0])
    pq = [(0, start, [start])]
    visited = set()
    
    if len(pq) > stats['max_frontier_size']:
        stats['max_frontier_size'] = len(pq)
        
    while pq:
        curr_cost, curr_pos, path = heapq.heappop(pq)
        stats['nodes_expanded'] += 1
        
        if curr_pos == end:
            return path, curr_cost
            
        if curr_pos not in visited:
            visited.add(curr_pos)
            
            r, c = curr_pos
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if belief_matrix[nr][nc] != 1 and (nr, nc) not in visited:
                        step_weight = 5 if actual_matrix[nr][nc] == 2 else 1
                        next_cost = curr_cost + step_weight
                        
                        heapq.heappush(pq, (next_cost, (nr, nc), path + [(nr, nc)]))
                        
                        stats['total_reached'] += 1
                        if len(pq) > stats['max_frontier_size']:
                            stats['max_frontier_size'] = len(pq)
    return None, 0

def solve_partially_observable_ucs(matrix, start_pos, victims, gates):
    """THUẬT TOÁN CHÍNH: UCS Quan sát một phần (Partially Observable UCS)"""
    rows, cols = len(matrix), len(matrix[0])
    belief_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    
    stats = {'nodes_expanded': 0, 'max_frontier_size': 0, 'total_reached': 1, 'reason': ''}
    
    current_pos = start_pos
    full_path = [start_pos]
    rescue_order = []
    remaining_victims = list(victims)
    total_accumulated_cost = 0 
    
    while remaining_victims:
        # 1. Đi cứu nạn nhân
        remaining_victims.sort(key=lambda v: abs(current_pos[0]-v[0]) + abs(current_pos[1]-v[1]))
        target_victim = remaining_victims[0]
        
        while current_pos != target_victim:
            # Radar quét liên tục ở mỗi bước
            r, c = current_pos
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if matrix[nr][nc] == 1:
                        belief_matrix[nr][nc] = 1 
                        
            planned_path, _ = ucs_planning(belief_matrix, matrix, current_pos, target_victim, stats)
            if not planned_path or len(planned_path) < 2:
                stats['reason'] = f"Radar báo lối đi đã bị bịt kín! Không tới được nạn nhân tại {target_victim}."
                return rescue_order, full_path, total_accumulated_cost, stats
                
            next_step = planned_path[1]
            step_weight = 5 if matrix[next_step[0]][next_step[1]] == 2 else 1
            total_accumulated_cost += step_weight
            
            current_pos = next_step
            full_path.append(current_pos)
            
        rescue_order.append(target_victim)
        remaining_victims.remove(target_victim)
        
        # 2. Đưa nạn nhân thoát ra cửa
        gates.sort(key=lambda g: abs(current_pos[0]-g[0]) + abs(current_pos[1]-g[1]))
        target_gate = gates[0]
        
        while current_pos != target_gate:
            r, c = current_pos
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if matrix[nr][nc] == 1:
                        belief_matrix[nr][nc] = 1 
                        
            planned_path, _ = ucs_planning(belief_matrix, matrix, current_pos, target_gate, stats)
            if not planned_path or len(planned_path) < 2:
                stats['reason'] = f"Cứu xong nạn nhân nhưng radar báo lối ra cửa đã bị bịt kín!"
                return rescue_order, full_path, total_accumulated_cost, stats
                
            next_step = planned_path[1]
            step_weight = 5 if matrix[next_step[0]][next_step[1]] == 2 else 1
            total_accumulated_cost += step_weight
            
            current_pos = next_step
            full_path.append(current_pos)
            
    stats['reason'] = "Giải cứu thành công tất cả nạn nhân!"
    return rescue_order, full_path, total_accumulated_cost, stats