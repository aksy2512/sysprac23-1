# importing all modules
from API.DOCX_to_PDF import *
from API.PDF_to_DOCX import *
from API.Audio_to_PDF import *
from API.XLSX_to_CSV import *
from API.XLSX_to_TSV import *
from API.PDF_to_JPG import *
from API.image_converter import *
from API.HTML_to_PDF import *
from API.MP3_to_WAV import *
from API.WAV_to_MP3 import *
from app import User, db
import magic
from multiprocessing import Pool,cpu_count
import sys, traceback

AUDIO_TYPES = ['MP3', 'WAV']
IMAGE_TYPES = ['JPG', 'PNG', 'GIF', 'BMP', 'TIFF', 'ICO', 'ICNS', 'WEBP', 'TGA']

def convert(*file): # called inside starmap
    print(file)
    # file = (file.file_uuid,file.name,file.originalExtension,file.desiredExtension)
    originalExtension=file[2]
    desiredExtension=file[3]

    fn=originalExtension+"_to_"+desiredExtension
    if originalExtension in AUDIO_TYPES and desiredExtension=='PDF':
        fn="Audio_to_PDF"
    elif originalExtension in IMAGE_TYPES and desiredExtension in IMAGE_TYPES+['PDF']:
        fn="convert_image"
    print(fn)
    
    db_file = User.query.filter(User.file_uuid == file[0]).first()

    # call conversion apis logic
    try:
        fn_call=fn + "("+str(file)+")"
        print("Running: ",fn_call)
        eval(fn_call)
        db_file.converted_file_path="converted/"+file[1].split(".")[0]+"."+desiredExtension.lower()
        print("Competed processing {} format...".format(fn))
        del_loc='rm uploads/'+ str(file[1])
        os.system(del_loc)
    except:
       # Handling of exception (if required)
       print("Error occurred in", fn)
       errlog = []
       for line in traceback.format_exception(*sys.exc_info()):
            errlog.extend(line.rstrip('\n').split('\n'))
       sys.stderr.write("".join(['|\t'+l+'\n' for l in errlog])+'-'*40+'\n')
       db_file.status = "Error"
    else:
        # execute if no exception
        db_file.status = "Done"
    finally:
        # Some code .....(always executed)
        db.session.commit()


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
    #########################################################
    # Testing on same files by changing their status from Error/Done to Pending
    # result_data = {'status': 'Pending'}
    # User.query.filter_by().update(result_data)
    # db.session.commit()
    # print(User.query.all())
    #########################################################

    query = User.query.filter(User.status == "Pending").order_by(User.created_at.asc())
    # print(query)
    dispatcher = []
    for file in query:
        dispatcher.append((file.file_uuid,file.name,file.originalExtension,file.desiredExtension))
    
    # To test individual files
    # convert(dispatcher[index])
    
    print(dispatcher)

    # example dispatcher
    # [('983cae96-af8a-4fa7-b2f9-458aabd15c53', 'a1_2023-05-0815:48:35257510.jpg', 'JPG', 'JPG', File: uploads/a1_2023-05-0815:48:35257510.jpg), 
    #  ('e8188470-0957-4820-b35a-0ab83fb6ee32', 'a2_2023-05-0815:48:35270865.png', 'PNG', 'JPG', File: uploads/a2_2023-05-0815:48:35270865.png)]
    
    # Call this when all APIs are working fine
    p = Pool(processes = 8) #max(len(data),cpu_count())
    result_mult = p.starmap(convert, dispatcher)
    p.close()
    p.join()

# print(User.query.all())