import os

from fpdf import FPDF
import requests
from tempfile import NamedTemporaryFile

class PDFWriter(FPDF):
    def __init__(self, orientation='P', unit='mm', format='A4', book_name:str = "", basedir:str=""):
        super().__init__(orientation=orientation, unit=unit, format=format)
        self.book_name = book_name
        fontsdir = os.path.join(basedir, "fonts")
        self.add_font("Jost", "", os.path.join(fontsdir, "Jost-Regular.ttf"), uni = True)
        self.add_font("Jost", "B", os.path.join(fontsdir, "Jost-Bold.ttf"), uni=True)
        self.add_font("Jost-Light", "", os.path.join(fontsdir, "Jost-Light.ttf"), uni=True)

    def header(self):
        self.set_font("Jost", "", 10)
        title_w = self.get_string_width(self.book_name) + 6
        self.set_x(0)
        self.set_y(10)

        self.cell(title_w, 3, self.book_name, ln=True, align="C")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Jost", "B", 12)

        self.cell(0, 10, f"{self.page_no()}", align="C")

    def add_title(self, title: str):
        self.set_font("Jost", "B", size=24)
        self.cell(0, 10, text=title, align="C")
        self.ln(10)

    def add_chapter_title(self, title: str):
        self.set_font("Jost", "B", size=18)
        self.cell(0, 20, text=title)
        self.ln(20)

    def add_text(self, text: str):
        self.set_font("Jost", "", size=14)
        self.multi_cell(0, 8, text=text)
        self.ln()

    def add_image(self, relativ_url: str):
        image_width = 80

        url = f"https://anylang.net{relativ_url}"
        try:
            img = requests.get(url, verify=False).content

            with NamedTemporaryFile(suffix=".jpeg") as f:
                f.write(img)
                self.image(name=f.name, w=image_width, x=((self.w - image_width) / 2))
                self.ln(5)
        except Exception as e:
            pass