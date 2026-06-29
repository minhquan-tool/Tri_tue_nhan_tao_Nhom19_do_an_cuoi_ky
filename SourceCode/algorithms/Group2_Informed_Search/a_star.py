# -*- coding: utf-8 -*-
import heapq

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def a_star_planning(matrix, start, end, stats):
    """Tìm đường bằng A* cho 1 chặng (từ điểm A đến B)."""
    if start == end: return [start], 0
        
    rows, cols = len(matrix), len(matrix[0])
    # Hàng đợi ưu tiên lưu: (f_cost, g_cost, vị_trí_hiện_tại, đường_đi_đến_đó)
    pq = [(manhattan_distance(start, end), 0, start, [start])]
    visited = {} # Lưu chi phí g_cost nhỏ nhất tại mỗi ô để tránh đi đường vòng
    
    while pq:
        if len(pq) > stats['max_frontier_size']:
            stats['max_frontier_size'] = len(pq)
            
        f_cost, g_cost, curr, path = heapq.heappop(pq)
        stats['nodes_expanded'] += 1
        
        if curr == end:
            return path, g_cost
            
        if curr in visited and visited[curr] <= g_cost:
            continue
        visited[curr] = g_cost
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = curr[0] + dr, curr[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] != 1:
                nxt = (nr, nc)
                # Tính chi phí bước đi (Lửa = 5, Trống = 1)
                step_cost = 5 if matrix[nr][nc] == 2 else 1
                new_g = g_cost + step_cost
                new_f = new_g + manhattan_distance(nxt, end)
                
                if nxt not in visited or new_g < visited[nxt]:
                    stats['total_reached'] += 1
                    heapq.heappush(pq, (new_f, new_g, nxt, path + [nxt]))
                    
    return None, 0

def solve_firefighter_a_star(matrix, start_pos, victims, gates):
    """THUẬT TOÁN CHÍNH: A* Search (Đã sửa logic đưa từng nạn nhân ra cửa)"""
    stats = {'nodes_expanded': 0, 'max_frontier_size': 0, 'total_reached': 1, 'reason': ''}
    current_pos = start_pos
    full_path = [start_pos]
    rescue_order = []
    unrescued = list(victims)
    total_cost = 0
    
    while unrescued:
        # 1. Tìm đường đi cứu nạn nhân gần nhất tính từ vị trí hiện tại
        unrescued.sort(key=lambda v: manhattan_distance(current_pos, v))
        target_victim = unrescued[0]
        
        path_to_victim, cost = a_star_planning(matrix, current_pos, target_victim, stats)
        if not path_to_victim:
            stats['reason'] = f"Bị chặn đường! Không thể tìm lối tới nạn nhân tại {target_victim}."
            return rescue_order, full_path, total_cost, stats
            
        # Cập nhật đường đi đến nạn nhân
        full_path.extend(path_to_victim[1:])
        total_cost += cost
        current_pos = target_victim
        rescue_order.append(target_victim)
        unrescued.remove(target_victim)
        
        # 2. Ngay lập tức tìm đường đưa nạn nhân vừa cứu ra cửa thoát hiểm gần nhất
        gates.sort(key=lambda g: manhattan_distance(current_pos, g))
        target_gate = gates[0]
        
        path_to_gate, cost = a_star_planning(matrix, current_pos, target_gate, stats)
        if not path_to_gate:
            stats['reason'] = f"Đã cứu nạn nhân tại {target_victim} nhưng bị chặn lối ra cửa thoát hiểm!"
            return rescue_order, full_path, total_cost, stats
            
        # Cập nhật đường đi ra cửa thoát hiểm
        full_path.extend(path_to_gate[1:])
        total_cost += cost
        current_pos = target_gate  # Lính cứu hỏa đang đứng ở cửa thoát hiểm, chuẩn bị quay lại cứu người tiếp theo

    stats['reason'] = "Giải cứu thành công tất cả nạn nhân!"
    return rescue_order, full_path, total_cost, stats