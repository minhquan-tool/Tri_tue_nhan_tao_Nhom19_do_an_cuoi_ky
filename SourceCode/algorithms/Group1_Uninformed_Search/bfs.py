# -*- coding: utf-8 -*-
from collections import deque

def bfs_grid_path(matrix, start, end, stats):
    """Tìm đường ngắn nhất (số bước) bằng BFS, bỏ qua trọng số của Lửa."""
    rows, cols = len(matrix), len(matrix[0])
    frontier = deque([(start, [start])])
    reached = {start}

    while frontier:
        if len(frontier) > stats['max_frontier_size']:
            stats['max_frontier_size'] = len(frontier)
            
        curr, path = frontier.popleft()
        stats['nodes_expanded'] += 1
        
        if curr == end:
            return path, len(path) - 1 # Chi phí tính bằng số bước đi

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = curr[0] + dr, curr[1] + dc
            # Tránh ra khỏi bản đồ và tránh Tường (1)
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] != 1:
                nxt = (nr, nc)
                if nxt not in reached:
                    reached.add(nxt)
                    stats['total_reached'] += 1
                    frontier.append((nxt, path + [nxt]))
    return None, float('inf')

def get_nearest_gate_bfs(matrix, start, gates, stats):
    """Tìm cửa thoát hiểm có số bước đi ít nhất."""
    best_gate, best_path, best_cost = None, None, float('inf')
    for g in gates:
        path, cost = bfs_grid_path(matrix, start, g, stats)
        if path and cost < best_cost:
            best_gate, best_path, best_cost = g, path, cost
    return best_gate, best_path, best_cost

def solve_firefighter_bfs(matrix, start_pos, victims, gates):
    """Giải quyết bài toán giải cứu thứ tự nạn nhân bằng BFS."""
    stats = {'nodes_expanded': 0, 'max_frontier_size': 0, 'total_reached': 1, 'reason': ''}
    current_pos = start_pos
    full_path = [start_pos]
    rescue_order = []
    unrescued = list(victims)
    total_cost = 0

    while unrescued:
        # 1. Tìm và đi đến nạn nhân gần nhất
        unrescued.sort(key=lambda v: abs(current_pos[0]-v[0]) + abs(current_pos[1]-v[1]))
        target = unrescued[0]

        path, cost = bfs_grid_path(matrix, current_pos, target, stats)
        if not path:
            stats['reason'] = f"Bị chặn đường! Không thể tìm lối tới nạn nhân tại {target}."
            return rescue_order, full_path, total_cost, stats
        
        full_path.extend(path[1:])
        total_cost += cost
        current_pos = target
        rescue_order.append(target)
        unrescued.remove(target)

        # 2. Đưa nạn nhân ra cửa thoát hiểm bằng hàm phụ trợ bạn đã viết
        gate, path, cost = get_nearest_gate_bfs(matrix, current_pos, gates, stats)
        if not gate:
            stats['reason'] = "Đã cứu xong nhưng không thể tìm thấy lối ra cửa thoát hiểm!"
            return rescue_order, full_path, total_cost, stats
        
        full_path.extend(path[1:])
        total_cost += cost
        current_pos = gate

    stats['reason'] = "Giải cứu thành công tất cả nạn nhân!"
    return rescue_order, full_path, total_cost, stats