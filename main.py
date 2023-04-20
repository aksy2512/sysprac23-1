# importing all modules
from DOCX_to_PDF import *
from PDF_to_DOCX import *
if __name__ == '__main__':
    # important to avoid recursion
    # test dox to pdf
    dir = "Data"
    # temp = DOCX2PDF(dir)
    temp = PDF2DOCX(dir)


