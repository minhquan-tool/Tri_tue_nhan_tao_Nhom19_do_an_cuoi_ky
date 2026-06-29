from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QGroupBox, QGridLayout, QSpinBox

class BottomPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 1. Cụm cấu hình thông số Map & Vật thể
        config_group = QGroupBox("Cấu hình Bản đồ")
        config_layout = QGridLayout()
        
        config_layout.addWidget(QLabel("Số hàng (N):"), 0, 0)
        self.spin_rows = QSpinBox()
        self.spin_rows.setRange(3, 30)
        self.spin_rows.setValue(5) # Mặc định là 5
        config_layout.addWidget(self.spin_rows, 0, 1)

        config_layout.addWidget(QLabel("Số cột (M):"), 0, 2)
        self.spin_cols = QSpinBox()
        self.spin_cols.setRange(3, 30)
        self.spin_cols.setValue(5) # Mặc định là 5
        config_layout.addWidget(self.spin_cols, 0, 3)

        config_layout.addWidget(QLabel("Số nạn nhân:"), 1, 0)
        self.spin_victims = QSpinBox()
        self.spin_victims.setRange(1, 10)
        self.spin_victims.setValue(1)
        config_layout.addWidget(self.spin_victims, 1, 1)

        config_layout.addWidget(QLabel("Số vùng cháy:"), 1, 2)
        self.spin_fire = QSpinBox()
        self.spin_fire.setRange(0, 15)
        self.spin_fire.setValue(2)
        config_layout.addWidget(self.spin_fire, 1, 3)

        config_group.setLayout(config_layout)

        # 2. Cụm nút hành động
        action_group = QGroupBox("Thao tác")
        action_layout = QVBoxLayout()
        
        self.btn_random = QPushButton("Random Map")
        
        h_btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("Bắt đầu")
        self.btn_stop = QPushButton("Dừng")
        self.btn_stop.setStyleSheet("background-color: #f38ba8; color: #11111b;")
        h_btn_layout.addWidget(self.btn_start)
        h_btn_layout.addWidget(self.btn_stop)
        
        action_layout.addWidget(self.btn_random)
        action_layout.addLayout(h_btn_layout)
        action_group.setLayout(action_layout)

        # 3. Cụm thông số kết quả (Results)
        stats_group = QGroupBox("Kết quả & Thông số")
        stats_layout = QGridLayout()
        
        self.lbl_cost = QLabel("Tổng chi phí: 0")
        self.lbl_time = QLabel("Thời gian thực thi: 0 ms")
        self.lbl_victims_progress = QLabel("Nạn nhân đã cứu: 0/1")
        self.lbl_path = QLabel("Độ dài đường đi: 0 bước")

        label_style = "font-size: 15px; color: #a6e3a1; font-weight: bold;"
        self.lbl_cost.setStyleSheet(label_style)
        self.lbl_time.setStyleSheet(label_style)
        self.lbl_victims_progress.setStyleSheet("font-size: 15px; color: #f9e2af; font-weight: bold;")

        stats_layout.addWidget(self.lbl_cost, 0, 0)
        stats_layout.addWidget(self.lbl_time, 0, 1)
        stats_layout.addWidget(self.lbl_victims_progress, 1, 0)
        stats_layout.addWidget(self.lbl_path, 1, 1)
        stats_group.setLayout(stats_layout)

        # Gom tất cả vào Layout chính của BottomPanel
        layout.addWidget(config_group, stretch=2)
        layout.addWidget(action_group, stretch=1)
        layout.addWidget(stats_group, stretch=2)