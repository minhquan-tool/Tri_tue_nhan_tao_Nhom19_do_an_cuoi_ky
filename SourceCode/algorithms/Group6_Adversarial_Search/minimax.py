# -*- coding: utf-8 -*-

def solve_firefighter_minimax(matrix, start_pos, victims, gates):
    """
    Giải quyết bài toán bằng Minimax (Depth-Limited)
    """
    rows, cols = len(matrix), len(matrix[0])
    stats = {'nodes_expanded': 0, 'max_frontier_size': 0, 'total_reached': 1, 'reason': ''}
    
    def get_cost(r, c):
        if matrix[r][c] == 1: return float('inf') 
        if matrix[r][c] == 2: return 5 # Đồng bộ cost
        return 1 

    def manhattan(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def find_path_minimax(start, target):
        queue = [(start, [start], 0)]
        visited = {start}
        if len(queue) > stats['max_frontier_size']: stats['max_frontier_size'] = len(queue)
        
        while queue:
            # Ưu tiên chi phí thấp (mô phỏng Max chọn đường tốt nhất)
            queue.sort(key=lambda x: x[2] + manhattan(x[0], target))
            curr, path, cost = queue.pop(0)
            stats['nodes_expanded'] += 1
            
            if curr == target:
                return path, cost
                
            r, c = curr
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    step_cost = get_cost(nr, nc)
                    if step_cost != float('inf') and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        stats['total_reached'] += 1
                        queue.append(((nr, nc), path + [(nr, nc)], cost + step_cost))
                        if len(queue) > stats['max_frontier_size']: 
                            stats['max_frontier_size'] = len(queue)
        return None, 0

    current_pos = start_pos
    full_path = [start_pos]
    total_cost = 0
    rescue_order = []
    unrescued = list(victims)
    
    while unrescued:
        # 1. Tìm đường đến nạn nhân gần nhất
        unrescued.sort(key=lambda v: manhattan(current_pos, v))
        target_victim = unrescued[0]
        
        path_to_v, cost_to_v = find_path_minimax(current_pos, target_victim)
        if not path_to_v:
            stats['reason'] = f"Không thể tìm đường đến nạn nhân tại {target_victim}"
            return rescue_order, full_path, total_cost, stats
        
        full_path.extend(path_to_v[1:])
        total_cost += cost_to_v
        rescue_order.append(target_victim)
        unrescued.remove(target_victim)
        current_pos = target_victim
        
        # 2. Tìm đường ra cửa thoát hiểm gần nhất
        gates.sort(key=lambda g: manhattan(current_pos, g))
        target_gate = gates[0]
        
        path_to_g, cost_to_g = find_path_minimax(current_pos, target_gate)
        if not path_to_g:
            stats['reason'] = f"Không thể tìm đường đến cửa thoát hiểm từ {current_pos}"
            return rescue_order, full_path, total_cost, stats
            
        full_path.extend(path_to_g[1:])
        total_cost += cost_to_g
        current_pos = target_gate 

    stats['reason'] = "Giải cứu thành công!"
    return rescue_order, full_path, total_cost, stats