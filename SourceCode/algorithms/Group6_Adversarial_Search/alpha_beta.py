# -*- coding: utf-8 -*-

def solve_firefighter_alpha_beta(matrix, start_pos, victims, gates):
    """
    Alpha-Beta Pruning: Cắt tỉa các nhánh tốn kém sớm hơn.
    """
    rows, cols = len(matrix), len(matrix[0])
    stats = {'nodes_expanded': 0, 'max_frontier_size': 0, 'total_reached': 1, 'reason': ''}
    
    def get_cost(r, c):
        if matrix[r][c] == 1: return float('inf')
        if matrix[r][c] == 2: return 5 # Đồng bộ chi phí Lửa = 5
        return 1

    def manhattan(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def find_path_alpha_beta(start, target):
        queue = [(start, [start], 0)]
        visited = {start: 0}
        
        if len(queue) > stats['max_frontier_size']: stats['max_frontier_size'] = len(queue)
        
        best_found_cost = float('inf')
        best_path = None
        
        while queue:
            queue.sort(key=lambda x: x[2] + manhattan(x[0], target))
            curr, path, cost = queue.pop(0)
            stats['nodes_expanded'] += 1
            
            # ALPHA-BETA PRUNING: Cắt tỉa nếu nhánh hiện tại đã đắt hơn kết quả tốt nhất tìm được
            if cost + manhattan(curr, target) >= best_found_cost:
                continue 
                
            if curr == target:
                if cost < best_found_cost:
                    best_found_cost = cost
                    best_path = path
                continue
                
            r, c = curr
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    step_cost = get_cost(nr, nc)
                    new_cost = cost + step_cost
                    
                    if step_cost != float('inf'):
                        # Cắt tỉa thêm: Nếu từng đến ô này với chi phí rẻ hơn thì bỏ qua (Alpha)
                        if (nr, nc) not in visited or new_cost < visited[(nr, nc)]:
                            visited[(nr, nc)] = new_cost
                            stats['total_reached'] += 1
                            queue.append(((nr, nc), path + [(nr, nc)], new_cost))
                            
                            if len(queue) > stats['max_frontier_size']: 
                                stats['max_frontier_size'] = len(queue)
                                
        return best_path, (best_found_cost if best_path else 0)

    # Logic giải cứu chính
    current_pos = start_pos
    full_path = [start_pos]
    total_cost = 0
    rescue_order = []
    unrescued = list(victims)
    
    while unrescued:
        # 1. Tìm nạn nhân gần nhất
        unrescued.sort(key=lambda v: manhattan(current_pos, v))
        target_victim = unrescued[0]
        
        path_to_v, cost_to_v = find_path_alpha_beta(current_pos, target_victim)
        if not path_to_v: 
            stats['reason'] = f"Bị chặn đường khi cứu nạn nhân tại {target_victim}!"
            return rescue_order, full_path, total_cost, stats
        
        full_path.extend(path_to_v[1:])
        total_cost += cost_to_v
        rescue_order.append(target_victim)
        unrescued.remove(target_victim)
        current_pos = target_victim
        
        # 2. Tìm cửa thoát hiểm gần nhất
        gates.sort(key=lambda g: manhattan(current_pos, g))
        target_gate = gates[0]
        
        path_to_g, cost_to_g = find_path_alpha_beta(current_pos, target_gate)
        if not path_to_g: 
            stats['reason'] = f"Không tìm thấy đường ra cửa thoát hiểm từ {current_pos}"
            return rescue_order, full_path, total_cost, stats
            
        full_path.extend(path_to_g[1:])
        total_cost += cost_to_g
        current_pos = target_gate

    stats['reason'] = "Giải cứu thành công!"
    return rescue_order, full_path, total_cost, stats