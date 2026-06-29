# -*- coding: utf-8 -*-
from algorithms.Group5_CSP.backtracking import simple_bfs_path

def solve_firefighter_ac3(matrix, start_pos, victims, gates):
    """THUẬT TOÁN CSP 3: AC-3 (RÀNG BUỘC CUNG)"""
    stats = {'assignments': 0, 'backtracks': 0, 'tree_log': [], 'reason': ''}
    n = len(victims)
    
    domains = {i: list(victims) for i in range(1, n + 1)}
    
    # Hàm duy trì tính nhất quán của cung (Arc Consistency)
    def ac3(domains, assigned_var, assigned_val):
        for k in range(1, n + 1):
            if k != assigned_var and assigned_val in domains[k]:
                domains[k].remove(assigned_val)
                stats['tree_log'].append(f"   AC-3: Loại {assigned_val} khỏi miền giá trị lượt {k}")
                if len(domains[k]) == 0:
                    return False # Báo lỗi xung đột
        return True

    def backtrack_ac3(assignment, current_domains):
        stats['assignments'] += 1
        if len(assignment) == n:
            return assignment
            
        current_var = len(assignment) + 1
        
        for victim in current_domains[current_var]:
            stats['tree_log'].append(f"Gán Lượt {current_var} -> {victim}")
            assignment.append(victim)
            
            # Deep copy domain để rollback
            next_domains = {k: list(vals) for k, vals in current_domains.items()}
            next_domains[current_var] = [victim]
            
            # Chạy AC-3 để lọc
            if ac3(next_domains, current_var, victim):
                result = backtrack_ac3(assignment, next_domains)
                if result:
                    return result
                    
            stats['tree_log'].append(f"Quay lui: Hủy Lượt {current_var} do AC-3 bế tắc")
            assignment.pop()
            stats['backtracks'] += 1
            
        return None

    stats['tree_log'].append("GỐC: Bắt đầu dò bằng AC-3...")
    rescue_order = backtrack_ac3([], domains)
    
    if not rescue_order:
        stats['reason'] = "AC-3 phát hiện bế tắc toàn cục."
        return [], [], 0, stats

    # LOGIC VẼ ĐƯỜNG ĐI ĐÃ ĐƯỢC SỬA LẠI
    full_path = [start_pos]
    curr = start_pos
    for v in rescue_order:
        # 1. Đi cứu nạn nhân
        p = simple_bfs_path(matrix, curr, v)
        if not p:
            stats['reason'] = f"CSP đã chọn {v} nhưng thực tế bị tường bít kín!"
            return rescue_order, full_path, len(full_path)-1, stats
        full_path.extend(p[1:])
        curr = v
        
        # 2. Đưa nạn nhân ra cửa thoát hiểm gần nhất
        gates.sort(key=lambda g: abs(curr[0]-g[0]) + abs(curr[1]-g[1]))
        target_gate = gates[0]
        gate_path = simple_bfs_path(matrix, curr, target_gate)
        if not gate_path:
            stats['reason'] = f"Đã cứu nạn nhân tại {v} nhưng không tìm thấy đường ra cửa!"
            return rescue_order, full_path, len(full_path)-1, stats
        full_path.extend(gate_path[1:])
        curr = target_gate # Vị trí mới để đi cứu người tiếp theo là từ cửa
    
    stats['reason'] = "Thành công!"
    return rescue_order, full_path, len(full_path)-1, stats