from fpdf import FPDF

class PDFWriter(FPDF):
    def __init__(self, orientation='P', unit='mm', format='A4', book_name = ""):
        super().__init__(orientation=orientation, unit=unit, format=format)
        self.book_name = book_name
        self.add_font("Helvetica", "", "fonts/Helvetica.ttf", uni=True)
        self.add_font("Helvetica", "B", "fonts/Helvetica-Bold.ttf", uni=True)

    def header(self):
        self.set_font("Helvetica", "", 10)
        title_w = self.get_string_width(self.book_name) + 6
        self.set_x(0)
        self.set_y(15)

        self.cell(title_w, 3, self.book_name, ln=True, align="C")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "B", 12)

        self.cell(0, 10, f"{self.page_no()}", align="C")