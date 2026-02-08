from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, 
                               QMessageBox, QInputDialog, QDialog, QTextEdit, QToolButton, QHBoxLayout, QSizePolicy)
from PySide6.QtGui import QIcon, QPixmap, QTransform, QGuiApplication
from PySide6.QtCore import Qt, QTimer, QSize, QDir
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.transaction_controller import deposit, withdraw, get_account_history
from controllers.notification_controller import get_my_notifications, read_notifications
from models.user_model import get_user_by_id
from models.transaction_model import get_balance

class DashboardView(QWidget):
    def __init__(self, parent=None, user_id=None, on_logout=None, on_send_money=None):
        super().__init__(parent)
        
        self.user_id = user_id
        self.on_logout = on_logout
        self.on_send_money = on_send_money

        user_data = get_user_by_id(self.user_id)

        self.full_name = user_data[1] if user_data else "User"
        self.account_number = user_data[2] if user_data else "N/A"

        self.balance_visible = True
        self.info_visible = False

        self.init_ui()

        self.update_balance()
        self.is_blinking_on = False

        self.blink_timer = QTimer(self)

        self.blink_timer.timeout.connect(self.blink_notification)
        self.check_notifications()

        self.real_time_timer = QTimer(self)
        self.real_time_timer.timeout.connect(self.check_notifications)
        self.real_time_timer.start(5000) # Check for new notifications every 5 seconds

    def init_ui(self):
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        self.welcome_label = QLabel(f"Welcome, {self.full_name[:5]}")

        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.welcome_label)

        # User Info (hidden by default)
        self.info_layout = QHBoxLayout()
        self.info_layout.setAlignment(Qt.AlignCenter)
        self.info_layout.setSpacing(15)

        self.full_name_label = self.create_clickable_label(self.full_name)
        self.account_number_label = self.create_clickable_label(self.account_number)

        self.info_layout.addWidget(self.full_name_label)
        self.info_layout.addWidget(self.account_number_label)

        self.info_widget = QWidget()
        self.info_widget.setLayout(self.info_layout)
        self.info_widget.setVisible(False)
        self.info_widget.setStyleSheet("font-size: 14px; color: #a0a0a0; font-family: 'Consolas', 'Monaco', monospace;")

        layout.addWidget(self.info_widget)

        self.toggle_info_btn = QPushButton("Show Details")
        self.toggle_info_btn.clicked.connect(self.toggle_info_visibility)
        self.toggle_info_btn.setStyleSheet("max-width: 120px; margin: 0 auto; padding: 4px 8px;")
        layout.addWidget(self.toggle_info_btn, 0, Qt.AlignCenter)

        # Balance Section
        balance_layout = QHBoxLayout()
        balance_layout.setAlignment(Qt.AlignCenter)
        balance_layout.setSpacing(10)

        self.balance_label = QLabel()
        self.balance_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50;")

        self.toggle_balance_btn = QPushButton()
        self.toggle_balance_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_balance_btn.setFixedSize(40, 40)
        self.toggle_balance_btn.clicked.connect(self.toggle_balance_visibility)
        self.show_icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icons', 'show.svg')
        self.hide_icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icons', 'hide.svg')
        self.toggle_balance_btn.setToolTip("Show/Hide Balance")
        self.toggle_balance_btn.setStyleSheet("background-color: transparent; border: none; font-size: 20px;")

        self.update_balance_icon()

        balance_layout.addWidget(self.balance_label)
        balance_layout.addWidget(self.toggle_balance_btn)

        layout.addLayout(balance_layout)

        # Grid for Actions
        grid = QGridLayout()
        grid.setSpacing(20)
        
        
        # Initialize notification icon paths and QIcon objects
        self.notif_on_icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icons', 'notification on.svg')
        self.notif_off_icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icons', 'notification off.svg')
        
        if os.path.exists(self.notif_off_icon_path):
            self.notif_off_icon = QIcon(self.notif_off_icon_path)
        if os.path.exists(self.notif_on_icon_path):
            self.notif_on_icon = QIcon(self.notif_on_icon_path)

        def create_action_btn(text, icon_file, callback):
            btn = QToolButton()
            btn.setText(text)
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icons', icon_file)
            if os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
                btn.setIconSize(QSize(48, 48))
            btn.clicked.connect(callback)
            btn.setCursor(Qt.PointingHandCursor)
            
            if text == "Notifications":
                # Ensure the initial icon is set correctly if not handled by init_ui
                if self.notif_off_icon:
                    btn.setIcon(self.notif_off_icon)


            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("""
                QToolButton {
                    background-color: #2d2d2d;
                    border: 1px solid #3e3e3e;
                    border-radius: 12px;
                    color: #e0e0e0;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 15px;
                }
                QToolButton:hover {
                    background-color: #3d3d3d;
                    border-color: #555555;
                }
                QToolButton:pressed {
                    background-color: #222222;
                }
            """)
            return btn
        
        btn_deposit = create_action_btn("Deposit", "deposit.svg", self.handle_deposit)
        btn_withdraw = create_action_btn("Withdraw", "withdraw.png", self.handle_withdraw)
        btn_transfer = create_action_btn("Transfer Money", "transfer.svg", lambda: self.on_send_money(self.user_id))
        btn_history = create_action_btn("Transactions", "transaction.png", self.show_transactions)
        
        self.btn_notif = create_action_btn("Notifications", "notification off.svg", self.show_notifications)

        grid.addWidget(btn_deposit, 0, 0)
        grid.addWidget(btn_withdraw, 0, 1)
        grid.addWidget(btn_transfer, 0, 2)
        grid.addWidget(btn_history, 1, 0)
        grid.addWidget(self.btn_notif, 1, 1)

        layout.addLayout(grid)
        layout.addStretch()
        
        # Logout Button (Bottom Right)
        logout_layout = QHBoxLayout()
        logout_layout.addStretch()
        
        btn_logout = QPushButton()
        logout_icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icons', 'logout.svg')
        if os.path.exists(logout_icon_path):
            pixmap = QPixmap(logout_icon_path)
            flipped_pixmap = pixmap.transformed(QTransform().scale(-1, 1))
            btn_logout.setIcon(QIcon(flipped_pixmap))
            btn_logout.setIconSize(QSize(32, 32))
        btn_logout.setToolTip("Logout")
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #333333;
                border-radius: 20px;
            }
        """)
        btn_logout.setFixedSize(40, 40)
        btn_logout.clicked.connect(self.on_logout)
        
        logout_layout.addWidget(btn_logout)
        layout.addLayout(logout_layout)
        
        self.setLayout(layout)

    def update_balance(self):
        if self.balance_visible:
            balance = get_balance(self.user_id)
            self.balance_label.setText(f"Balance: {balance:.2f} DA" if balance is not None else "N/A")
        else:
            self.balance_label.setText("Balance: ******** DA")

    def update_balance_icon(self):
         if self.balance_visible:
            self.toggle_balance_btn.setIcon(QIcon(self.show_icon_path))
         else:
            self.toggle_balance_btn.setIcon(QIcon(self.hide_icon_path))

    def toggle_balance_visibility(self):
        self.balance_visible = not self.balance_visible

        self.update_balance()
        self.update_balance_icon()




    def toggle_info_visibility(self):
        self.info_visible = not self.info_visible
        self.info_widget.setVisible(self.info_visible)
        self.toggle_info_btn.setText("Hide Details" if self.info_visible else "Show Details")

    def create_clickable_label(self, text):
        label = QPushButton(text)
        label.setCursor(Qt.PointingHandCursor)
        label.setStyleSheet("background-color: transparent; border: none; text-decoration: underline;")
        label.clicked.connect(lambda: self.copy_to_clipboard(label))
        return label

    def copy_to_clipboard(self, label_button):
        text_to_copy = label_button.text()
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(text_to_copy)
        
        # Show a temporary "Copied!" message
        original_text = label_button.text()
        label_button.setText("Copied!")
        QTimer.singleShot(1000, lambda: label_button.setText(original_text))

    def handle_deposit(self):
        amount, ok = QInputDialog.getDouble(self, "Deposit", "Amount:", 0, 0, 1000000, 2)
        if ok and amount > 0:
            success, msg = deposit(self.user_id, amount)
            if success:
                QMessageBox.information(self, "Success", msg)
                self.update_balance()
            else:
                QMessageBox.warning(self, "Error", msg)

    def handle_withdraw(self):
        amount, ok = QInputDialog.getDouble(self, "Withdraw", "Amount:", 0, 0, 1000000, 2)
        if ok and amount > 0:
            success, msg = withdraw(self.user_id, amount)
            if success:
                QMessageBox.information(self, "Success", msg)
                self.update_balance()
            else:
                QMessageBox.warning(self, "Error", msg)

    def show_transactions(self):
        txs = get_account_history(self.user_id)
        text = "\n".join([f"{t[2]}: {t[0]} {t[1]:.2f} DA" for t in txs]) if txs else "No transactions."
        self.show_info_dialog("Transaction History", text)

    def check_notifications(self):
        notifs = get_my_notifications(self.user_id)
        self.notif_count = len(notifs)

        if self.notif_count > 0:
            self.btn_notif.setText(f"Notifications ({self.notif_count})")
            # Start blinking if not already
            if not self.blink_timer.isActive():
                self.start_blinking()
        else:
            # Stop blinking if there are no notifications
            if self.blink_timer.isActive():
                self.stop_blinking()
            self.btn_notif.setText("Notifications")

    def start_blinking(self):
        if not self.notif_on_icon or not self.notif_off_icon:
            return
        # Ensure we start from a known state and show the 'on' icon immediately
        self.is_blinking_on = False
        self.blink_notification() # This will set icon to 'on' and is_blinking_on to True
        self.blink_timer.start(500)

    def stop_blinking(self):
        self.blink_timer.stop()
        self.is_blinking_on = False
        if self.notif_off_icon:
            self.btn_notif.setIcon(self.notif_off_icon)

    def blink_notification(self):
        if not self.notif_on_icon or not self.notif_off_icon:
            return

        if self.is_blinking_on:
            self.btn_notif.setIcon(self.notif_off_icon)
        else:
            self.btn_notif.setIcon(self.notif_on_icon)
        self.is_blinking_on = not self.is_blinking_on

    def show_notifications(self):
        self.stop_blinking() # Stop blinking and reset to 'off' state
        notifs = get_my_notifications(self.user_id)
        text = "\n".join([n[0] for n in notifs]) if notifs else "No new notifications."
        self.show_info_dialog("Notifications", text)
        read_notifications(self.user_id)
        self.check_notifications() # Re-check to update count (which should be 0)

    def show_info_dialog(self, title, content):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.resize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.setPlainText(content)
        text_area.setStyleSheet("font-size: 14px; padding: 10px;")
        layout.addWidget(text_area)
        
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)
        
        dialog.exec()
