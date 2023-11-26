import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from db import *


class ContactManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = Context()
        
        self.db1 = Context()
        
        
        print(self.db is self.db1)
        
         
         
         #window form   
        fontWindow = self.font()
        fontWindow.setPointSize(10)
        fontWindow.setFamily('tahoma')
        
        self.setFont(fontWindow)
         
        self.setWindowTitle("Contact Manager")
        self.setGeometry(0, 0, 500, 600)

        # Central Widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        
        self.center()
        
        # Layouts
        main_layout = QVBoxLayout(central_widget)
        form_layout = QVBoxLayout()
        button_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        
        
        # creating label
        image_label  = QLabel(self)
         
        image_label.setAlignment(Qt.AlignCenter)
         
        # loading image
        self.pixmap = QPixmap('image.png')
 
        # adding image to label
        image_label .setPixmap(self.pixmap)
 
        # Optional, resize label to image size
        image_label .resize(self.pixmap.width(),
                          self.pixmap.height())     

        main_layout.addWidget(image_label )
        
        # header font
        font = self.font()
        font.setPointSize(24)
        font.setFamily('tahoma')
    

        lblHeader = QLabel(self)
        lblHeader.setFrameStyle(QFrame.Sunken)
        lblHeader.setText("Contact Manager")
        lblHeader.setAlignment(Qt.AlignCenter)
        lblHeader.setFont(font)
        main_layout.addWidget(lblHeader)
        

    

        # Define Labels and Input Fields
        self.id_label = QLabel("ID", self)
        form_layout.addWidget(self.id_label)
        self.id_entry = QLineEdit(self)
        form_layout.addWidget(self.id_entry)
        self.id_entry.setReadOnly(True)

        self.name_label = QLabel("Name", self)
        form_layout.addWidget(self.name_label)
        self.name_entry = QLineEdit(self)
        form_layout.addWidget(self.name_entry)

        self.phone_label = QLabel("Phone", self)
        form_layout.addWidget(self.phone_label)
        self.phone_entry = QLineEdit(self)
        form_layout.addWidget(self.phone_entry)

        self.email_label = QLabel("Email", self)
        form_layout.addWidget(self.email_label)
        self.email_entry = QLineEdit(self)
        form_layout.addWidget(self.email_entry)

        main_layout.addLayout(form_layout)

        # Define Buttons
        
        
        self.add_button = QPushButton('Add Contact', self)
        self.add_button.clicked.connect(self.add_contact)
        button_layout.addWidget(self.add_button)

        

        self.update_button = QPushButton("Update Contact", self)
        self.update_button.clicked.connect(self.update_contact)
        button_layout.addWidget(self.update_button)

        self.remove_button = QPushButton("Remove Contact", self)
        self.remove_button.clicked.connect(self.remove_contact)
        button_layout.addWidget(self.remove_button)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear_inputs)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

        # Search Bar
        self.search_label = QLabel("Search", self)
        search_layout.addWidget(self.search_label)
        self.search_entry = QLineEdit(self)
        self.search_entry.textChanged.connect(self.search_contacts)
        search_layout.addWidget(self.search_entry)

        main_layout.addLayout(search_layout)

        # Define Treeview (Table)
        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabels(['ID', 'Name', 'Phone', 'Email'])
        self.tree.itemClicked.connect(self.update_input_fields)
        main_layout.addWidget(self.tree)

        # Define Exit Button
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.clicked.connect(self.close_window)
        main_layout.addWidget(self.exit_button)

        # Load contacts into Treeview
        self.load_contacts()
        
        
    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def load_contacts(self):
        self.tree.clear()
        items = []
        for row in self.db.read_records():
            item = QTreeWidgetItem()
            item.setText(0, str(row.id))
            item.setText(1, str(row.name))
            item.setText(2, str(row.phone))
            item.setText(3, str(row.email))
            items.append(item)
        self.tree.insertTopLevelItems(0, items)
            

    def add_contact(self):
        name = self.name_entry.text()
        phone = self.phone_entry.text()
        email = self.email_entry.text()

        if name and phone and email:
            self.db.create_record(name, phone, email)
            self.load_contacts()
            self.clear_inputs()
            QMessageBox.information(self, 'Success', 'Contact added successfully!')
        else:
            QMessageBox.information(self, 'Error', 'All fields must be filled!')


    def update_contact(self):
        selected_item = self.tree.currentItem()

        if selected_item:
            contact_id = selected_item.text(0)
            name = self.name_entry.text()
            phone = self.phone_entry.text()
            email = self.email_entry.text()

            if not all([name, phone, email]):
                QMessageBox.information(self, 'Warning', 'All fields must be filled!')
                return
            
            self.db.update_record(contact_id, name, phone, email)
            self.load_contacts()
            self.clear_inputs()
            QMessageBox.information(self, 'Success', 'Contact updated successfully!')


    def remove_contact(self):
        selected_item = self.tree.currentItem()
        
        if selected_item: 
            contact_id = selected_item.text(0)
            if contact_id is not None and contact_id != 0:
                self.db.delete_record(contact_id)
                self.load_contacts()
                self.clear_inputs()
                QMessageBox.information(self, 'Success', 'Contact removed successfully!')
            else:
                QMessageBox.information(self, 'Error', 'Select a contact to remove!')
        else:
            QMessageBox.information(self, 'Error', 'Select a contact to remove!')
            
    def close_window(self):
        self.close()
                
    def clear_inputs(self):
        self.id_entry.clear()
        self.name_entry.clear()
        self.phone_entry.clear()
        self.email_entry.clear()


    def update_input_fields(self, item):
        selectedValues = [item.text(i) for i in range(item.columnCount())]
        self.id_entry.setReadOnly(False)
        self.id_entry.clear()
        self.name_entry.clear()
        self.phone_entry.clear()
        self.email_entry.clear()
        
        if(selectedValues!=None):
            self.id_entry.insert(str(selectedValues[0]))
            self.name_entry.insert( str(selectedValues[1]))
            self.phone_entry.insert( str(selectedValues[2]))
            self.email_entry.insert(str(selectedValues[3]))
            self.id_entry.setReadOnly(True)
            
    def search_contacts(self):
        txtSearch = str(self.search_entry.text().lower())        
        if txtSearch != "":
            self.tree.clear()
            contacts = self.db.search_record(txtSearch)
            items = []
            for row in contacts:
                item = QTreeWidgetItem()
                item.setText(0, str(row.id))
                item.setText(1, str(row.name))
                item.setText(2, str(row.phone))
                item.setText(3, str(row.email))
                items.append(item)
            self.tree.insertTopLevelItems(0, items)
        else :
            self.load_contacts()

        
            
            
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ContactManager()
    main_window.show()
    sys.exit(app.exec_())
