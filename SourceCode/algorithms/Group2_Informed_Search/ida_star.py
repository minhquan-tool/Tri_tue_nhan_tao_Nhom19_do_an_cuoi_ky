# -*- coding: utf-8 -*-
from algorithms.Group2_Informed_Search.a_star import manhattan_distance

def ida_star_planning(matrix, start, end, stats):
    """Tìm đường bằng IDA* (Chạy DFS tăng dần ngưỡng Threshold)."""
    rows, cols = len(matrix), len(matrix[0])
    
    def search(curr, g, threshold, current_path, path_set):
        f = g + manhattan_distance(curr, end)
        stats['nodes_expanded'] += 1
        
        # Nếu vượt quá ngưỡng cho phép, chặn lại và trả về giá trị f bị vượt này
        if f > threshold:
            return f, None, 0
        if curr == end:
            return "FOUND", current_path, g
            
        min_exceeded = float('inf')
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = curr[0] + dr, curr[1] + dc
            nxt = (nr, nc)
            
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] != 1:
                # Đảm bảo không đi lùi tạo thành vòng lặp vô hạn trong DFS nhánh này
                if nxt not in path_set:
                    step_cost = 5 if matrix[nr][nc] == 2 else 1
                    stats['total_reached'] += 1
                    
                    path_set.add(nxt)
                    current_path.append(nxt)
                    
                    if len(current_path) > stats['max_frontier_size']:
                        stats['max_frontier_size'] = len(current_path)
                        
                    res_f, res_path, res_cost = search(nxt, g + step_cost, threshold, current_path, path_set)
                    
                    # Backtrack (Lùi lại để thử hướng khác)
                    current_path.pop()
                    path_set.remove(nxt)
                    
                    if res_f == "FOUND":
                        return "FOUND", res_path, res_cost
                    if res_f < min_exceeded:
                        min_exceeded = res_f
                        
        return min_exceeded, None, 0

    # Khởi tạo ngưỡng ban đầu bằng đúng khoảng cách chim bay
    threshold = manhattan_distance(start, end)
    
    while True:
        res_f, res_path, res_cost = search(start, 0, threshold, [start], {start})
        
        if res_f == "FOUND":
            return list(res_path), res_cost
        if res_f == float('inf'): # Đã thử mở rộng mọi giới hạn nhưng vẫn không tìm được
            return None, 0
            
        # Nâng ngưỡng (Threshold) lên mức nhỏ nhất bị vượt qua ở lần duyệt trước
        threshold = res_f

def solve_firefighter_ida_star(matrix, start_pos, victims, gates):
    """THUẬT TOÁN CHÍNH: IDA* (Đã sửa logic)"""
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
        
        path_to_victim, cost = ida_star_planning(matrix, current_pos, target_victim, stats)
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
        
        path_to_gate, cost = ida_star_planning(matrix, current_pos, target_gate, stats)
        if not path_to_gate:
            stats['reason'] = f"Đã cứu nạn nhân tại {target_victim} nhưng không thể tìm thấy lối ra cửa thoát hiểm!"
            return rescue_order, full_path, total_cost, stats
            
        full_path.extend(path_to_gate[1:])
        total_cost += cost
        current_pos = target_gate
    
    stats['reason'] = "Giải cứu thành công tất cả nạn nhân!"
    return rescue_order, full_path, total_cost, stats