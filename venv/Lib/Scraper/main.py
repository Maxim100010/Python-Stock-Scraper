import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QFileDialog, QLabel
from PySide6.QtGui import QIntValidator

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Exchange Scraper Widget")
        self.setGeometry(100, 100, 500, 350)

        self.layout = QVBoxLayout(self)

        # Adding labels and text inputs
        self.add_labeled_dropdown_input("Which exchange to scrape:", ["NYSE", "NASDAQ", "BOTH"])
        self.add_labeled_integer_input("Current closing price (Limit scraping to stock under e.g. 20$):", minimum=0)
        self.add_labeled_integer_input("Minimum percentual difference between current closing price and future Low price:", minimum=0)

        # Adding label and folder selection input
        self.add_labeled_folder_input("Folder Input:")

        # Adding dropdown and additional input
        self.add_labeled_dropdown_input("Dropdown Input:", ["Option 1", "Option 2", "Option 3"])

        # Adding submit button
        self.button = QPushButton("Submit", self)
        self.button.clicked.connect(self.button_clicked)
        self.layout.addWidget(self.button)

    def add_labeled_text_input(self, label_text):
        label = QLabel(label_text, self)
        text_input = QLineEdit(self)
        self.layout.addWidget(label)
        self.layout.addWidget(text_input)

    def add_labeled_integer_input(self, label_text, minimum=0):
        label = QLabel(label_text, self)
        text_input = QLineEdit(self)
        validator = QIntValidator(minimum, 2147483647)  # Set the maximum value to the maximum integer value supported
        text_input.setValidator(validator)
        self.layout.addWidget(label)
        self.layout.addWidget(text_input)

    def add_labeled_folder_input(self, label_text):
        label = QLabel(label_text, self)
        self.folder_path_input = QLineEdit(self)
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_folder)
        self.layout.addWidget(label)
        self.layout.addWidget(self.folder_path_input)
        self.layout.addWidget(self.browse_button)

    def add_labeled_dropdown_input(self, label_text, options):
        label = QLabel(label_text, self)
        self.layout.addWidget(label)
        self.dropdown = QComboBox(self)
        self.dropdown.addItems(options)
        self.layout.addWidget(self.dropdown)
        self.additional_input = QLineEdit(self)
        self.additional_input.setPlaceholderText("Additional Input")
        self.additional_input.hide()
        self.layout.addWidget(self.additional_input)
        self.dropdown.currentIndexChanged.connect(self.option_selected)

    def option_selected(self, index):
        selected_option = self.dropdown.currentText()
        if selected_option == "Option 3":
            self.additional_input.show()
        else:
            self.additional_input.hide()

    def browse_folder(self):
        folder_dialog = QFileDialog(self)
        folder_dialog.setFileMode(QFileDialog.Directory)
        if folder_dialog.exec():
            folder_path = folder_dialog.selectedFiles()[0]
            self.folder_path_input.setText(folder_path)

    def button_clicked(self):
        # Getting values from inputs
        exchange_option = self.dropdown.currentText()
        text_inputs = [self.layout.itemAt(i).widget().text() for i in range(1, 4)]  # Exclude labels
        folder_path = self.folder_path_input.text()
        selected_option = self.dropdown.currentText()
        additional_text = self.additional_input.text() if self.additional_input.isVisible() else None

        # Printing values
        print("Exchange to scrape:", exchange_option)
        print("Text inputs:", text_inputs)
        print("Folder path:", folder_path)
        print("Selected option:", selected_option)
        print("Additional text:", additional_text)
        # You can perform any action with the user inputs here

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())

