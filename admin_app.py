import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon
from views.admin_login import AdminLoginView
from views.admin_dashboard import AdminDashboardView
from utils.styles import LIGHT_STYLE

class AdminApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MiniBank Admin Panel")
        self.resize(900, 600)
        
        icon_path = os.path.join(os.path.dirname(__file__), 'views', 'assets', 'bank_logo.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.setStyleSheet(LIGHT_STYLE)
        self.show_admin_login()

    def show_admin_login(self):
        self.setCentralWidget(AdminLoginView(on_success=self.show_admin_dashboard))

    def show_admin_dashboard(self):
        self.setCentralWidget(AdminDashboardView(on_logout=self.show_admin_login))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminApp()
    window.show()
    sys.exit(app.exec())