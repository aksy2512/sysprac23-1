# importing all modules
from DOCX_to_PDF import *
from Excel_to_CSV import *
from Excel_to_TSV import *
from PDF_to_Image import *

if __name__ == '__main__':
    # important to avoid recursion
    # test dox to pdf
    # dir = "Data"
    # temp = DOCX2PDF(dir)
    # test excel to csv
    # dir = "ExcelData"
    # temp = EXCEL2TSV(dir)
    # test pdf to image
    dir = "PDFData"
    temp = PDF2IMAGE(dir)