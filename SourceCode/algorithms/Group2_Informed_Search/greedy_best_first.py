# -*- coding: utf-8 -*-
import heapq
from algorithms.Group2_Informed_Search.a_star import manhattan_distance

def greedy_planning(matrix, start, end, stats):
    """Tìm đường bằng Greedy (Chỉ ưu tiên h_cost)."""
    if start == end: return [start], 0
        
    rows, cols = len(matrix), len(matrix[0])
    # Hàng đợi ưu tiên lưu: (h_cost, g_cost, vị_trí_hiện_tại, đường_đi_đến_đó)
    pq = [(manhattan_distance(start, end), 0, start, [start])]
    visited = set()
    
    while pq:
        if len(pq) > stats['max_frontier_size']:
            stats['max_frontier_size'] = len(pq)
            
        # Ưu tiên lấy ô có h_cost nhỏ nhất (Gần đích nhất theo đường chim bay)
        h_cost, g_cost, curr, path = heapq.heappop(pq)
        stats['nodes_expanded'] += 1
        
        if curr == end:
            return path, g_cost
            
        if curr in visited:
            continue
        visited.add(curr)
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = curr[0] + dr, curr[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] != 1:
                nxt = (nr, nc)
                if nxt not in visited:
                    step_cost = 5 if matrix[nr][nc] == 2 else 1
                    new_g = g_cost + step_cost
                    new_h = manhattan_distance(nxt, end)
                    
                    stats['total_reached'] += 1
                    heapq.heappush(pq, (new_h, new_g, nxt, path + [nxt]))
                    
    return None, 0

def solve_firefighter_greedy(matrix, start_pos, victims, gates):
    """THUẬT TOÁN CHÍNH: Greedy Best-First Search (Đã sửa logic)"""
    stats = {'nodes_expanded': 0, 'max_frontier_size': 0, 'total_reached': 1, 'reason': ''}
    current_pos = start_pos
    full_path = [start_pos]
    rescue_order = []
    unrescued = list(victims)
    total_cost = 0
    
    while unrescued:
        # 1. Tìm đường đi cứu nạn nhân gần nhất
        unrescued.sort(key=lambda v: manhattan_distance(current_pos, v))
        target_victim = unrescued[0]
        
        path_to_victim, cost = greedy_planning(matrix, current_pos, target_victim, stats)
        if not path_to_victim:
            stats['reason'] = f"Bị chặn đường! Không thể tìm lối tới nạn nhân tại {target_victim}."
            return rescue_order, full_path, total_cost, stats
            
        full_path.extend(path_to_victim[1:])
        total_cost += cost
        current_pos = target_victim
        rescue_order.append(target_victim)
        unrescued.remove(target_victim)
        
        # 2. Đưa nạn nhân ra cửa thoát hiểm gần nhất
        gates.sort(key=lambda g: manhattan_distance(current_pos, g))
        target_gate = gates[0]
        
        path_to_gate, cost = greedy_planning(matrix, current_pos, target_gate, stats)
        if not path_to_gate:
            stats['reason'] = f"Đã cứu nạn nhân tại {target_victim} nhưng không thể tìm thấy lối ra cửa thoát hiểm!"
            return rescue_order, full_path, total_cost, stats
            
        full_path.extend(path_to_gate[1:])
        total_cost += cost
        current_pos = target_gate
    
    stats['reason'] = "Giải cứu thành công tất cả nạn nhân!"
    return rescue_order, full_path, total_cost, stats