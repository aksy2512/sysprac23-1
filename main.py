# importing all modules
from DOCX_to_PDF import *

if __name__ == '__main__':
    # important to avoid recursion
    # test dox to pdf
    dir = "Data"
    temp = DOCX2PDF(dir)

