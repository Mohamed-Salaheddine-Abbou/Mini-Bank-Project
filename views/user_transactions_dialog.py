from PySide6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                               QLabel, QHeaderView)
from PySide6.QtCore import Qt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.admin_controller import fetch_user_transactions_with_counterparty

class UserTransactionsDialog(QDialog):
    def __init__(self, user_id, user_full_name, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.user_full_name = user_full_name
        self.setWindowTitle(f"Transactions for {self.user_full_name}")
        self.resize(800, 600)
        self.init_ui()
        self.load_transactions()

    def init_ui(self):
        layout = QVBoxLayout()
        title_label = QLabel(f"Transaction History for: {self.user_full_name}")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)

        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(6) # ID, Type, Amount, Date, Counterparty, Counterparty Account
        self.transactions_table.setHorizontalHeaderLabels(["ID", "Type", "Amount", "Date", "Counterparty", "Counterparty Account"])
        #

        header = self.transactions_table.horizontalHeader()

        # Stretch normal columns
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Type
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Amount
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Date
        header.setSectionResizeMode(4, QHeaderView.Stretch)           # Counterparty
        header.setSectionResizeMode(5, QHeaderView.Stretch)           # Counterparty Account

        # Ensure last column is wide enough for the title
        self.transactions_table.setColumnWidth(5, 220)

        # 
        # self.transactions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.transactions_table.setAlternatingRowColors(True)
        self.transactions_table.verticalHeader().setDefaultSectionSize(35)
        
        layout.addWidget(self.transactions_table)
        self.setLayout(layout)

    def load_transactions(self):
        transactions = fetch_user_transactions_with_counterparty(self.user_id)
        self.transactions_table.setRowCount(len(transactions))
        for i, transaction in enumerate(transactions):
            # Assuming transaction structure: (id, type, amount, created_at, counterparty_name, counterparty_account_number)
            for j, val in enumerate(transaction):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.transactions_table.setItem(i, j, item)