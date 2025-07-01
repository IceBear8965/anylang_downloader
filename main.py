import requests
from bs4 import BeautifulSoup
import lxml
from fpdf import FPDF
from tempfile import NamedTemporaryFile
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QStandardPaths
import sys

from ui.UI_MainWindow import Ui_MainWindow
from pdf_writer import PDFWriter

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.documents_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        requests.packages.urllib3.disable_warnings()

        self.connect_signals_to_slots()

    def fetch_book(self):
        url = self.urlField.text()
        if len(url) >= 10:
            html = requests.get(url).text
            self.urlField.clear()
            print("fetched")
            self.write_book(html)

    def write_book(self, html):
        soup = BeautifulSoup(html, "lxml")
        pages = soup.find_all("div", class_="page")
        book_name = soup.find("title").text.split("|")[0].strip()
        file_name = book_name + ".pdf"
        pdf = PDFWriter("P", "mm", "A4", book_name)
        pdf.add_page()
        pdf.add_font("Helvetica", "", "fonts/Helvetica.ttf", uni=True)
        pdf.add_font("Helvetica", "B", "fonts/Helvetica-Bold.ttf", uni=True)

        for page in pages:
            children = page.find_all()
            for child in children:
                if child.name == "img":
                    image_width = 80

                    relativ_url = child.get("src")
                    url = f"https://anylang.net{relativ_url}"
                    response = requests.get(url, verify=False).content

                    with NamedTemporaryFile(suffix=".jpeg") as f:
                        f.write(response)
                        pdf.image(name=f.name, w = image_width, x = ((pdf.w - image_width)/2))

                elif not self.check_empty_paragraph(child):
                    try:
                        if child.get("style") == "text-align: center;":
                            pdf.set_font("Helvetica", "B", size=24)
                            pdf.cell(0, 8, txt=child.text, align="C")
                            pdf.ln()
                        elif child.get("class") is not None:
                            if child.get("class")[0] == "toc_h":
                                pdf.set_font("Helvetica", "B", size=18)
                                pdf.cell(0, 16, txt=child.text)
                                pdf.ln()
                        else:
                            pdf.set_font("Helvetica", "", size=14)
                            pdf.multi_cell(0, 8, txt=child.text)
                            pdf.ln()
                    except Exception as e:
                        print(e)

        pdf.output(f"{self.documents_path}/{file_name}", "F")
        print("done")

    def check_empty_paragraph(self, paragraph):
        return paragraph.text.strip() == ""

    def connect_signals_to_slots(self):
        self.runBtn.clicked.connect(self.fetch_book)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()