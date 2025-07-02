import requests
from PySide6.QtGui import QIcon
from bs4 import BeautifulSoup
import lxml
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QStandardPaths, QObject, QThread, Signal
from PySide6.QtGui import QIcon
import sys, os

from ui.UI_MainWindow import Ui_MainWindow
from pdf_writer import PDFWriter

basedir = os.path.dirname(__file__)

class Worker(QObject):
    finished = Signal()
    message = Signal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.documents_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        requests.packages.urllib3.disable_warnings()

    def run(self):
        self.fetch_book(self.url)

    def fetch_book(self, url: str):
        html = requests.get(url).text
        self.message.emit("Page downloaded")
        self.write_book(html)

    def write_book(self, html):
        soup = BeautifulSoup(html, "lxml")
        pages = soup.find_all("div", class_="page")
        book_name = soup.find("title").text.split("|")[0].strip()
        file_name = book_name + ".pdf"
        pdf = PDFWriter("P", "mm", "A4", book_name, basedir)
        pdf.add_page()

        for page in pages:
            children = page.find_all()
            for child in children:
                if child.name == "img":
                    relativ_url = child.get("src")
                    pdf.add_image(relativ_url)
                elif not self.check_empty_paragraph(child):
                    try:
                        if child.get("style") == "text-align: center;":
                            pdf.add_title(child.text)
                        elif child.get("class") is not None:
                            if child.get("class")[0] == "toc_h":
                                pdf.add_chapter_title(child.text)
                        else:
                            pdf.add_text(child.text)
                    except Exception as e:
                        print(e)
            self.message.emit(f"Writed Page {pages.index(page)+1} out of {len(pages)}")

        pdf.output(f"{self.documents_path}/{file_name}")
        self.message.emit("File Saved")
        self.finished.emit()

    def check_empty_paragraph(self, paragraph):
        return paragraph.text.strip() == ""

# Меняем дефолтный идентификатор приложухи на свой, чтоб винда правильно отображала иконку на панели задач
try:
    from ctypes import windll  # Only exists on Windows.
    myappid = f'com.anylang-downloader'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Anylang Downloader")
        self.setWindowIcon(QIcon(os.path.join(basedir, "images/logo.ico")))
        self.logs = []

        self.connect_signals_to_slots()

    def run_thread(self):
        url = self.urlField.text()
        self.logsField.clear()
        self.logs = []
        if len(url) >= 10:
            # Создаём поток и рабочий объект
            self.thread = QThread()
            self.worker = Worker(url)
            self.worker.moveToThread(self.thread)

            # Подключаем сигналы и слоты
            self.thread.started.connect(self.worker.run)
            self.worker.message.connect(self.handle_thread_messages)
            self.worker.finished.connect(self.thread_finished)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()
        else:
            self.logs = []
            self.logsField.setPlainText("Enter URL")

    def thread_finished(self):
        self.urlField.clear()

    def handle_thread_messages(self, message):
        self.logs.append(message)
        self.logsField.setPlainText("\n".join(self.logs))
        self.logsField.verticalScrollBar().setValue(self.logsField.verticalScrollBar().maximum())

    def connect_signals_to_slots(self):
        self.runBtn.clicked.connect(self.run_thread)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()