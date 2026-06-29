from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGroupBox, QStackedWidget, QLabel, QHBoxLayout, QProgressBar
from PyQt5.QtGui import QBrush, QPen, QColor, QPixmap, QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis

import random
import os

# =====================================================================
# 1. BASE GRID VIEW
# =====================================================================
class BaseGridView(QWidget):
    def __init__(self, title):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.group_box = QGroupBox(title)
        vbox = QVBoxLayout()

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(1) 
        
        vbox.addWidget(self.view)
        self.group_box.setLayout(vbox)
        layout.addWidget(self.group_box)

        self.grid_types = []
        self.cell_size = 40
        
        self.colors = {
            "empty": QColor("#1e1e2e"), "wall": QColor("#45475a"),
            "fire": QColor("#fab387"), "firefighter": QColor("#89b4fa"),
            "victim": QColor("#a6e3a1"), "exit": QColor("#f38ba8"),
            "fog": QColor("#11111b")
        }

        self.pixmaps = {}
        assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")
        asset_files = {"wall": "wall.png", "fire": "fire.png", "firefighter": "firefighter.png", "victim": "victim.png", "exit": "exit.png"}

        for key, filename in asset_files.items():
            full_path = os.path.join(assets_path, filename)
            if os.path.exists(full_path):
                self.pixmaps[key] = QPixmap(full_path)
            else:
                self.pixmaps[key] = None 

    def generate_map_data(self, rows, cols, num_victims, num_fires):
        """Chỉ tạo dữ liệu ma trận, không vẽ"""
        self.grid_types = [["empty" for _ in range(cols)] for _ in range(rows)]
        max_dim = max(rows, cols)
        self.cell_size = max(35, min(100, 500 // max_dim)) 

        edge_coords = [(r, c) for r in range(rows) for c in range(cols) if r==0 or r==rows-1 or c==0 or c==cols-1]
        num_exits = min(3, len(edge_coords))
        for r, c in random.sample(edge_coords, num_exits): 
            self.grid_types[r][c] = "exit"
            
        empty_coords = [(r, c) for r in range(rows) for c in range(cols) if self.grid_types[r][c] == "empty"]
        if not empty_coords: return

        ff = random.choice(empty_coords)
        self.grid_types[ff[0]][ff[1]] = "firefighter"
        empty_coords.remove(ff)

        for t, count in [("victim", num_victims), ("fire", num_fires)]:
            for _ in range(min(count, len(empty_coords))):
                pos = random.choice(empty_coords)
                self.grid_types[pos[0]][pos[1]] = t
                empty_coords.remove(pos)

        num_walls = min(len(empty_coords), int(len(empty_coords) * 0.2))
        for _ in range(num_walls):
            pos = random.choice(empty_coords)
            self.grid_types[pos[0]][pos[1]] = "wall"
            empty_coords.remove(pos)

    def draw_cell_item(self, r, c, cell_type):
        self.scene.addRect(c*self.cell_size, r*self.cell_size, self.cell_size, self.cell_size, QPen(QColor("#313244")), QBrush(self.colors["empty"]))
        if cell_type != "empty":
            pixmap = self.pixmaps.get(cell_type)
            if pixmap and not pixmap.isNull():
                pixmap_item = self.scene.addPixmap(pixmap.scaled(self.cell_size - 6, self.cell_size - 6, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                pixmap_item.setPos(c*self.cell_size + 3, r*self.cell_size + 3)
            else:
                self.scene.addRect(c*self.cell_size + 2, r*self.cell_size + 2, self.cell_size - 4, self.cell_size - 4, QPen(Qt.NoPen), QBrush(self.colors[cell_type]))

# =====================================================================
# 2. STANDARD GRID VIEW
# =====================================================================
class StandardGridView(BaseGridView):
    def redraw_map(self):
        self.scene.clear()
        rows = len(self.grid_types)
        cols = len(self.grid_types[0]) if rows > 0 else 0
        for r in range(rows):
            for c in range(cols):
                self.draw_cell_item(r, c, self.grid_types[r][c])
        self.scene.setSceneRect(0, 0, cols*self.cell_size, rows*self.cell_size)

# =====================================================================
# 3. SENSORLESS GRID VIEW
# =====================================================================
class SensorlessGridView(BaseGridView):
    def redraw_map(self):
        self.scene.clear()
        rows = len(self.grid_types)
        cols = len(self.grid_types[0]) if rows > 0 else 0
        for r in range(rows):
            for c in range(cols):
                if self.grid_types[r][c] == "firefighter":
                    self.draw_cell_item(r, c, "firefighter")
                else:
                    self.scene.addRect(c*self.cell_size, r*self.cell_size, self.cell_size, self.cell_size, QPen(QColor("#181825")), QBrush(self.colors["fog"]))
        self.scene.setSceneRect(0, 0, cols*self.cell_size, rows*self.cell_size)

# =====================================================================
# 4. CSP GRID VIEW
# =====================================================================
class CSPGridView(BaseGridView):
    def redraw_map(self):
        self.scene.clear()
        rows = len(self.grid_types)
        cols = len(self.grid_types[0]) if rows > 0 else 0
        for r in range(rows):
            for c in range(cols):
                t = self.grid_types[r][c]
                self.scene.addRect(c*self.cell_size, r*self.cell_size, self.cell_size, self.cell_size, QPen(QColor("#313244")), QBrush(QColor("#11111b")))
                
                pen = QPen(self.colors.get(t, QColor("#1e1e2e")), 2)
                brush = QBrush(QColor(self.colors.get(t, QColor("#1e1e2e")).name() + "15"))
                
                offset = int(self.cell_size * 0.1)
                diameter = int(self.cell_size * 0.8)
                self.scene.addEllipse(c*self.cell_size + offset, r*self.cell_size + offset, diameter, diameter, pen, brush)
                
                if t != "empty":
                    pixmap = self.pixmaps.get(t)
                    if pixmap and not pixmap.isNull():
                        inner_size = int(self.cell_size * 0.45)
                        pixmap_item = self.scene.addPixmap(pixmap.scaled(inner_size, inner_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        center_pos = (self.cell_size - inner_size) // 2
                        pixmap_item.setPos(c*self.cell_size + center_pos, r*self.cell_size + center_pos)
                        
        self.scene.setSceneRect(0, 0, cols*self.cell_size, rows*self.cell_size)

# =====================================================================
# 5. COMPARISON VIEW (Giữ nguyên)
# =====================================================================
class AlgorithmComparisonView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.chart = QChart()
        self.chart.setTitle("📊 SO SÁNH HIỆU SUẤT THUẬT TOÁN")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setBackgroundBrush(QColor("#1e1e2e"))
        self.chart.setTitleBrush(QColor("#cdd6f4"))
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setStyleSheet("background-color: #1e1e2e; border: none;")
        self.layout.addWidget(self.chart_view)
        self.data = {
            "BFS": {"time": 0, "steps": 0, "cost": 0, "group": 1},
            "DFS": {"time": 0, "steps": 0, "cost": 0, "group": 1},
            "UCS": {"time": 0, "steps": 0, "cost": 0, "group": 1},
            "Simple HC": {"time": 0, "steps": 0, "cost": 0, "group": 3},
            "Random Restart": {"time": 0, "steps": 0, "cost": 0, "group": 3},
            "Local Beam": {"time": 0, "steps": 0, "cost": 0, "group": 3}
        }
        self.current_group = 1 
        self.draw_chart()

    def set_current_group(self, group_id):
        self.current_group = group_id
        if group_id == 1: self.chart.setTitle("📊 SO SÁNH TÌM KIẾM MÙ (NHÓM 1)")
        elif group_id == 3: self.chart.setTitle("⛰️ SO SÁNH LOCAL SEARCH (NHÓM 3)")
        else: self.chart.setTitle("📈 SO SÁNH TẤT CẢ THUẬT TOÁN")
        self.draw_chart()

    def update_data(self, algo_name, cost, steps, time_ms):
        if algo_name in self.data:
            self.data[algo_name]["time"] = time_ms
            self.data[algo_name]["steps"] = steps
            self.data[algo_name]["cost"] = cost
            self.draw_chart()

    def draw_chart(self):
        self.chart.removeAllSeries()
        for axis in self.chart.axes(): self.chart.removeAxis(axis)
        series = QBarSeries()
        colors = [QColor("#89b4fa"), QColor("#f38ba8"), QColor("#a6e3a1"), QColor("#f9e2af"), QColor("#cba6f7"), QColor("#94e2d5")]
        color_idx = 0
        for algo_name, stats in self.data.items():
            if self.current_group == 0 or stats["group"] == self.current_group:
                bar_set = QBarSet(algo_name)
                bar_set.setColor(colors[color_idx % len(colors)])
                bar_set.append([stats["time"], stats["steps"], stats["cost"]])
                series.append(bar_set)
                color_idx += 1
        self.chart.addSeries(series)
        axisX = QBarCategoryAxis()
        axisX.append(["Thời gian (ms)", "Số bước đi", "Chi phí"])
        axisX.setLabelsColor(QColor("#cdd6f4"))
        self.chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        axisY = QValueAxis()
        axisY.setLabelsColor(QColor("#cdd6f4"))
        self.chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart.legend().setLabelColor(QColor("#cdd6f4"))

# =====================================================================
# MAIN SIMULATION VIEW MANAGEMENT
# =====================================================================
class SimulationView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.view_standard = StandardGridView("Mô phỏng trực quan (Ma trận Chuẩn)")
        self.view_sensorless = SensorlessGridView("Mô phỏng trực quan (Giao diện Mù - Sensorless)")
        self.view_csp = CSPGridView("Mô phỏng trực quan (Mạng ràng buộc CSP)")
        self.view_comparison = AlgorithmComparisonView()

        self.stacked_widget.addWidget(self.view_standard)   
        self.stacked_widget.addWidget(self.view_sensorless) 
        self.stacked_widget.addWidget(self.view_csp)        
        self.stacked_widget.addWidget(self.view_comparison)  

    def generate_random_map_with_params(self, rows, cols, victims, fires):
        """Khởi tạo 1 map duy nhất và đồng bộ cho tất cả các View"""
        self.view_standard.generate_map_data(rows, cols, victims, fires)
        shared_grid = self.view_standard.grid_types
        shared_cell_size = self.view_standard.cell_size
        
        # Clone dữ liệu sang các view khác để đảm bảo tính công bằng 100%
        self.view_sensorless.grid_types = shared_grid
        self.view_sensorless.cell_size = shared_cell_size
        
        self.view_csp.grid_types = shared_grid
        self.view_csp.cell_size = shared_cell_size
        
        self.redraw_current_view()

    def redraw_current_view(self):
        """Chỉ vẽ lại map cũ, tuyệt đối không tạo map mới"""
        idx = self.stacked_widget.currentIndex()
        if idx == 0: self.view_standard.redraw_map()
        elif idx == 1: self.view_sensorless.redraw_map()
        elif idx == 2: self.view_csp.redraw_map()

    def change_view(self, view_type):
        if view_type == "standard": self.stacked_widget.setCurrentIndex(0)
        elif view_type == "sensorless": self.stacked_widget.setCurrentIndex(1)
        elif view_type == "csp": self.stacked_widget.setCurrentIndex(2)
        elif view_type == "comparison": self.stacked_widget.setCurrentIndex(3)
        
        # Khi chuyển tab, map được vẽ lại nguyên vẹn như lúc chưa chạy thuật toán
        self.redraw_current_view()
        
    def display_csp_order(self, rescue_order):
        view = self.view_standard 
        if not rescue_order: return

        for idx, pos in enumerate(rescue_order):
            r, c = pos
            text_item = view.scene.addText(f"#{idx + 1}")
            font = text_item.font()
            font.setPointSize(12)
            font.setBold(True)
            text_item.setFont(font)
            text_item.setDefaultTextColor(QColor("#f9e2af")) 
            
            cell_size = getattr(view, 'cell_size', 40)
            text_item.setPos(c * cell_size + 8, r * cell_size + 8)
            text_item.setZValue(10)