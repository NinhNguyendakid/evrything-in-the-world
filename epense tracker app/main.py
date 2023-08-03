from PyQt5.QtWidgets import QApplication,QHeaderView,QMessageBox,QMainWindow, QWidget,QLabel,QPushButton,QDateEdit,QTableWidget,QComboBox,QLineEdit,QHBoxLayout,QVBoxLayout,QTableWidgetItem
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
import sys
class ExpenseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('expense tracker app')
        self.resize(1050,500)

        self.main_window = QWidget()
        self.layout = QVBoxLayout(self.main_window)
        self.dateBox = QDateEdit()
        self.dateBox.setDate(QDate.currentDate())

        self.categoryBox = QComboBox()
        
        self.amountbox = QLineEdit()
        self.amountbox.setPlaceholderText('Enter amount quickly')

        self.descriptionedit = QLineEdit()
        self.descriptionedit.setPlaceholderText('Make it ez')

        self.add_button = QPushButton('Add expense')
        self.del_button = QPushButton('Delete expense')

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID","Date","Category","Amout","Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.categoryBox.addItems(['Entertainmnet','Education','Food','House','Car'])

        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()
        
        self.row1.addWidget(QLabel('Date:'))
        self.row1.addWidget(self.dateBox)
        self.row1.addWidget(QLabel('Category:'))
        self.row1.addWidget(self.categoryBox)

        self.row2.addWidget(QLabel('Amount:'))
        self.row2.addWidget(self.amountbox)
        self.row2.addWidget(QLabel("Description:"))
        self.row2.addWidget(self.descriptionedit)
        
        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.del_button)

        self.layout.addLayout(self.row1)
        self.layout.addLayout(self.row2)
        self.layout.addLayout(self.row3)
        self.layout.addWidget(self.table)

        self.setCentralWidget(self.main_window)
        self.show()

        self.add_button.clicked.connect(self.addexpense)
        self.del_button.clicked.connect(self.delete_expense)
        self.setStyleSheet("""
                    QWidget {
                           background-color: #CDC8B1;
                    }
                    
                    QLabel {
                           color: #8B7355;
                           font-size: 25px;
                           font-family: "Lucida Console", "Courier New", monospace;
                    }
                    
                    QLineEdit, QDateEdit, QComboBox, QPushButton{
                        
                           background-color: #CDAA7D;
                           font-family: "Lucida Console", "Courier New", monospace;
                           border-style: solid;
                    }
                    
                    QTableWidget {
                            background-color: #CC9966;
                            color: #333;
                            font-family: "Lucida Console", "Courier New", monospace;
                            border: 2px solid #333;
                            selection-background-color: #ddd;
                           
                    }
                        

                        """)
        self.load_table()

    def addexpense(self):
        date = self.dateBox.date().toString('yyyy-MM-dd')
        category = self.categoryBox.currentText()
        amount = self.amountbox.text()
        description = self.descriptionedit.text()

        query = QSqlQuery()
        query.prepare("""
            INSERT INTO app_date (date,category,amount,description)
            VALUES(?,?,?,?)
        """)

        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        query.exec_()

        self.dateBox.setDate(QDate.currentDate())
        self.categoryBox.setCurrentIndex(0)
        self.amountbox.clear()
        self.descriptionedit.clear()

        self.load_table()

    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self,"ERROR", "YOU MUST CHOOSE ONE TO DELETE")
            return 
            
        confirm = QMessageBox.question(self,"Are u sure?","Do you want to delete",QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.No:
            return

        expense_id = int(self.table.item(selected_row,0).text())

        query = QSqlQuery()
        query.prepare("DELETE FROM app_date WHERE id = ?")
        query.addBindValue(expense_id)
        query.exec_()

        self.load_table()        

    def load_table(self):
        self.table.setRowCount(0)

        query = QSqlQuery("SELECT * FROM app_date")
        row = 0
        while query.next():
            expnense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)

            self.table.insertRow(row)
            self.table.setItem(row,0,QTableWidgetItem(str(expnense_id)))
            self.table.setItem(row,1,QTableWidgetItem(date))
            self.table.setItem(row,2,QTableWidgetItem(category))
            self.table.setItem(row,3,QTableWidgetItem(str(amount)))
            self.table.setItem(row,4,QTableWidgetItem(description))
            row+=1

    




database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("app_date.db")
if not database.open():
    QMessageBox.critical(None, "Error:", "Could not open the database")
    sys.exit(1)

query = QSqlQuery()
query.exec_("""
    CREATE TABLE IF NOT EXISTS app_date(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
    )
""")
    



if __name__ in "__main__":
    app = QApplication([])
    main = ExpenseApp()
    main.show()
    app.exec_()