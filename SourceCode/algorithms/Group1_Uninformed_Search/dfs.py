# -*- coding: utf-8 -*-

def dfs_grid_path(matrix, start, end, stats):
    """Tìm đường bằng DFS, bỏ qua trọng số của Lửa. (Không đảm bảo ngắn nhất)"""
    rows, cols = len(matrix), len(matrix[0])
    frontier = [(start, [start])] # Stack
    reached = {start}

    while frontier:
        if len(frontier) > stats['max_frontier_size']:
            stats['max_frontier_size'] = len(frontier)
            
        curr, path = frontier.pop() # Lấy phần tử cuối cùng ra
        stats['nodes_expanded'] += 1
        
        if curr == end:
            return path, len(path) - 1

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = curr[0] + dr, curr[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] != 1:
                nxt = (nr, nc)
                if nxt not in reached:
                    reached.add(nxt)
                    stats['total_reached'] += 1
                    frontier.append((nxt, path + [nxt]))
    return None, float('inf')

def get_nearest_gate_dfs(matrix, start, gates, stats):
    """Lấy cửa thoát hiểm đầu tiên tìm thấy được bằng DFS."""
    best_gate, best_path, best_cost = None, None, float('inf')
    for g in gates:
        path, cost = dfs_grid_path(matrix, start, g, stats)
        if path and cost < best_cost:
            best_gate, best_path, best_cost = g, path, cost
    return best_gate, best_path, best_cost

def solve_firefighter_dfs(matrix, start_pos, victims, gates):
    """Giải quyết bài toán bằng DFS."""
    stats = {'nodes_expanded': 0, 'max_frontier_size': 0, 'total_reached': 1, 'reason': ''}
    current_pos = start_pos
    full_path = [start_pos]
    rescue_order = []
    unrescued = list(victims)
    total_cost = 0

    while unrescued:
        # 1. Đi đến nạn nhân gần nhất
        unrescued.sort(key=lambda v: abs(current_pos[0]-v[0]) + abs(current_pos[1]-v[1]))
        target = unrescued[0]

        path, cost = dfs_grid_path(matrix, current_pos, target, stats)
        if not path:
            stats['reason'] = f"Bị chặn đường! Không thể tìm lối tới nạn nhân tại {target}."
            return rescue_order, full_path, total_cost, stats
        
        full_path.extend(path[1:])
        total_cost += cost
        current_pos = target
        rescue_order.append(target)
        unrescued.remove(target)

        # 2. Đưa ra cửa bằng DFS
        gate, path, cost = get_nearest_gate_dfs(matrix, current_pos, gates, stats)
        if not gate:
            stats['reason'] = "Đã cứu xong nhưng không thể tìm thấy lối ra cửa thoát hiểm!"
            return rescue_order, full_path, total_cost, stats
        
        full_path.extend(path[1:])
        total_cost += cost
        current_pos = gate

    stats['reason'] = "Giải cứu thành công tất cả nạn nhân!"
    return rescue_order, full_path, total_cost, stats