# importing all modules
from DOCX_to_PDF import *
from PDF_to_DOCX import *
# from Audio_to_PDF import *
# from Excel_to_CSV import *
# from Excel_to_TSV import *
# from PDF_to_Image import *
# from image_converter import *
# from HTML_to_PDF import *
from app import User
from multiprocessing import Pool,cpu_count
def convert(*args): # called inside starmap
    
    print(args)


    ####################################################
    ## convert and save the files
    # test dox to pdf
    # dir = "Data"
    # temp = DOCX2PDF(dir)
    # test excel to csv
    # dir = "ExcelData"
    # temp = EXCEL2TSV(dir)
    # test pdf to image
    # dir = "PDFData"
    # temp = PDF2IMAGE(dir)
    # temp = convert_image('ImageData/a2.jpg', 'png')
    # dir = "PDF2DOCDATA"
    # temp = PDF2DOCX(dir)
    dir = "Audiodata"
    # temp = AUD2PDF(dir)
    ####################################################



    # Databse update to done code[200] instead of Pending

if __name__ == '__main__':

    # call conversion apis logic
    uploads = User.query.all()
    data=[]
    for file in uploads:
        print(file)
        
        # generate data from file and send to
        # data.append(...)

    #examples data
    data=[['9118c0f8-eaae-11ed-af16-5d2bd66f0fd9','acb0d987-eaae-11ed-af16-5d2bd66f0fd9','pdf'],['9118c0f8-eaae-11ed-af16-5d2bd66f0fd9','acb0d987-eaae-11ed-af16-5d2bd66f0fd9','docx'],['9118c0f8-eaae-11ed-af16-5d2bd66f0fd9','acb0d987-eaae-11ed-af16-5d2bd66f0fd9','pdf']]
    p = Pool(processes = 8) #max(len(data),cpu_count())
    result_mult = p.starmap(convert, data)
    p.close()
    p.join()

