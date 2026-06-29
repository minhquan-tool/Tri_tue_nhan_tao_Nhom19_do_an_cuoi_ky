import random
from algorithms.Group3_Local_Search.simple_hill_climbing import manhattan_distance

def get_randomized_neighbors(matrix, pos):
    """Lấy các ô xung quanh nhưng TRỘN NGẪU NHIÊN thứ tự duyệt"""
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random.shuffle(directions) # Xáo trộn ngẫu nhiên để tránh đi vào ngõ cụt cũ
    rows, cols = len(matrix), len(matrix[0])
    for dr, dc in directions:
        nr, nc = pos[0] + dr, pos[1] + dc
        if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] != 1:
            neighbors.append((nr, nc))
    return neighbors

def solve_firefighter_random_restart_hc(matrix, start_pos, victims, gates):
    MAX_RESTARTS = 50
    restarts = 0
    nodes_expanded = 0
    total_reached = 1
    
    while restarts < MAX_RESTARTS:
        path = [start_pos]
        rescue_order = []
        current_pos = start_pos
        unrescued = list(victims)
        success = True
        
        while unrescued:
            # 1. Cứu nạn nhân
            unrescued.sort(key=lambda v: manhattan_distance(current_pos, v))
            target_victim = unrescued[0]
            
            while current_pos != target_victim:
                nodes_expanded += 1
                neighbors = get_randomized_neighbors(matrix, current_pos)
                total_reached += len(neighbors)
                
                best_neighbor = None
                current_h = manhattan_distance(current_pos, target_victim)
                
                for n in neighbors:
                    if manhattan_distance(n, target_victim) < current_h:
                        best_neighbor = n
                        break
                        
                if not best_neighbor:
                    success = False
                    break # Bị kẹt
                    
                current_pos = best_neighbor
                path.append(current_pos)
                
            if not success: break
            
            rescue_order.append(target_victim)
            unrescued.remove(target_victim)
            
            # 2. Đưa nạn nhân ra cửa thoát hiểm
            gates.sort(key=lambda g: manhattan_distance(current_pos, g))
            target_gate = gates[0]
            
            while current_pos != target_gate:
                nodes_expanded += 1
                neighbors = get_randomized_neighbors(matrix, current_pos)
                total_reached += len(neighbors)
                
                best_neighbor = None
                current_h = manhattan_distance(current_pos, target_gate)
                
                for n in neighbors:
                    if manhattan_distance(n, target_gate) < current_h:
                        best_neighbor = n
                        break
                        
                if not best_neighbor:
                    success = False
                    break # Bị kẹt trên đường ra cửa
                    
                current_pos = best_neighbor
                path.append(current_pos)
                
            if not success: break
            
        if not success:
            restarts += 1
            continue # Kẹt ở bất kỳ đâu (đường đến nạn nhân hoặc đường ra cửa) thì Start lại toàn bộ
            
        # NẾU TÌM THÀNH CÔNG VÀ KHÔNG BỊ KẸT
        stats = {"nodes_expanded": nodes_expanded, "max_frontier_size": 1, "total_reached": total_reached, "restarts": restarts, "reason": "Giải cứu thành công!"}
        return rescue_order, path, len(path) - 1, stats
            
    stats = {"nodes_expanded": nodes_expanded, "max_frontier_size": 1, "total_reached": total_reached, "restarts": restarts, "reason": f"Đã thử restart lại {MAX_RESTARTS} lần nhưng vẫn bị kẹt (Local Optima)!"}
    return rescue_order, [], 0, stats