# importing all modules
from API.DOCX_to_PDF import *
from API.PDF_to_DOCX import *
from API.Audio_to_PDF import *
from API.XLSX_to_CSV import *
from API.XLSX_to_TSV import *
from API.PDF_to_JPEG import *
from API.image_converter import *
from API.HTML_to_PDF import *
from app import User, db
import magic
from multiprocessing import Pool,cpu_count



def convert(file, *args): # called inside starmap
    print(file)
    # [file.file_path,file.name,file.originalExtension,file.desiredExtension]
    originalExtension=file[2]
    desiredExtension=file[3]
    file_path="uploads/"+file[0]
    fn=originalExtension+"_to_"+desiredExtension
    if(fn=="WAV_to_PDF" or fn=="MP3_to_PDF"):
        fn="Audio_to_PDF"
    print(fn)

    file = User.query.filter(User.file_uuid == file[0])
    try:
        fn_call=fn + "("+file_path+")"
        eval(fn_call)
        print("Running: ",fn_call)
    except:
       # Handling of exception (if required)
       print("Error occurred in", fn)
       file.status = "Error"
    else:
        # execute if no exception
        file.status = "Done"
    finally:
        # Some code .....(always executed)
        db.session.commit()
        pass

    # calls API
    # # iterate over each process
    # for current_type in dispatcher.keys():
    #     if current_type == "PDF":
    #         pass
    #     elif current_type == "DOCX":
    #         print('yeet'*10)
    #         print(dispatcher[current_type])
    #         # DOCX2PDF(dispatcher[current_type])
    #         print("Competed processing {} format...".format(current_type))
    

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
    # dir = "Audiodata"
    # temp = AUD2PDF(dir)
    ####################################################





if __name__ == '__main__':
    print("Inside convert.py")
    # call conversion apis logic
    # convert("PDF")
    #########################################################
    # Testing on same files
    # temp=User.query.filter()
    # temp.status = "Pending"
    # db.session.commit()
    # print(User.query.all())
    #########################################################

    query = User.query.filter(User.status == "Pending" or User.status == "Active").order_by(User.created_at.asc()).all()
    # print(query)
    dispatcher = []
    for file in query:
        dispatcher.append([file.file_uuid,file.name,file.originalExtension,file.desiredExtension,file])
    
    print(dispatcher)
    # To test individual files
    # convert(dispatcher[0])



    # #examples data
    # data=[['9118c0f8-eaae-11ed-af16-5d2bd66f0fd9','acb0d987-eaae-11ed-af16-5d2bd66f0fd9','pdf'],['9118c0f8-eaae-11ed-af16-5d2bd66f0fd9','acb0d987-eaae-11ed-af16-5d2bd66f0fd9','docx'],['9118c0f8-eaae-11ed-af16-5d2bd66f0fd9','acb0d987-eaae-11ed-af16-5d2bd66f0fd9','pdf']]
    p = Pool(processes = 8) #max(len(data),cpu_count())
    result_mult = p.starmap(convert, dispatcher)
    p.close()
    p.join()


print(User.query.all())