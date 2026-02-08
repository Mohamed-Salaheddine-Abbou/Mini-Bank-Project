from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QTableWidget, 
                               QTableWidgetItem, QPushButton, QAbstractItemView, QHBoxLayout, QLabel, QMessageBox, QHeaderView, QComboBox, QDialog)
import sys
import os
from PySide6.QtCore import Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.admin_controller import (
    fetch_all_users, remove_user, fetch_stats,
    fetch_all_admins, fetch_global_transactions,
    fetch_user_transactions_with_counterparty # New import for fetching user transactions with counterparty
)
from views.user_transactions_dialog import UserTransactionsDialog # New import for the dialog

class AdminDashboardView(QWidget):
    def __init__(self, parent=None, on_logout=None):
        super().__init__(parent)
        self.on_logout = on_logout
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20) # Add more padding around the entire dashboard
        layout.setSpacing(15) # Increase spacing between elements
        
        header_layout = QHBoxLayout()
        title = QLabel("Admin Panel")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333;")
        header_layout.addWidget(title)
        header_layout.addStretch() # Pushes logout button to the right
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.on_logout)
        logout_btn.setFixedWidth(100) # Set a fixed width for the logout button
        header_layout.addWidget(logout_btn)
        layout.addLayout(header_layout)

    
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px; color: #555555;")
        layout.addWidget(self.stats_label)
        self.refresh_stats()

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabWidget::pane { border: 1px solid #cccccc; border-radius: 8px; }") # Style tab pane
        self.users_tab = QWidget()
        self.admins_tab = QWidget()
        self.trans_tab = QWidget()

        self.tabs.addTab(self.users_tab, "Users")
        self.tabs.addTab(self.admins_tab, "Admins")
        self.tabs.addTab(self.trans_tab, "Transactions")
        
        self.setup_users_tab()
        self.setup_admins_tab()
        self.setup_trans_tab()
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def refresh_stats(self):
        count, money = fetch_stats()
        self.stats_label.setText(f"Total Users: {count} | Total Funds: {money:.2f} DA")

    def setup_users_tab(self):
        layout = QVBoxLayout()
        
        self.users_table = QTableWidget()
        self.users_table.setFocusPolicy(Qt.NoFocus)
        self.users_table.setColumnCount(5)
        self.users_table.setHorizontalHeaderLabels(["ID", "Name", "Phone", "Account", "Balance"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.users_table.setAlternatingRowColors(True) # Enable zebra striping
        self.users_table.verticalHeader().setDefaultSectionSize(35) # Increase row height
        
        button_layout = QHBoxLayout()
        button_layout.addStretch() # Pushes buttons to the right
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_users)
        refresh_btn.setFixedWidth(120) # Set fixed width
        button_layout.addWidget(refresh_btn)
        
        view_transactions_btn = QPushButton("View Transactions") # New button
        view_transactions_btn.clicked.connect(self.view_user_transactions)
        view_transactions_btn.setFixedWidth(160)
        button_layout.addWidget(view_transactions_btn)

        delete_btn = QPushButton("Delete User")
        delete_btn.setObjectName("DangerButton") # Apply DangerButton style
        delete_btn.clicked.connect(self.delete_user)
        delete_btn.setFixedWidth(120) # Set fixed width
        button_layout.addWidget(delete_btn)

        layout.addWidget(self.users_table)
        layout.addLayout(button_layout) # Add button layout to the tab layout
        self.users_tab.setLayout(layout)
        self.load_users()

    def load_users(self):
        
        users = fetch_all_users()
        self.users_table.setRowCount(len(users))

        for i, user in enumerate(users):
            for j, val in enumerate(user):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)

                # Allow editing ONLY Name (1) and Phone (2)
                if j not in (1, 2):
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                self.users_table.setItem(i, j, item)

        self.refresh_stats()


    def view_user_transactions(self):
        row = self.users_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "View Transactions", "Please select a user to view transactions.")
            return
        
        user_id = int(self.users_table.item(row, 0).text())
        user_full_name = self.users_table.item(row, 1).text()
        
        dialog = UserTransactionsDialog(user_id, user_full_name, self)
        dialog.exec()

    def delete_user(self):
        row = self.users_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Delete User", "Please select a user to delete.")
            return
        user_id = self.users_table.item(row, 0).text()
        reply = QMessageBox.question(self, "Confirm Delete", 
                                     f"Are you sure you want to delete user ID {user_id}?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if remove_user(user_id):
                QMessageBox.information(self, "Delete User", f"User ID {user_id} deleted successfully.")
                self.load_users()
            else:
                QMessageBox.critical(self, "Delete User", f"Failed to delete user ID {user_id}.")

    def setup_admins_tab(self):
        layout = QVBoxLayout()
        self.admins_table = QTableWidget()
        self.admins_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.admins_table.setFocusPolicy(Qt.NoFocus)
        self.admins_table.setColumnCount(2)
        self.admins_table.setHorizontalHeaderLabels(["ID", "Username"])
        self.admins_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.admins_table.setAlternatingRowColors(True) # Enable zebra striping
        self.admins_table.verticalHeader().setDefaultSectionSize(35) # Increase row height
        
        layout.addWidget(self.admins_table)
        self.admins_tab.setLayout(layout)
        self.load_admins()

    def load_admins(self):
        admins = fetch_all_admins()
        self.admins_table.setRowCount(len(admins))
        for i, admin in enumerate(admins):
            for j, val in enumerate(admin):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter) # Center align text in cells
                self.admins_table.setItem(i, j, item)

    def setup_trans_tab(self):
        layout = QVBoxLayout()

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter by Type:"))
        self.type_filter_combo = QComboBox()
        self.type_filter_combo.addItems(["All", "Deposit", "Withdraw", "Transfer"])
        self.type_filter_combo.currentIndexChanged.connect(self.load_transactions)
        filter_layout.addWidget(self.type_filter_combo)
        filter_layout.addStretch() # Push filter to the left

        layout.addLayout(filter_layout)

        self.trans_table = QTableWidget()
        self.trans_table.setFocusPolicy(Qt.NoFocus)
        self.trans_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.trans_table.setColumnCount(5)
        self.trans_table.setHorizontalHeaderLabels(["ID", "User", "Type", "Amount", "Date"])
        self.trans_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.trans_table.setAlternatingRowColors(True) # Enable zebra striping
        self.trans_table.verticalHeader().setDefaultSectionSize(35) # Increase row height
        
        layout.addWidget(self.trans_table)
        self.trans_tab.setLayout(layout)
        self.load_transactions()
        
    def load_transactions(self):
        selected_type = self.type_filter_combo.currentText()
        if selected_type == "All":
            transactions = fetch_global_transactions()
        else:
            transactions = fetch_global_transactions(transaction_type=selected_type) # Assuming fetch_global_transactions can take a type filter

        self.trans_table.setRowCount(len(transactions))
        for i, transaction in enumerate(transactions):
            for j, val in enumerate(transaction):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter) # Center align text in cells
                self.trans_table.setItem(i, j, item)