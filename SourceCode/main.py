import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow 

def main():
    app = QApplication(sys.argv)
    
    # Thiết lập giao diện hiện đại phong cách Dark Theme (QSS)
    app.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #1e1e2e;
            color: #cdd6f4;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
        }
        QGroupBox {
            border: 1px solid #45475a;
            border-radius: 8px;
            margin-top: 15px;
            font-weight: bold;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
            color: #89b4fa;
        }
        QPushButton {
            background-color: #89b4fa;
            color: #11111b;
            border-radius: 6px;
            padding: 8px 15px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #b4befe;
        }
        QTreeWidget, QTextEdit {
            background-color: #11111b;
            border: 1px solid #313244;
            border-radius: 5px;
            padding: 5px;
        }
        QHeaderView::section {
            background-color: #313244;
            color: white;
            border: none;
            padding: 4px;
        }
        QSplitter::handle {
            background-color: #313244;
        }
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()