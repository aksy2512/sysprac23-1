# importing all modules
from DOCX_to_PDF import *
from PDF_to_DOCX import *
# from Audio_to_PDF import *
# from Excel_to_CSV import *
# from Excel_to_TSV import *
# from PDF_to_Image import *
# from image_converter import *
# from HTML_to_PDF import *
from app import User, db
import magic
from multiprocessing import Pool,cpu_count



def convert(dest, *args): # called inside starmap
    query = User.query.filter(User.status == "Pending").order_by(User.created_at.asc()).all()
    # print(query)
    dispatcher = {}
    for file in query:
        if file.originalExtension not in dispatcher.keys():
            dispatcher[file.originalExtension] = [file]
        else:
            dispatcher[file.originalExtension].append(file)
    print("+"*20)
    print("Dispatcher: ")
    print(dispatcher)
    print("+"*20)
    # iterate over each process
    for current_type in dispatcher.keys():
        if current_type == "pdf":
            pass
        elif current_type == "docx":
            DOCX2PDF(dispatcher[current_type])
            print("Competed processing {} format...".format(current_type))
    

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





if __name__ == '__main__':
    print(User.query.all())
    # call conversion apis logic
    # convert("pdf")

    # #examples data
    # data=[['9118c0f8-eaae-11ed-af16-5d2bd66f0fd9','acb0d987-eaae-11ed-af16-5d2bd66f0fd9','pdf'],['9118c0f8-eaae-11ed-af16-5d2bd66f0fd9','acb0d987-eaae-11ed-af16-5d2bd66f0fd9','docx'],['9118c0f8-eaae-11ed-af16-5d2bd66f0fd9','acb0d987-eaae-11ed-af16-5d2bd66f0fd9','pdf']]
    # p = Pool(processes = 8) #max(len(data),cpu_count())
    # result_mult = p.starmap(convert, data)
    # p.close()
    # p.join()
    pass

