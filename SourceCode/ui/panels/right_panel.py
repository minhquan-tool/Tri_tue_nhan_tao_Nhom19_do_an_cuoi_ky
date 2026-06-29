from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QGroupBox
from PyQt5.QtGui import QColor

class RightPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        group_box = QGroupBox("Nhật ký hệ thống (Logs)")
        vbox = QVBoxLayout()

        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        
        vbox.addWidget(self.log_console)
        group_box.setLayout(vbox)
        layout.addWidget(group_box)

        self.log("Hệ thống đã khởi tạo thành công.", "cyan")
        self.log("Đang chờ chọn thuật toán...", "white")

    def log(self, message, color_name="white"):
        color_map = {
            "white": "#cdd6f4",
            "green": "#a6e3a1",
            "red": "#f38ba8",
            "yellow": "#f9e2af",
            "cyan": "#89dceb"
        }
        color = color_map.get(color_name, "#cdd6f4")
        self.log_console.append(f'<span style="color:{color};">{message}</span>')