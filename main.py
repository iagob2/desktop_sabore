# main.py
import sys
from PyQt5.QtWidgets import QApplication
from modern_app import ModernSaboreApp
from api_client import SaboreAPIClient

class SaboreApplication:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Saborê Dashboard")
        self.app.setApplicationVersion("2.0.0")
        self.app.setOrganizationName("Saborê")

        self.api_client = SaboreAPIClient()
        self.main_window = ModernSaboreApp(self.api_client)
        self.main_window.show()

    def run(self):
        return self.app.exec_()

if __name__ == '__main__':
    app = SaboreApplication()
    sys.exit(app.run())