
from multiprocessing import Pool,cpu_count
from multiprocessing.process import current_process
import sys, traceback, os, datetime
import sqlite3

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


DBSCHEMA = {
    "user_uuid" : 0,
    "file_uuid" : 1,
    "name" : 2,
    "desiredExtension" : 3,
    "originalExtension" : 4,
    "path" : 5,
    "created_at" : 6,
    "status" : 7,
    "converted_file_path" : 8,
}

AUDIO_TYPES = ['MP3', 'WAV']
IMAGE_TYPES = ['JPG', 'PNG', 'GIF', 'BMP', 'TIFF', 'ICO', 'ICNS', 'WEBP', 'TGA']

def convert(*file):
    """
    This function is called in each subprocess of multiprocessing.Pool
    Each call is responsible for conversion of 1 assigned file
    :arg: file = (UUID, Original Name, Source Type, Target Type)
    """
    dbconn = sqlite3.connect('instance/database.db')
    dbcurs = dbconn.cursor()
    print(file)

    originalExtension=file[2]
    desiredExtension=file[3]

    fn=originalExtension+"_to_"+desiredExtension
    if originalExtension in AUDIO_TYPES and desiredExtension=='PDF':
        fn="Audio_to_PDF"
    elif originalExtension in IMAGE_TYPES and desiredExtension in IMAGE_TYPES+['PDF']:
        fn="convert_image"
    print(fn)
    
    db_file = dbcurs.execute(f'SELECT * FROM user WHERE file_uuid="{file[0]}"').fetchone()

    # call conversion apis logic
    try:
        fn_call=fn + "("+str(file)+")"
        print("Running: ",fn_call)
        eval(fn_call)
        cfpath = "converted/"+os.path.splitext(file[1])[0]+"."+desiredExtension.lower()
        dbcurs.execute(f"""UPDATE user SET converted_file_path="{cfpath}" WHERE file_uuid="{file[0]}"; """)
        print("Competed processing {} format...".format(fn))
        
    except:
       # Handling of exception (if required)
       print("Error occurred in", fn)
       errlog = []
       for line in traceback.format_exception(*sys.exc_info()):
            errlog.extend(line.rstrip('\n').split('\n'))
       sys.stderr.write("".join(['|\t'+l+'\n' for l in errlog])+'-'*40+'\n')
       dbcurs.execute(f"""UPDATE user SET status="Error" WHERE file_uuid="{file[0]}"; """)
    else:
        # execute if no exception
        dbcurs.execute(f"""UPDATE user SET status="Done" WHERE file_uuid="{file[0]}"; """)
        # del_loc='rm uploads/'+ str(file[1])
        # os.system(del_loc)
    finally:
        # Some code .....(always executed)
        dbconn.commit()
        dbconn.close()



def spawn():
    """
    Identifies all unconverted files and creates a pool of workers to process them
    This is a blocking function due to pool.join(), which is necessary
    Call it in a separate thread for async operation.
    (Warning for Windows : Use __name__=='__main__' guard to prevent recursion)
    """

    dbconn = sqlite3.connect('instance/database.db')
    dbcurs = dbconn.cursor()

    query = dbcurs.execute("""
    SELECT * FROM user WHERE status="Pending" ORDER BY created_at
    """).fetchall()
    # print(query)
    dispatcher = []
    for file in query:
        dispatcher.append((file[DBSCHEMA['file_uuid']], file[DBSCHEMA['name']],
            file[DBSCHEMA['originalExtension']], file[DBSCHEMA['desiredExtension']]))
    # example dispatcher
    # [('983cae96-af8a-4fa7-b2f9-458aabd15c53', 'a1_2023-05-0815:48:35257510.jpg', 'JPG', 'JPG', File: uploads/a1_2023-05-0815:48:35257510.jpg), 
    #  ('e8188470-0957-4820-b35a-0ab83fb6ee32', 'a2_2023-05-0815:48:35270865.png', 'PNG', 'JPG', File: uploads/a2_2023-05-0815:48:35270865.png)]
    dbconn.commit()
    dbconn.close()
    
    # Call this when all APIs are working fine
    p = Pool(processes = 8) #max(len(data),cpu_count())
    result_mult = p.starmap(convert, dispatcher)
    p.close()
    p.join()

