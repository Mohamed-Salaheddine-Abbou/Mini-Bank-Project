from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize
import sys
import os

# Ensure we can import from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.auth_controller import login

class LoginView(QWidget):
    def __init__(self, parent=None, on_login_success=None, on_back=None):
        super().__init__(parent)
        self.on_login_success = on_login_success
        self.on_back = on_back
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- Left Side (Form) ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(40, 40, 40, 40)

        if self.on_back:
            top_bar = QHBoxLayout()
            arrow_path = os.path.join(os.path.dirname(__file__), 'assets', 'arrow.svg')
            back_btn = QPushButton()
            back_btn.setIcon(QIcon(arrow_path))
            back_btn.setIconSize(QSize(24, 24))
            back_btn.setCursor(Qt.PointingHandCursor)
            back_btn.setStyleSheet("background-color: transparent; border: none;")
            back_btn.setFixedWidth(50)
            back_btn.clicked.connect(self.on_back)
            top_bar.addWidget(back_btn)
            top_bar.addStretch()
            left_layout.addLayout(top_bar)
        
        left_layout.addStretch()

        container = QWidget()
        container.setFixedWidth(350)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Login")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignLeft)
        layout.addWidget(title)
        
        layout.addWidget(QLabel("Account Number"))
        self.account_entry = QLineEdit()
        self.account_entry.setPlaceholderText("Enter Account Number")
        layout.addWidget(self.account_entry)

        layout.addWidget(QLabel("Password"))
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setPlaceholderText("Enter Password")
        layout.addWidget(self.password_entry)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)
        self.login_btn.setMinimumHeight(40)
        layout.addWidget(self.login_btn)
        
        left_layout.addWidget(container, 0, Qt.AlignCenter)
        left_layout.addStretch()

        # --- Right Side (Logo) ---
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
        self.setLayout(main_layout)

    def handle_login(self):
        account_num = self.account_entry.text().strip()
        password = self.password_entry.text().strip()

        user, error = login(account_num, password)

        if error:
            QMessageBox.critical(self, "Login Failed", error)
        else:
            if self.on_login_success:
                self.on_login_success(user['id'])