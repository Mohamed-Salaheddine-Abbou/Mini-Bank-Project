from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout
import sys
import os
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.transaction_controller import send_money

class SendMoneyView(QWidget):
    def __init__(self, parent=None, user_id=None, on_back=None):
        super().__init__(parent)
        self.user_id = user_id
        self.on_back = on_back
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Top bar with back arrow
        if self.on_back:
            top_bar = QHBoxLayout()
            arrow_path = os.path.join(os.path.dirname(__file__), 'assets', 'arrow.svg')
            back_btn = QPushButton()
            if os.path.exists(arrow_path):
                back_btn.setIcon(QIcon(arrow_path))
                back_btn.setIconSize(QSize(24, 24))
                back_btn.setStyleSheet("background-color: transparent; border: none;")
                back_btn.setFixedWidth(50)
            back_btn.setCursor(Qt.PointingHandCursor)
            back_btn.clicked.connect(self.on_back)
            top_bar.addWidget(back_btn)
            top_bar.addStretch()
            main_layout.addLayout(top_bar)

        main_layout.addStretch()

        container = QWidget()
        container.setFixedWidth(300)

        layout = QVBoxLayout(container)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Send Money")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addWidget(QLabel("Receiver Account Number"))
        self.receiver_entry = QLineEdit()
        layout.addWidget(self.receiver_entry)
        
        layout.addWidget(QLabel("Amount (DA)"))
        self.amount_entry = QLineEdit()
        layout.addWidget(self.amount_entry)

        send_btn = QPushButton("Send Money")
        send_btn.clicked.connect(self.handle_send)
        layout.addWidget(send_btn)

        main_layout.addWidget(container, 0, Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def handle_send(self):
        receiver = self.receiver_entry.text().strip()
        amount_str = self.amount_entry.text().strip()

        try:
            amount = float(amount_str)
            success, msg = send_money(self.user_id, receiver, amount)
            if success:
                QMessageBox.information(self, "Success", msg)
                self.on_back()
            else:
                QMessageBox.critical(self, "Error", msg)
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid amount")