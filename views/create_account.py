from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QComboBox, QFileDialog
from PySide6.QtGui import QPixmap, QIcon, QGuiApplication
import sys
import os
from PySide6.QtCore import Qt, QSize

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.account_controller import open_account
from utils.validators import is_valid_algerian_phone

class CreateAccountView(QWidget):
    def __init__(self, parent=None, on_back=None):
        super().__init__(parent)
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
            if os.path.exists(arrow_path):
                back_btn.setIcon(QIcon(arrow_path))
                back_btn.setIconSize(QSize(24, 24))
                back_btn.setStyleSheet("background-color: transparent; border: none;")
                back_btn.setFixedWidth(50)
            else:
                back_btn.setText("Back")
            back_btn.setCursor(Qt.PointingHandCursor)
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

        title = QLabel("Create New Account")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignLeft)
        layout.addWidget(title)

        layout.addWidget(QLabel("Full Name"))
        self.name_entry = QLineEdit()
        layout.addWidget(self.name_entry)
        
        layout.addWidget(QLabel("Phone (Algerian)"))
        phone_layout = QHBoxLayout()
        self.phone_prefix = QComboBox()
        self.phone_prefix.addItems(["05", "06", "07"])
        self.phone_suffix = QLineEdit()
        phone_layout.addWidget(self.phone_prefix)
        phone_layout.addWidget(self.phone_suffix)
        layout.addLayout(phone_layout)

        self.create_btn = QPushButton("Create Account")
        self.create_btn.clicked.connect(self.create_account)
        self.create_btn.setMinimumHeight(40)
        layout.addWidget(self.create_btn)

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

    def create_account(self):
   
        full_name = self.name_entry.text().strip()
        phone = self.phone_prefix.currentText() + self.phone_suffix.text().strip()

        if not full_name or not phone:
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return

        data, error = open_account(full_name, phone)
        if error:
            QMessageBox.critical(self, "Error", error)
            return

        msg = (
            "Your account has been created!\n\n"
            f"Account Number: {data['account_number']}\n"
            f"Password: {data['password']}\n\n"
            "Please save these details now."
        )

        while True:  # Keep showing until OK is clicked
            box = QMessageBox(self)
            box.setWindowTitle("Success")
            box.setText("Account created successfully")
            box.setInformativeText(msg)
            box.setIcon(QMessageBox.Information)

            ok_btn = box.addButton("OK", QMessageBox.AcceptRole)
            copy_btn = box.addButton("Copy", QMessageBox.ActionRole)
            download_btn = box.addButton("Download", QMessageBox.ActionRole)

            box.exec()
            
            clicked = box.clickedButton()
            
            if clicked == copy_btn:
                QGuiApplication.clipboard().setText(msg)
                # Loop continues, dialog will reappear
                
            elif clicked == download_btn:
                file_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Save Account Details",
                    "account_details.txt",
                    "Text Files (*.txt)"
                )
                if file_path:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(msg)
                # Loop continues, dialog will reappear
                
            else:  # OK button clicked
                break  # Exit the loop

        self.name_entry.clear()
        self.phone_suffix.clear()

        if self.on_back:
            self.on_back()

