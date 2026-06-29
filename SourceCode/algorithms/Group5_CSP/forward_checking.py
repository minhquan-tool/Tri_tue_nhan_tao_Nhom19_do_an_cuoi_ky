# -*- coding: utf-8 -*-
from algorithms.Group5_CSP.backtracking import simple_bfs_path

def solve_firefighter_forward_checking(matrix, start_pos, victims, gates):
    """THUẬT TOÁN CSP 2: FORWARD CHECKING (CẮT TỈA MIỀN GIÁ TRỊ SỚM)"""
    stats = {'assignments': 0, 'backtracks': 0, 'tree_log': [], 'reason': ''}
    n = len(victims)
    
    # Khởi tạo Domain cho N biến (N lượt cứu)
    domains = {i: list(victims) for i in range(1, n + 1)}
    
    def forward_check(assignment, current_domains):
        stats['assignments'] += 1
        if len(assignment) == n:
            return assignment
            
        current_var = len(assignment) + 1
        
        for victim in current_domains[current_var]:
            stats['tree_log'].append(f"FC: Gán Lượt {current_var} -> {victim}")
            assignment.append(victim)
            
            # Cập nhật Domain của các lượt chưa gán (Xóa victim vừa chọn)
            next_domains = {k: [v for v in vals if v != victim] for k, vals in current_domains.items()}
            
            # Kiểm tra xem có Domain nào bị rỗng không (Nếu có -> Cắt nhánh sớm)
            empty_domain_found = False
            for k in range(current_var + 1, n + 1):
                if len(next_domains[k]) == 0:
                    empty_domain_found = True
                    stats['tree_log'].append(f"FC Phát hiện nhánh cụt: Domain lượt {k} bị rỗng!")
                    break
                    
            if not empty_domain_found:
                result = forward_check(assignment, next_domains)
                if result:
                    return result
                    
            stats['tree_log'].append(f"FC Quay lui: Hủy Lượt {current_var}")
            assignment.pop()
            stats['backtracks'] += 1
            
        return None

    stats['tree_log'].append("GỐC: Bắt đầu dò bằng Forward Checking...")
    rescue_order = forward_check([], domains)
    
    if not rescue_order:
        stats['reason'] = "CSP không thể tìm được phép gán."
        return [], [], 0, stats

    # LOGIC VẼ ĐƯỜNG ĐI ĐÃ ĐƯỢC SỬA LẠI
    full_path = [start_pos]
    curr = start_pos
    for v in rescue_order:
        # 1. Đi tới chỗ nạn nhân
        p = simple_bfs_path(matrix, curr, v)
        if not p:
            stats['reason'] = f"CSP đã chọn {v} nhưng thực tế bị tường bít kín!"
            return rescue_order, full_path, len(full_path)-1, stats
        full_path.extend(p[1:])
        curr = v
        
        # 2. Rời nạn nhân ra cửa
        gates.sort(key=lambda g: abs(curr[0]-g[0]) + abs(curr[1]-g[1]))
        target_gate = gates[0]
        gate_path = simple_bfs_path(matrix, curr, target_gate)
        if not gate_path:
            stats['reason'] = f"Đã cứu nạn nhân tại {v} nhưng không thể ra cửa thoát hiểm!"
            return rescue_order, full_path, len(full_path)-1, stats
        full_path.extend(gate_path[1:])
        curr = target_gate
    
    stats['reason'] = "Thành công!"
    return rescue_order, full_path, len(full_path)-1, stats