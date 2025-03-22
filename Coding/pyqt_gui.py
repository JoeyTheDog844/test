import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QInputDialog, QMessageBox
from testing import generate_pdf_report  # ✅ Import your corrected function

class PDFExporter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Export Report")

        layout = QVBoxLayout()
        self.export_button = QPushButton("Export to PDF", self)
        self.export_button.clicked.connect(self.ask_user_details)

        layout.addWidget(self.export_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def ask_user_details(self):
        """Ask for user name and lab number before exporting the report"""
        name, ok1 = QInputDialog.getText(self, "User Input", "Enter your name:")
        if not ok1 or not name.strip():
            QMessageBox.warning(self, "Warning", "Name cannot be empty!")
            return

        lab_number, ok2 = QInputDialog.getText(self, "User Input", "Enter your lab number:")
        if not ok2 or not lab_number.strip():
            QMessageBox.warning(self, "Warning", "Lab number cannot be empty!")
            return

        self.export_pdf(name, lab_number)

    def export_pdf(self, name, lab_number):
        """Generate a PDF report with user details"""
        generate_pdf_report(name, lab_number)  # ✅ Now passing name and lab_number
        QMessageBox.information(self, "Success", f"PDF exported successfully!\nSaved as System_Audit_Report.pdf")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFExporter()
    window.show()
    sys.exit(app.exec())
