def manhattan_distance(pos1, pos2):
    """Khoảng cách Manhattan (đường chim bay theo ô vuông)"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def get_neighbors(matrix, pos):
    """Lấy các ô xung quanh không bị vướng tường"""
    neighbors = []
    rows, cols = len(matrix), len(matrix[0])
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = pos[0] + dr, pos[1] + dc
        if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] != 1:
            neighbors.append((nr, nc))
    return neighbors

def solve_firefighter_simple_hc(matrix, start_pos, victims, gates):
    """
    SIMPLE HILL CLIMBING: Chỉ chọn bước đi đầu tiên gần đích hơn hiện tại.
    """
    path = [start_pos]
    rescue_order = []
    current_pos = start_pos
    unrescued = list(victims)
    
    nodes_expanded = 0
    max_frontier_size = 1 # Hill Climbing chỉ lưu 1 trạng thái hiện tại
    total_reached = 1
    
    while unrescued:
        # 1. Đi cứu nạn nhân
        unrescued.sort(key=lambda v: manhattan_distance(current_pos, v))
        target_victim = unrescued[0]
        
        while current_pos != target_victim:
            nodes_expanded += 1
            neighbors = get_neighbors(matrix, current_pos)
            total_reached += len(neighbors)
            
            best_neighbor = None
            current_h = manhattan_distance(current_pos, target_victim)
            
            # Chọn ô Hàng xóm đầu tiên có khoảng cách ngắn hơn hiện tại
            for n in neighbors:
                n_h = manhattan_distance(n, target_victim)
                if n_h < current_h:
                    best_neighbor = n
                    break
                    
            if not best_neighbor:
                stats = {"nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size, "total_reached": total_reached, "reason": f"Bị kẹt (Local Optima) - Không có hướng nào gần nạn nhân tại {target_victim} hơn!"}
                return rescue_order, path, len(path) - 1, stats
                
            current_pos = best_neighbor
            path.append(current_pos)
            
        rescue_order.append(target_victim)
        unrescued.remove(target_victim)
        
        # 2. Đưa nạn nhân thoát ra cửa gần nhất
        gates.sort(key=lambda g: manhattan_distance(current_pos, g))
        target_gate = gates[0]
        
        while current_pos != target_gate:
            nodes_expanded += 1
            neighbors = get_neighbors(matrix, current_pos)
            total_reached += len(neighbors)
            
            best_neighbor = None
            current_h = manhattan_distance(current_pos, target_gate)
            
            for n in neighbors:
                if manhattan_distance(n, target_gate) < current_h:
                    best_neighbor = n
                    break
                    
            if not best_neighbor:
                stats = {"nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size, "total_reached": total_reached, "reason": f"Đã cứu nạn nhân tại {target_victim} nhưng bị kẹt (Local Optima) trên đường ra cửa!"}
                return rescue_order, path, len(path) - 1, stats
                
            current_pos = best_neighbor
            path.append(current_pos)
            
    stats = {"nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size, "total_reached": total_reached, "reason": "Giải cứu thành công tất cả nạn nhân!"}
    return rescue_order, path, len(path) - 1, stats