from PyPDF2 import PdfReader

reader = PdfReader("./uploads/Kirans_Resume.pdf")
page = reader.pages[0]
text = page.extract_text()
print(text)
