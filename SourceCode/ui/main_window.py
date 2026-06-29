import time
import traceback
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QPen, QBrush

from ui.panels.left_panel import LeftPanel
from ui.panels.right_panel import RightPanel
from ui.panels.bottom_panel import BottomPanel
from ui.views.simulation_view import SimulationView

# =====================================================================
# IMPORT AN TOÀN (CHỐNG VĂNG APP NẾU THIẾU FILE)
# =====================================================================
# Nhóm 1
try:
    from algorithms.Group1_Uninformed_Search.bfs import solve_firefighter_bfs
    from algorithms.Group1_Uninformed_Search.dfs import solve_firefighter_dfs
    from algorithms.Group1_Uninformed_Search.ucs import solve_firefighter_ucs
except Exception as e:
    solve_firefighter_bfs = solve_firefighter_dfs = solve_firefighter_ucs = None
    
# Nhóm 2
try:
    from algorithms.Group2_Informed_Search.a_star import solve_firefighter_a_star
    from algorithms.Group2_Informed_Search.greedy_best_first import solve_firefighter_greedy
    from algorithms.Group2_Informed_Search.ida_star import solve_firefighter_ida_star
except Exception as e:
    solve_firefighter_a_star = solve_firefighter_greedy = solve_firefighter_ida_star = None

# Nhóm 3
try:
    from algorithms.Group3_Local_Search.simple_hill_climbing import solve_firefighter_simple_hc
    from algorithms.Group3_Local_Search.random_restart_hill_climbing import solve_firefighter_random_restart_hc
    from algorithms.Group3_Local_Search.local_beam_search import solve_firefighter_local_beam
except Exception as e:
    solve_firefighter_simple_hc = solve_firefighter_random_restart_hc = solve_firefighter_local_beam = None

# Nhóm 4
try:
    from algorithms.Group4_Partial_Sensorless_Search.bfs_sensorless import solve_sensorless_bfs
    from algorithms.Group4_Partial_Sensorless_Search.dfs_sensorless import solve_sensorless_dfs
    from algorithms.Group4_Partial_Sensorless_Search.ucs_partially_observable import solve_partially_observable_ucs
except Exception as e:
    solve_sensorless_bfs = solve_sensorless_dfs = solve_partially_observable_ucs = None

# Nhóm 5 (CSP)
try:
    from algorithms.Group5_CSP.backtracking import solve_firefighter_backtracking
    from algorithms.Group5_CSP.forward_checking import solve_firefighter_forward_checking
    from algorithms.Group5_CSP.ac3 import solve_firefighter_ac3
except Exception as e:
    solve_firefighter_backtracking = solve_firefighter_forward_checking = solve_firefighter_ac3 = None

# Nhóm 6
try:
    from algorithms.Group6_Adversarial_Search.minimax import solve_firefighter_minimax
    from algorithms.Group6_Adversarial_Search.alpha_beta import solve_firefighter_alpha_beta
    from algorithms.Group6_Adversarial_Search.expectimax import solve_firefighter_expectimax
except Exception as e:
    solve_firefighter_minimax = solve_firefighter_alpha_beta = solve_firefighter_expectimax = None
    
# =====================================================================
# LUỒNG PHỤ (WORKER) XỬ LÝ THUẬT TOÁN 
# =====================================================================
class SimulationWorker(QThread):
    log_signal = pyqtSignal(str, str)            
    step_signal = pyqtSignal(int, int)            
    finished_signal = pyqtSignal(object, object, float)
    csp_order_signal = pyqtSignal(list) # Signal báo cáo thứ tự CSP ra UI đánh số

    def __init__(self, algo_name, matrix, start_pos, victims, gates):
        super().__init__()
        self.algo_name = algo_name
        self.matrix = matrix
        self.start_pos = start_pos
        self.victims = victims
        self.gates = gates

    def run(self):
        try:
            self.log_signal.emit(f"Bắt đầu tính toán: {self.algo_name}...", "yellow")
            start_time = time.time()
            
            result = None
            is_csp = any(kw in self.algo_name for kw in ["Backtracking", "Forward Checking", "AC-3"])
            is_adversarial = any(kw in self.algo_name for kw in ["Minimax", "Alpha-Beta", "Expectimax"])
            
            # --- ĐIỀU HƯỚNG NHÓM 1 ---
            if "BFS" in self.algo_name and "Sensorless" not in self.algo_name and "Partially" not in self.algo_name:
                if solve_firefighter_bfs: result = solve_firefighter_bfs(self.matrix, self.start_pos, self.victims, self.gates)
            elif "DFS" in self.algo_name and "Sensorless" not in self.algo_name and "Partially" not in self.algo_name:
                if solve_firefighter_dfs: result = solve_firefighter_dfs(self.matrix, self.start_pos, self.victims, self.gates)
            elif "UCS" in self.algo_name and "Partially" not in self.algo_name and "Sensorless" not in self.algo_name:
                if solve_firefighter_ucs: result = solve_firefighter_ucs(self.matrix, self.start_pos, self.victims, self.gates)
                
            # --- ĐIỀU HƯỚNG NHÓM 2 (INFORMED SEARCH) ---
            elif "A*" in self.algo_name:
                if solve_firefighter_a_star: result = solve_firefighter_a_star(self.matrix, self.start_pos, self.victims, self.gates)
            elif "Greedy" in self.algo_name:
                if solve_firefighter_greedy: result = solve_firefighter_greedy(self.matrix, self.start_pos, self.victims, self.gates)
            elif "IDA*" in self.algo_name:
                if solve_firefighter_ida_star: result = solve_firefighter_ida_star(self.matrix, self.start_pos, self.victims, self.gates)
                
            # --- ĐIỀU HƯỚNG NHÓM 3 ---
            elif "Simple" in self.algo_name:
                if solve_firefighter_simple_hc: result = solve_firefighter_simple_hc(self.matrix, self.start_pos, self.victims, self.gates)
            elif "Random Restart" in self.algo_name:
                if solve_firefighter_random_restart_hc: result = solve_firefighter_random_restart_hc(self.matrix, self.start_pos, self.victims, self.gates)
            elif "Beam" in self.algo_name:
                if solve_firefighter_local_beam: result = solve_firefighter_local_beam(self.matrix, self.start_pos, self.victims, self.gates)

            # --- ĐIỀU HƯỚNG NHÓM 4 ---
            elif "Sensorless BFS" in self.algo_name:
                if solve_sensorless_bfs: result = solve_sensorless_bfs(self.matrix, self.start_pos, self.victims, self.gates)
            elif "Sensorless DFS" in self.algo_name:
                if solve_sensorless_dfs: result = solve_sensorless_dfs(self.matrix, self.start_pos, self.victims, self.gates)
            elif "Partially Observable UCS" in self.algo_name:
                if solve_partially_observable_ucs: result = solve_partially_observable_ucs(self.matrix, self.start_pos, self.victims, self.gates)

            # --- ĐIỀU HƯỚNG NHÓM 5 (CSP) ---
            elif "Backtracking" in self.algo_name:
                if solve_firefighter_backtracking: result = solve_firefighter_backtracking(self.matrix, self.start_pos, self.victims, self.gates)
            elif "Forward Checking" in self.algo_name:
                if solve_firefighter_forward_checking: result = solve_firefighter_forward_checking(self.matrix, self.start_pos, self.victims, self.gates)
            elif "AC-3" in self.algo_name or "Constraint Propagation" in self.algo_name:
                if solve_firefighter_ac3: result = solve_firefighter_ac3(self.matrix, self.start_pos, self.victims, self.gates)
            
            # --- ĐIỀU HƯỚNG NHÓM 6 (ADVERSARIAL SEARCH) ---
            elif "Minimax" in self.algo_name:
                if solve_firefighter_minimax: result = solve_firefighter_minimax(self.matrix, self.start_pos, self.victims, self.gates)
            elif "Alpha-Beta" in self.algo_name:
                if solve_firefighter_alpha_beta: result = solve_firefighter_alpha_beta(self.matrix, self.start_pos, self.victims, self.gates)
            elif "Expectimax" in self.algo_name:
                if solve_firefighter_expectimax: result = solve_firefighter_expectimax(self.matrix, self.start_pos, self.victims, self.gates)

            # --- XỬ LÝ KẾT QUẢ TRẢ VỀ ---
            if result is None:
                self.log_signal.emit("❌ Thuật toán chưa được liên kết hoặc file bị thiếu!", "red")
                self.finished_signal.emit(0, 0, 0.0)
                return

            if len(result) == 4:
                # Xử lý linh hoạt nếu thuật toán Nhóm 6 vẫn trả về (path, order, cost, err_msg) thay vì dict stats
                if isinstance(result[3], str):
                    path_res, order_res, cost_res, err_res = result
                    order, path, cost = order_res, path_res, cost_res
                    stats = {'reason': err_res} if err_res else {}
                else:
                    order, path, cost, stats = result
            elif len(result) == 3:
                order, path, cost = result
                stats = {}
            else:
                self.log_signal.emit("❌ Lỗi: Thuật toán trả về sai định dạng!", "red")
                self.finished_signal.emit(0, 0, 0.0)
                return

            execution_time = (time.time() - start_time) * 1000 

            # ================================================================
            # XỬ LÝ KHI KHÔNG TÌM ĐƯỢC ĐƯỜNG ĐI (THẤT BẠI)
            # ================================================================
            if not path:
                self.log_signal.emit("<br>--------------------------------------------------", "white")
                reason_msg = stats.get('reason', "Không tìm thấy đường đi khả thi lên mục tiêu.")
                self.log_signal.emit(f"❌ THẤT BẠI: {reason_msg}", "red")
                
                # NẾU LÀ CSP THÌ IN CÂY BACKTRACKING NGAY CẢ KHI THẤT BẠI
                if is_csp:
                    self.log_signal.emit("<br><b>[CÂY TÌM KIẾM BACKTRACKING (CSP LOG)]</b>", "cyan")
                    for log_msg in stats.get('tree_log', []):
                        if "❌" in log_msg or "Hủy" in log_msg: self.log_signal.emit(f"  {log_msg}", "red")
                        elif "⚠️" in log_msg or "cụt" in log_msg: self.log_signal.emit(f"  {log_msg}", "yellow")
                        elif "Thử" in log_msg or "Gán" in log_msg or "AC-3" in log_msg: self.log_signal.emit(f"  {log_msg}", "white")
                        else: self.log_signal.emit(f"  {log_msg}", "green")
                elif is_adversarial:
                    self.log_signal.emit("<br><b>[THÔNG SỐ ĐỐI KHÁNG TRƯỚC KHI DỪNG]</b>", "cyan")
                    self.log_signal.emit("  > Môi trường đã chặn mọi đường đi khả thi (Nút MIN/CHANCE chiến thắng).", "yellow")
                    if stats:
                        self.log_signal.emit(f"  > Số trạng thái đã xét: {stats.get('nodes_expanded', 0)}", "yellow")
                elif stats:
                    self.log_signal.emit("<br><b>📊 [THÔNG SỐ TRƯỚC KHI THẤT BẠI]</b>", "cyan")
                    self.log_signal.emit(f"  > Số nút đã mở rộng (Nodes Expanded): {stats.get('nodes_expanded', 0)}", "yellow")
                    self.log_signal.emit(f"  > Biên tìm kiếm lớn nhất (Max Frontier): {stats.get('max_frontier_size', 0)}", "yellow")
                    self.log_signal.emit(f"  > Tổng số nút đã tiếp cận (Total Reached): {stats.get('total_reached', 0)}", "yellow")
                
                self.finished_signal.emit(0, 0, execution_time)
                return

            # ================================================================
            # IN THÔNG SỐ LOG CHI TIẾT RA MÀN HÌNH UI (KHI THÀNH CÔNG)
            # ================================================================
            # Lọc riêng Log và Stats cho Nhóm 5 CSP
            if is_csp:
                self.log_signal.emit("<br><b>[CÂY TÌM KIẾM BACKTRACKING (CSP LOG)]</b>", "cyan")
                for log_msg in stats.get('tree_log', []):
                    if "❌" in log_msg or "Hủy" in log_msg: self.log_signal.emit(f"  {log_msg}", "red")
                    elif "⚠️" in log_msg or "cụt" in log_msg: self.log_signal.emit(f"  {log_msg}", "yellow")
                    elif "Thử" in log_msg or "Gán" in log_msg or "AC-3" in log_msg: self.log_signal.emit(f"  {log_msg}", "white")
                    else: self.log_signal.emit(f"  {log_msg}", "green")
                    
                self.log_signal.emit("<br><b>[THÔNG SỐ ĐẶC TRƯNG CSP]</b>", "cyan")
                self.log_signal.emit(f"  > Số lượt Gán (Assignments): {stats.get('assignments', 0)}", "yellow")
                self.log_signal.emit(f"  > Số lượt Quay lui (Backtracks): {stats.get('backtracks', 0)}", "yellow")
                
                # Gửi Signal hiển thị UI số thứ tự nạn nhân
                if order:
                    self.csp_order_signal.emit(order)
            
            # Lọc riêng Log cho Nhóm 6 Adversarial Search
            elif is_adversarial:
                self.log_signal.emit("<br><b>[THÔNG SỐ TÌM KIẾM ĐỐI KHÁNG - NHÓM 6]</b>", "cyan")
                self.log_signal.emit("  > Môi trường (Lửa, Tường) đóng vai trò: MIN Node / CHANCE Node.", "white")
                self.log_signal.emit("  > Lính cứu hỏa đóng vai trò: MAX Node (Tối ưu hóa hành động cứu hộ).", "white")
                if stats:
                    self.log_signal.emit(f"  > Trạng thái đã duyệt (Visited States): {stats.get('nodes_expanded', 0)}", "yellow")
                    if "Alpha-Beta" in self.algo_name:
                        self.log_signal.emit(f"  > Cắt tỉa (Pruning): Cắt bỏ {stats.get('pruned_branches', 'nhiều')} nhánh kém hiệu quả.", "green")
                    elif "Expectimax" in self.algo_name:
                        self.log_signal.emit("  > Kỳ vọng (Expected Value): Đã ưu tiên các nhánh có rủi ro lửa thấp hơn.", "green")

            else:
                self.log_signal.emit("<br><b>📊 [THÔNG SỐ ĐẶC TRƯNG CỦA THUẬT TOÁN]</b>", "cyan")
                if stats:
                    self.log_signal.emit(f"  > Số nút đã mở rộng (Nodes Expanded): {stats.get('nodes_expanded', 0)}", "yellow")
                    self.log_signal.emit(f"  > Biên tìm kiếm lớn nhất (Max Frontier/Queue/Stack): {stats.get('max_frontier_size', 0)}", "yellow")
                    self.log_signal.emit(f"  > Tổng số nút đã tiếp cận (Total Reached): {stats.get('total_reached', 0)}", "yellow")
                else:
                    self.log_signal.emit("  > Thuật toán này chưa hỗ trợ thống kê Node/Frontier.", "red")

            self.log_signal.emit("<br><b>[KẾT QUẢ GIẢI CỨU]</b>", "cyan")
            if order:
                self.log_signal.emit(f"  > Thứ tự nạn nhân được cứu: {order}", "white")
            
            self.log_signal.emit(f"  > Tổng số bước di chuyển: {len(path) - 1} bước", "white")
            self.log_signal.emit(f"  > Tổng chi phí hành trình (Cost): {cost}", "white")
            self.log_signal.emit(f"  > Đường đi chi tiết: {path}", "green")
            self.log_signal.emit("<br>--------------------------------------------------", "white")

            self.log_signal.emit("Đang mô phỏng bước đi...", "cyan")
            for position in path:
                self.step_signal.emit(position[0], position[1])
                time.sleep(0.15) 

            self.log_signal.emit("✅ Hoàn thành xuất sắc!", "green")
            self.finished_signal.emit(cost, len(path) - 1, execution_time)

        except Exception as e:
            err_msg = traceback.format_exc()
            self.log_signal.emit(f"❌ CRASH THUẬT TOÁN: {str(e)}", "red")
            print(err_msg)
            self.finished_signal.emit(0, 0, 0.0)

# =====================================================================
# GIAO DIỆN CHÍNH
# =====================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Firefighter Rescue AI Simulation")
        self.setGeometry(100, 100, 1400, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.h_splitter = QSplitter(Qt.Horizontal)
        self.left_panel = LeftPanel()
        self.simulation_view = SimulationView()
        self.right_panel = RightPanel()

        self.h_splitter.addWidget(self.left_panel)
        self.h_splitter.addWidget(self.simulation_view)
        self.h_splitter.addWidget(self.right_panel)
        self.h_splitter.setSizes([280, 840, 280])

        self.bottom_panel = BottomPanel()
        self.main_layout.addWidget(self.h_splitter, stretch=4)
        self.main_layout.addWidget(self.bottom_panel, stretch=1)

        self.selected_algo = None  
        self.worker = None
        self.revealed_cells = set()
        self.current_csp_order = [] 

        self.left_panel.tree.itemClicked.connect(self.on_tree_item_clicked)
        self.bottom_panel.btn_start.clicked.connect(self.run_simulation)
        self.bottom_panel.btn_random.clicked.connect(self.generate_new_map)

    def generate_new_map(self):
        try:
            rows = self.bottom_panel.spin_rows.value()
            cols = self.bottom_panel.spin_cols.value()
            victims = self.bottom_panel.spin_victims.value()
            fires = self.bottom_panel.spin_fire.value()

            self.bottom_panel.lbl_victims_progress.setText(f"Nạn nhân đã cứu: 0/{victims}")
            self.bottom_panel.lbl_cost.setText("Tổng chi phí: 0")
            self.bottom_panel.lbl_path.setText("Độ dài đường đi: 0 bước")
            
            self.current_csp_order = []
            if hasattr(self.simulation_view, 'display_csp_order'):
                self.simulation_view.display_csp_order([])
            
            self.simulation_view.generate_random_map_with_params(rows, cols, victims, fires)
            self.right_panel.log(f"Đã tạo bản đồ mới {rows}x{cols}", "white")    
        except Exception as e:
            self.right_panel.log(f"Lỗi tạo map: {str(e)}", "red")

    def on_tree_item_clicked(self, item, column):
        text = item.text(column)
        
        valid_keywords = ["BFS", "DFS", "UCS", "A*", "Greedy", "IDA*", "Simple", "Random", "Beam", "Sensorless", "Partially", "Backtracking", "Forward", "AC-3", "Minimax", "Alpha-Beta", "Expectimax"]
        if any(keyword in text for keyword in valid_keywords):
            self.selected_algo = text
            self.right_panel.log(f"Đã chọn thuật toán: {text}", "yellow")

        # Đổi View (Map được giữ nguyên)
        if "So sánh Nhóm 1" in text:
            if hasattr(self.simulation_view, 'view_comparison'): self.simulation_view.view_comparison.set_current_group(1)
            self.simulation_view.change_view("comparison")
        elif "So sánh Nhóm 2" in text:
            if hasattr(self.simulation_view, 'view_comparison'): self.simulation_view.view_comparison.set_current_group(2)
            self.simulation_view.change_view("comparison")
        elif "So sánh Nhóm 3" in text:
            if hasattr(self.simulation_view, 'view_comparison'): self.simulation_view.view_comparison.set_current_group(3)
            self.simulation_view.change_view("comparison")
        elif "So sánh Nhóm 4" in text:
            if hasattr(self.simulation_view, 'view_comparison'): self.simulation_view.view_comparison.set_current_group(4)
            self.simulation_view.change_view("comparison")
        elif "So sánh Nhóm 5" in text:
            if hasattr(self.simulation_view, 'view_comparison'): self.simulation_view.view_comparison.set_current_group(5)
            self.simulation_view.change_view("comparison")
        elif "So sánh Nhóm 6" in text:
            if hasattr(self.simulation_view, 'view_comparison'): self.simulation_view.view_comparison.set_current_group(6)
            self.simulation_view.change_view("comparison")
        elif "So sánh" in text or "📈" in text:
            if hasattr(self.simulation_view, 'view_comparison'): self.simulation_view.view_comparison.set_current_group(0)
            self.simulation_view.change_view("comparison")
        elif "Sensorless" in text or "Partially" in text:
            self.simulation_view.change_view("sensorless")
        elif "Backtracking" in text or "Forward" in text or "AC-3" in text:
            self.simulation_view.change_view("csp")
        else:
            self.simulation_view.change_view("standard")
            
        # Reset lại thông số dưới thanh Bottom Panel cho sạch sẽ
        self.bottom_panel.lbl_cost.setText("Tổng chi phí: 0")
        self.bottom_panel.lbl_path.setText("Độ dài đường đi: 0 bước")
        self.bottom_panel.lbl_time.setText("Thời gian: 0 ms")

    def run_simulation(self):
        try:
            if not self.selected_algo:
                self.right_panel.log("⚠️ Vui lòng chọn một thuật toán!", "yellow")
                return

            self.bottom_panel.btn_start.setEnabled(False)
            self.bottom_panel.btn_random.setEnabled(False)
            self.left_panel.setEnabled(False)

            # Lấy bản đồ nguyên gốc đã sinh ra từ trước
            matrix, start_pos, victims, gates = self.parse_map_from_ui(self.simulation_view)
            
            if not matrix:
                self.right_panel.log("⚠️ Bản đồ trống!", "red")
                self.on_simulation_finished(0, 0, 0)
                return

            self.sim_matrix = matrix
            self.sim_victims_on_map = list(victims) # Danh sách nạn nhân đang ở trên bản đồ
            self.sim_gates = gates
            self.total_victims_count = len(victims)
            
            self.carried_victim = None # Trạng thái chứa nạn nhân trên lưng
            self.total_saved = 0       # Tổng số người được đưa ra cửa
            self.bottom_panel.lbl_victims_progress.setText(f"Nạn nhân đã cứu: 0/{self.total_victims_count}")
            
            self.current_csp_order = []
            if hasattr(self.simulation_view, 'display_csp_order'):
                self.simulation_view.display_csp_order([])

            self.revealed_cells = set()
            if start_pos:
                self.revealed_cells.add((start_pos[0], start_pos[1]))
            
            self.worker = SimulationWorker(self.selected_algo, matrix, start_pos, victims, gates)
            self.worker.log_signal.connect(self.right_panel.log)
            self.worker.step_signal.connect(self.update_simulation_step)
            self.worker.csp_order_signal.connect(self.display_csp_ui_labels) 
            self.worker.finished_signal.connect(self.on_simulation_finished)
            
            self.worker.start()
        except Exception as e:
            self.right_panel.log(f"❌ Lỗi khi ấn nút bắt đầu: {str(e)}", "red")
            self.on_simulation_finished(0, 0, 0)

    def display_csp_ui_labels(self, order):
        self.current_csp_order = order 
        if hasattr(self.simulation_view, 'display_csp_order'):
            self.simulation_view.display_csp_order(order)

    def update_simulation_step(self, r, c):
        try:
            # Chọn View hiện tại để vẽ
            idx = self.simulation_view.stacked_widget.currentIndex()
            if idx == 0: view = self.simulation_view.view_standard
            elif idx == 1: view = self.simulation_view.view_sensorless
            elif idx == 2: view = self.simulation_view.view_csp
            else: return

            view.scene.clear() 
            
            w, h = view.view.width(), view.view.height()
            rows, cols = len(self.sim_matrix), len(self.sim_matrix[0])
            
            cell_w = w / cols if cols > 0 else 40
            cell_h = h / rows if rows > 0 else 40
            cell_size = max(10, int(min(cell_w, cell_h) * 0.95))
            
            offset_x = (w - cols * cell_size) / 2
            offset_y = (h - rows * cell_size) / 2
            view.scene.setSceneRect(0, 0, w, h)
            
            # --- LOGIC CÕNG NẠN NHÂN VÀ ĐƯA RA CỬA ---
            # 1. Bắt gặp nạn nhân -> Cõng lên lưng (nhặt khỏi bản đồ)
            if (r, c) in self.sim_victims_on_map and self.carried_victim is None:
                self.sim_victims_on_map.remove((r, c))
                self.carried_victim = (r, c)

            # 2. Bước vào cửa và đang cõng người -> Nạn nhân biến mất hoàn toàn
            if (r, c) in self.sim_gates and self.carried_victim is not None:
                self.carried_victim = None
                self.total_saved += 1
                self.bottom_panel.lbl_victims_progress.setText(f"Nạn nhân đã cứu: {self.total_saved}/{self.total_victims_count}")

            if self.selected_algo and ("Sensorless" in self.selected_algo or "Partially" in self.selected_algo):
                if "Partially" in self.selected_algo:
                    for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                        self.revealed_cells.add((r + dr, c + dc))
                else:
                    self.revealed_cells.add((r, c))

            for i in range(rows):
                for j in range(cols):
                    cell_type = "empty"
                    if self.sim_matrix[i][j] == 1: cell_type = "wall"
                    elif self.sim_matrix[i][j] == 2: cell_type = "fire"
                    elif (i, j) in self.sim_victims_on_map: cell_type = "victim"
                    elif (i, j) in self.sim_gates: cell_type = "exit" 
                    
                    x = offset_x + j * cell_size
                    y = offset_y + i * cell_size
                    
                    # Vẽ nền Base
                    view.scene.addRect(x, y, cell_size, cell_size, QPen(QColor("#313244")), QBrush(view.colors["empty"]))
                    
                    # Vẽ đối tượng tĩnh
                    if cell_type != "empty":
                        if hasattr(view, 'pixmaps') and cell_type in view.pixmaps and view.pixmaps[cell_type] is not None:
                            pixmap = view.pixmaps[cell_type].scaled(cell_size - 6, cell_size - 6, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            item = view.scene.addPixmap(pixmap)
                            item.setPos(x + 3, y + 3)
                        else:
                            color = view.colors.get(cell_type, QColor("#1e1e2e"))
                            view.scene.addRect(x + 2, y + 2, cell_size - 4, cell_size - 4, QPen(Qt.NoPen), QBrush(color))
                        
                    # Giao diện Mù (Sương mù)
                    if self.selected_algo and ("Sensorless" in self.selected_algo or "Partially" in self.selected_algo):
                        if (i, j) not in self.revealed_cells:
                            fog_color = QColor(20, 20, 30, 240)
                            view.scene.addRect(x, y, cell_size, cell_size, QPen(Qt.NoPen), QBrush(fog_color))

                    # Vẽ Lính Cứu Hỏa
                    if i == r and j == c:
                        if hasattr(view, 'pixmaps') and "firefighter" in view.pixmaps and view.pixmaps["firefighter"] is not None:
                            pixmap = view.pixmaps["firefighter"].scaled(cell_size - 6, cell_size - 6, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            item = view.scene.addPixmap(pixmap)
                            item.setPos(x + 3, y + 3)
                            
                            # --- HIỆU ỨNG CÕNG NẠN NHÂN ---
                            if self.carried_victim is not None:
                                mini_pixmap = view.pixmaps["victim"].scaled(cell_size//2, cell_size//2, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                                mini_item = view.scene.addPixmap(mini_pixmap)
                                # Đặt mini icon ở góc trên cùng bên phải của lính cứu hỏa
                                mini_item.setPos(x + cell_size//2, y)
                        else:
                            color = view.colors.get("firefighter", QColor("#89b4fa"))
                            view.scene.addRect(x + 2, y + 2, cell_size - 4, cell_size - 4, QPen(Qt.NoPen), QBrush(color))
                            
                            if self.carried_victim is not None:
                                view.scene.addRect(x + cell_size//2, y, cell_size//2, cell_size//2, QPen(Qt.NoPen), QBrush(view.colors["victim"]))
                            
            if self.current_csp_order:
                for idx, pos in enumerate(self.current_csp_order):
                    cr, cc = pos
                    # Chỉ hiển thị số trên đầu nạn nhân CHƯA được giải cứu thành công
                    if pos in self.sim_victims_on_map or pos == self.carried_victim:
                        text_item = view.scene.addText(f"#{idx + 1}")
                        font = text_item.font()
                        font.setPointSize(12)
                        font.setBold(True)
                        text_item.setFont(font)
                        text_item.setDefaultTextColor(QColor("#f9e2af"))
                        
                        # Nếu đang cõng, hiển thị số chạy theo lính cứu hỏa
                        if pos == self.carried_victim:
                            text_item.setPos(offset_x + c * cell_size, offset_y + r * cell_size - 10)
                        else:
                            text_item.setPos(offset_x + cc * cell_size + 8, offset_y + cr * cell_size + 8)
                        text_item.setZValue(10)

        except Exception as e:
            print(f"Lỗi vẽ UI: {str(e)}")
            
    def on_simulation_finished(self, cost, steps, time_ms):
        try:
            self.bottom_panel.btn_start.setEnabled(True)
            self.bottom_panel.btn_random.setEnabled(True)
            self.left_panel.setEnabled(True)
            
            if cost == 0 and steps == 0:
                return
                
            self.bottom_panel.lbl_cost.setText(f"Tổng chi phí: {cost}")
            self.bottom_panel.lbl_path.setText(f"Độ dài đường đi: {steps} bước")
            self.bottom_panel.lbl_time.setText(f"Thời gian: {time_ms:.2f} ms")
            
            if self.selected_algo and hasattr(self.simulation_view, 'view_comparison'):
                algo_key = None
                group_id = 0
                
                # --- PHÂN NHÓM 1 ---
                if "BFS" in self.selected_algo and "Sensorless" not in self.selected_algo: 
                    algo_key, group_id = "BFS", 1
                elif "DFS" in self.selected_algo and "Sensorless" not in self.selected_algo: 
                    algo_key, group_id = "DFS", 1
                elif "UCS" in self.selected_algo and "Partially" not in self.selected_algo: 
                    algo_key, group_id = "UCS", 1
                
                # --- PHÂN NHÓM 2 ---
                elif "A*" in self.selected_algo and "IDA*" not in self.selected_algo: 
                    algo_key, group_id = "A*", 2
                elif "Greedy" in self.selected_algo: 
                    algo_key, group_id = "Greedy", 2
                elif "IDA*" in self.selected_algo: 
                    algo_key, group_id = "IDA*", 2
                
                # --- PHÂN NHÓM 3 ---
                elif "Simple" in self.selected_algo: 
                    algo_key, group_id = "Simple HC", 3
                elif "Random" in self.selected_algo: 
                    algo_key, group_id = "Random Restart", 3
                elif "Beam" in self.selected_algo: 
                    algo_key, group_id = "Local Beam", 3
                
                # --- PHÂN NHÓM 4 ---
                elif "Sensorless BFS" in self.selected_algo: 
                    algo_key, group_id = "Sensorless BFS", 4
                elif "Sensorless DFS" in self.selected_algo: 
                    algo_key, group_id = "Sensorless DFS", 4
                elif "Partially Observable UCS" in self.selected_algo: 
                    algo_key, group_id = "Partial UCS", 4
                    
                # --- PHÂN NHÓM 5 ---
                elif "Backtracking" in self.selected_algo: 
                    algo_key, group_id = "Backtracking", 5
                elif "Forward" in self.selected_algo: 
                    algo_key, group_id = "Forward Checking", 5
                elif "AC-3" in self.selected_algo: 
                    algo_key, group_id = "AC-3", 5
                    
                # --- PHÂN NHÓM 6 ---
                elif "Minimax" in self.selected_algo: 
                    algo_key, group_id = "Minimax", 6
                elif "Alpha-Beta" in self.selected_algo: 
                    algo_key, group_id = "Alpha-Beta Pruning", 6
                elif "Expectimax" in self.selected_algo: 
                    algo_key, group_id = "Expectimax", 6
            
                    
                if algo_key and hasattr(self.simulation_view.view_comparison, 'update_data'):
                    if algo_key not in self.simulation_view.view_comparison.data:
                        self.simulation_view.view_comparison.data[algo_key] = {"time": 0, "steps": 0, "cost": 0, "group": group_id}
                    self.simulation_view.view_comparison.update_data(algo_key, int(cost), int(steps), float(time_ms))
        except Exception as e:
            self.right_panel.log(f"Lỗi cập nhật biểu đồ: {str(e)}", "red")

    def parse_map_from_ui(self, simulation_view):
        try:
            grid = simulation_view.view_standard.grid_types 
            if not grid: return None, None, None, None
                
            rows = len(grid)
            cols = len(grid[0])
            matrix = [[0 for _ in range(cols)] for _ in range(rows)]
            start_pos = (0, 0)
            victims = []
            gates = []

            for r in range(rows):
                for c in range(cols):
                    cell = grid[r][c]
                    if cell == "wall": matrix[r][c] = 1        
                    elif cell == "fire": matrix[r][c] = 2        
                    elif cell == "firefighter": start_pos = (r, c)      
                    elif cell == "victim": victims.append((r, c))  
                    elif cell == "exit": gates.append((r, c))    

            return matrix, start_pos, victims, gates
        except Exception as e:
            print(f"Lỗi đọc map: {str(e)}")
            return None, None, None, None