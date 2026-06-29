# -*- coding: utf-8 -*-
import heapq

def ucs_grid_path(matrix, start, end, stats):
    """Tìm đường bằng UCS, tính trọng số Lửa (5) và Bình thường (1)."""
    rows, cols = len(matrix), len(matrix[0])
    # Priority Queue lưu: (chi_phí, vị_trí, đường_đi)
    frontier = [(0, start, [start])]
    reached = {} # Lưu vị trí và chi phí thấp nhất để đến đó

    while frontier:
        if len(frontier) > stats['max_frontier_size']:
            stats['max_frontier_size'] = len(frontier)
            
        curr_cost, curr, path = heapq.heappop(frontier)
        stats['nodes_expanded'] += 1
        
        # Kiểm tra đích muộn để đảm bảo chi phí thấp nhất
        if curr == end:
            return path, curr_cost
            
        if curr in reached and reached[curr] < curr_cost:
            continue
        reached[curr] = curr_cost

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = curr[0] + dr, curr[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] != 1:
                nxt = (nr, nc)
                # Tính chi phí: Lửa(2) = 5, Trống(0) = 1
                step_cost = 5 if matrix[nr][nc] == 2 else 1
                new_cost = curr_cost + step_cost
                
                if nxt not in reached or new_cost < reached[nxt]:
                    reached[nxt] = new_cost
                    stats['total_reached'] += 1
                    heapq.heappush(frontier, (new_cost, nxt, path + [nxt]))
    return None, float('inf')

def get_nearest_gate_ucs(matrix, start, gates, stats):
    """Tìm cửa thoát hiểm ít tốn sức lực nhất."""
    best_gate, best_path, best_cost = None, None, float('inf')
    for g in gates:
        path, cost = ucs_grid_path(matrix, start, g, stats)
        if path and cost < best_cost:
            best_gate, best_path, best_cost = g, path, cost
    return best_gate, best_path, best_cost

def solve_firefighter_ucs(matrix, start_pos, victims, gates):
    """Giải quyết bài toán vĩ mô bằng UCS (Ưu tiên tổng chi phí thấp nhất)."""
    stats = {'nodes_expanded': 0, 'max_frontier_size': 0, 'total_reached': 1, 'reason': ''}
    current_pos = start_pos
    full_path = [start_pos]
    rescue_order = []
    unrescued = list(victims)
    total_cost = 0

    while unrescued:
        # 1. Tìm nạn nhân gần nhất
        unrescued.sort(key=lambda v: abs(current_pos[0]-v[0]) + abs(current_pos[1]-v[1]))
        target = unrescued[0]

        path, cost = ucs_grid_path(matrix, current_pos, target, stats)
        if not path:
            stats['reason'] = f"Bị chặn đường! Không thể tìm lối tới nạn nhân tại {target}."
            return rescue_order, full_path, total_cost, stats
        
        full_path.extend(path[1:])
        total_cost += cost
        current_pos = target
        rescue_order.append(target)
        unrescued.remove(target)

        # 2. Đưa ra cửa ưu tiên chi phí thấp nhất bằng UCS
        gate, path, cost = get_nearest_gate_ucs(matrix, current_pos, gates, stats)
        if not gate:
            stats['reason'] = "Đã cứu xong nhưng không thể tìm thấy lối ra cửa thoát hiểm!"
            return rescue_order, full_path, total_cost, stats
        
        full_path.extend(path[1:])
        total_cost += cost
        current_pos = gate

    stats['reason'] = "Giải cứu thành công tất cả nạn nhân!"
    return rescue_order, full_path, total_cost, stats