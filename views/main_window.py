from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QHBoxLayout
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
import os
from views.login import LoginView
from views.create_account import CreateAccountView
from views.dashboard import DashboardView
from views.send_money import SendMoneyView
from views.admin_login import AdminLoginView
from views.admin_dashboard import AdminDashboardView

from utils.styles import LIGHT_STYLE
from utils.styles import DARK_STYLE

class MainWindow(QMainWindow):
    def __init__(self, enable_admin=True):
        super().__init__()
        self.setWindowTitle("MiniBank - PySide6")
        self.resize(900, 600)
        self.enable_admin = enable_admin
        
        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'bank_logo.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.setStyleSheet(DARK_STYLE)
        self.show_menu()

    def show_menu(self):
        widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(40, 40, 40, 40)
        left_layout.addStretch()

        container = QWidget()
        container.setFixedWidth(350)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(15)

        title = QLabel("MiniBank System")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        btn_login = QPushButton("Login")
        btn_login.clicked.connect(self.show_login)
        btn_login.setMinimumHeight(40)
        
        btn_create = QPushButton("Create Account")
        btn_create.clicked.connect(self.show_create_account)
        btn_create.setMinimumHeight(40)
        
        layout.addWidget(btn_login)
        layout.addWidget(btn_create)

        if self.enable_admin:
            btn_admin = QPushButton("Admin Panel")
            btn_admin.clicked.connect(self.show_admin_login)
            btn_admin.setMinimumHeight(40)
            layout.addWidget(btn_admin)
        
        left_layout.addWidget(container, 0, Qt.AlignCenter)
        left_layout.addStretch()
        
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setAlignment(Qt.AlignCenter)

        logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.svg')
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            pixmap = pixmap.scaled(450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            right_layout.addWidget(logo_label)

        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(right_widget, 1)
        
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def show_login(self):
        self.setCentralWidget(LoginView(on_login_success=self.show_dashboard, on_back=self.show_menu))

    def show_create_account(self):
        self.setCentralWidget(CreateAccountView(on_back=self.show_menu))

    def show_dashboard(self, user_id):
        self.setCentralWidget(DashboardView(
            user_id=user_id, 
            on_logout=self.show_menu,
            on_send_money=self.show_send_money
        ))

    def show_send_money(self, user_id):
        self.setCentralWidget(SendMoneyView(
            user_id=user_id, 
            on_back=lambda: self.show_dashboard(user_id)
        ))

    def show_admin_login(self):
        self.setCentralWidget(AdminLoginView(on_success=self.show_admin_dashboard, on_back=self.show_menu))

    def show_admin_dashboard(self):
        self.setCentralWidget(AdminDashboardView(on_logout=self.show_menu))
