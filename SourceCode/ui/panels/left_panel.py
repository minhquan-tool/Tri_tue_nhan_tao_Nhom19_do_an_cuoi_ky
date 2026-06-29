from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QGroupBox

class LeftPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        group_box = QGroupBox("Danh sách Thuật toán")
        vbox = QVBoxLayout()

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        
        # Khởi tạo 6 nhóm thuật toán
        for i in range(1, 7):
            if i == 1:
                # ==========================================
                # NHÓM 1: CẤU HÌNH TÊN CHUẨN HÓA
                # ==========================================
                group_item = QTreeWidgetItem(self.tree, ["Group 1: Uninformed Search (Tìm kiếm mù)"])
                
                # Các thuật toán con
                QTreeWidgetItem(group_item, ["Breadth-First Search (BFS)"])
                QTreeWidgetItem(group_item, ["Depth-First Search (DFS)"])
                QTreeWidgetItem(group_item, ["Uniform Cost Search (UCS)"])
                
                # Nút So sánh Nhóm 1 (Gắn icon 📊 để MainWindow tự nhận diện và mở Biểu đồ)
                comp_item = QTreeWidgetItem(group_item, ["📊 So sánh Nhóm 1"])
                comp_item.setForeground(0, self.tree.palette().link().color())
            # Khởi tạo 6 nhóm thuật toán
            elif i == 2:
                # ==========================================
                # NHÓM 2: THÊM MỚI TÊN NHÓM THUẬT TOÁN
                # ==========================================
                group_item = QTreeWidgetItem(self.tree, ["Group 2: Informed Search (Tìm kiếm có thông tin)"])
                
                # Các thuật toán con của nhóm 2
                QTreeWidgetItem(group_item, ["A* Search Algorithm"])
                QTreeWidgetItem(group_item, ["Greedy Best-First Search"])
                QTreeWidgetItem(group_item, ["IDA* Search Algorithm"])
                
                # Nút So sánh Nhóm 2
                comp_item = QTreeWidgetItem(group_item, ["📊 So sánh Nhóm 2"])
                comp_item.setForeground(0, self.tree.palette().link().color())
            elif i == 3:
                # ==========================================
                # NHÓM 3: CẤU HÌNH LOCAL SEARCH
                # ==========================================
                group_item = QTreeWidgetItem(self.tree, ["Group 3: Local Search (Tìm kiếm cục bộ)"])
                QTreeWidgetItem(group_item, ["Simple Hill Climbing"])
                QTreeWidgetItem(group_item, ["Random Restart Hill Climbing"])
                QTreeWidgetItem(group_item, ["Local Beam Search"])
                
                comp_item = QTreeWidgetItem(group_item, ["📊 So sánh Nhóm 3"])
                comp_item.setForeground(0, self.tree.palette().link().color())
            elif i == 4:
                group_item = QTreeWidgetItem(self.tree, ["Group 4: Partial & Sensorless Search"])
                
                QTreeWidgetItem(group_item, ["Sensorless BFS"])
                QTreeWidgetItem(group_item, ["Sensorless DFS"])
                QTreeWidgetItem(group_item, ["Partially Observable UCS"])
                
                comp_item = QTreeWidgetItem(group_item, ["📊 So sánh Nhóm 4"])
                comp_item.setForeground(0, self.tree.palette().link().color())
            elif i == 5:
                group_item = QTreeWidgetItem(self.tree, ["Group 5: CSP"])
                
                QTreeWidgetItem(group_item, ["Backtracking Search"])
                QTreeWidgetItem(group_item, ["Forward Checking"])
                QTreeWidgetItem(group_item, ["AC-3"])
                
                comp_item = QTreeWidgetItem(group_item, ["📊 So sánh Nhóm 5"])
                comp_item.setForeground(0, self.tree.palette().link().color())
            elif i == 6:
                group_item = QTreeWidgetItem(self.tree, ["Group 6: Adversarial Search"])
                QTreeWidgetItem(group_item, ["Minimax"])
                QTreeWidgetItem(group_item, ["Alpha-Beta Pruning"])
                QTreeWidgetItem(group_item, ["Expectimax"])
                
                comp_item = QTreeWidgetItem(group_item, ["📊 So sánh Nhóm 6"])
                comp_item.setForeground(0, self.tree.palette().link().color())
        # So sánh tổng quát tất cả các nhóm ở cuối cùng
        global_comp_item = QTreeWidgetItem(self.tree, ["📈 So sánh tất cả các nhóm"])
        global_comp_item.setForeground(0, self.tree.palette().link().color())
        
        vbox.addWidget(self.tree)
        group_box.setLayout(vbox)
        layout.addWidget(group_box)

        # Mở rộng toàn bộ cây danh mục cho dễ nhìn
        self.tree.expandAll()