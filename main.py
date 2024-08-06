from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QWidget, QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add Student", self)                           #Self argument will connect QAction to the actual class
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)
        
        delete_student_action = QAction("Delete Student", self)
        delete_student_action.triggered.connect(self.delete)  
        file_menu_item.addAction(delete_student_action)
                      
        about_action = QAction("About", self)                                       #Self argument will connect QAction to the actual class
        help_menu_item.addAction(about_action) 
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        
        search_action = QAction("Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)
        
        #Create Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM  students")
        self.table.setRowCount(0)                                                               # Resets the table and loads the data
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)                                                    #Use to insert an empty row to row number
            #print(row_number)
            #print(row_data)
            for column_number, data in enumerate(row_data):                                     #Populate cells of that row with actual data
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))      # Secify row and which column
        connection.close()
    
    #Instantiate an insert dialogue class
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()
    
    #Instantiate an search dialogue class    
    def search(self):
        dialog = SearchDialog()
        dialog.exec()
    
    #Instantiate a delete dialogue class
    def delete(self):
        dialog = DeleteDialogue()
        dialog.exec()
        
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)
        self.setLayout(layout)
    
        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)
    
        # Add a submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)
        
        self.setLayout(layout)
        
    def add_student(self): 
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, course, mobile))
        
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        #   Set Window title and size
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        #   Create layout and input widget
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        # Create button
        button = QPushButton("Search")   
        button.clicked.connect(self.search)
        layout.addWidget(button)
        
        self.setLayout(layout)
    
    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("Select * FROM students WHERE name = ?", (name,))
        rows = list(result)
        print(rows)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(),1).setSelected(True)
        cursor.close()
        connection.close()

class DeleteDialogue(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
    
        #Create layout and input widget
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        # Create submit button
        button = QPushButton("Delete")
        button.clicked.connect(self.delete)
        layout.addWidget(button)
        
        self.setLayout(layout)
    
    def delete(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("DELETE FROM students WHERE name=?" , (name,))
        result2 = cursor.execute("Select * FROM students")
        
        rows = list(result2)
        print(rows)
        
        
        
        cursor.close()
        connection.close()
   

        
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec()) 