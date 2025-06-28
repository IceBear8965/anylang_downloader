import requests
from bs4 import BeautifulSoup
import lxml
import pdfkit
from PySide6.QtWidgets import QMainWindow, QApplication
import sys

from ui.UI_MainWindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect_signals_to_slots()

    def fetch_book(self):
        url = self.urlField.text()
        if len(url) >= 10:
            html = requests.get(url).text

        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        self.parse_book(html)

    def parse_book(self, html):
        soup = BeautifulSoup(html, "lxml")
        pages = soup.find_all("div", class_="page")

    def connect_signals_to_slots(self):
        self.runBtn.clicked.connect(self.fetch_book)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()