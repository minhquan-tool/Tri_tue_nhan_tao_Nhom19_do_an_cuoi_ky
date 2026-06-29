from algorithms.Group3_Local_Search.simple_hill_climbing import manhattan_distance, get_neighbors

def solve_firefighter_local_beam(matrix, start_pos, victims, gates):
    K = 3 # Độ rộng Beam (Lưu giữ 3 nhánh tốt nhất mỗi lượt)
    nodes_expanded = 0
    max_frontier_size = K
    total_reached = 1
    
    full_path = [start_pos]
    rescue_order = []
    current_pos = start_pos
    unrescued = list(victims)
    
    def search_segment(start_node, goal_node, current_nodes_expanded, current_total_reached):
        # Beam lưu trữ: [(Vị_trí, Đường_đi)]
        beam = [(start_node, [start_node])]
        
        while beam:
            new_candidates = []
            for pos, path in beam:
                current_nodes_expanded += 1
                
                if pos == goal_node:
                    return path, current_nodes_expanded, current_total_reached
                    
                neighbors = get_neighbors(matrix, pos)
                current_total_reached += len(neighbors)
                
                for n in neighbors:
                    new_candidates.append((n, path + [n]))
                    
            if not new_candidates:
                return None, current_nodes_expanded, current_total_reached
                
            # Đánh giá và lọc ra K ứng viên tốt nhất (Gần đích nhất)
            new_candidates.sort(key=lambda x: manhattan_distance(x[0], goal_node))
            beam = new_candidates[:K]
            
        return None, current_nodes_expanded, current_total_reached

    while unrescued:
        # 1. Đi cứu nạn nhân gần nhất
        unrescued.sort(key=lambda t: manhattan_distance(current_pos, t))
        target_victim = unrescued[0]
        
        segment_path, nodes_expanded, total_reached = search_segment(current_pos, target_victim, nodes_expanded, total_reached)
        
        if not segment_path:
            stats = {"nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size, "total_reached": total_reached, "reason": f"Bị kẹt (Local Optima) - Tất cả {K} tia Beam đều đâm vào ngõ cụt khi cứu nạn nhân tại {target_victim}!"}
            return rescue_order, full_path, len(full_path) - 1, stats
            
        full_path.extend(segment_path[1:])
        current_pos = target_victim
        rescue_order.append(target_victim)
        unrescued.remove(target_victim)
        
        # 2. Đưa nạn nhân ra cửa thoát hiểm gần nhất
        gates.sort(key=lambda g: manhattan_distance(current_pos, g))
        target_gate = gates[0]
        
        segment_path, nodes_expanded, total_reached = search_segment(current_pos, target_gate, nodes_expanded, total_reached)
        
        if not segment_path:
            stats = {"nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size, "total_reached": total_reached, "reason": f"Đã cứu nạn nhân tại {target_victim} nhưng bị kẹt trên đường ra cửa!"}
            return rescue_order, full_path, len(full_path) - 1, stats
            
        full_path.extend(segment_path[1:])
        current_pos = target_gate # Lính cứu hỏa đang đứng ở cửa, chuẩn bị đi cứu người tiếp theo
        
    stats = {"nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size, "total_reached": total_reached, "reason": "Giải cứu thành công tất cả nạn nhân!"}
    return rescue_order, full_path, len(full_path) - 1, stats