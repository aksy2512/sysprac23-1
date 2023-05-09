from flask import Flask, flash, jsonify, request, redirect, url_for, redirect, render_template
from dotenv import load_dotenv
import os
import shutil
import datetime
import threading
import logging
import uuid
import time
import magic
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename
import json

load_dotenv()
PATHBASE = os.path.abspath(os.path.dirname(__file__))

if 'uploads' not in os.listdir():
    print("Creating Upload directory.....")
    os.makedirs('uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
# sets max payload limit of 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.app_context().push()


# making database
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


format_mapping = {
    'JPG':'image/jpeg',
    'PNG':'image/png', 
    'GIF':'image/gif', 
    'BMP':'image/bmp', 
    'TIFF':'image/tiff', 
    'ICO':'image/vnd.microsoft.icon', 
    'ICNS':'image/x-icns',
    'WEBP':'image/webp', 
    'TGA':'image/targa', 
    'PDF':'application/pdf',
    'MP3':'audio/mpeg',
    'WAV':'audio/wav',
    'HTML':'text/html',
    'DOCX':'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'XLSX':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'CSV':'text/csv',
    'TSV':'text/tab-separated-values',
}

magic_numbers = {
    "pdf": bytes([0x25, 0x50, 0x44, 0x46]),
    "png": bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]),
    "xlsx": bytes([0x50, 0x4b, 0x03, 0x04, 0x14, 0x00, 0x08, 0x08]),
    "jpg": bytes([0xff, 0xd8, 0xff, 0xe0, 0x00 ,0x10, 0x4a, 0x46]),
    "docx": bytes([0x50, 0x4b, 0x03, 0x04, 0x14, 0x00, 0x00, 0x00]),
    "wav": bytes([0x52, 0x49,0x46,0x46 ,0xa6, 0xd3 ,0x1b, 0x00]),
    "mp3": bytes([0x49, 0x44, 0x33]),
    "gif": bytes([0x47, 0x49, 0x46, 0x38]),
    "bmp": bytes([0x42, 0x4d]),
    "tiff": bytes([0x49, 0x49, 0x2A, 0x00]),
    "ico": bytes([0x00, 0x00, 0x01, 0x00]),
    "icns": bytes([0x69, 0x63, 0x6e, 0x73]),
    "webp": bytes([0x57, 0x45, 0x42, 0x50])
}

class User(db.Model):
    user_uuid = db.Column(db.Integer, primary_key=True)
    file_uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    desiredExtension = db.Column(db.String(100), nullable=False)
    originalExtension = db.Column(db.String(100), nullable=False)
    path  = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    status = db.Column(db.String(100), nullable=False,server_default="Pending")
    converted_file_path  = db.Column(db.String(100), nullable=False,server_default="NaN")
    

    def __repr__(self):
        print("-"*50)
        print("User_Id: {}\nFile_Id: {}\nFile Name: {}\nCurrentExtension: {}\ndesiredExtension: {}\nPath: {}\nCreated at: {}\nStatus: \
              {}\nconverted_file_path: {}".format(self.user_uuid,self.file_uuid,self.name,self.originalExtension,self.desiredExtension,\
                         self.path,self.created_at,self.status,self.converted_file_path))
        print("-"*50)
        return f'File: {self.path}'

with app.app_context():
    # os.remove("instance")
    db.create_all()

    # db.session.add(User('admin', 'admin@example.com'))
    # db.session.add(User('guest', 'guest@example.com'))
    # db.session.commit()

    # users = User.query.all()
    # print(users)




logger = logging.getLogger('webserver')
logging.basicConfig(level=logging.INFO,
    format='%(name)-10s %(levelname)-8s [%(asctime)s] %(message)s',
)

# ***************************************
# BEGIN server route definitions
# ***************************************

@app.route('/')
def landing_page():
    print("*"*100)
    users = User.query.all()
    print(users)
    """Home page. User can upload files from here"""
    return render_template('landing.html')

def check_extension(file_path, ext):
    return True
    with open(file_path, 'rb') as f:
        file_head = f.read()
        if ext=='txt' or ext=='csv' or ext=='tsv' or ext=='html':
            return True
        if file_head.startswith(magic_numbers[ext]):
            return True
        return False
    

@app.route('/upload', methods=['POST','GET'])
def upload_page():
    if request.method == 'POST':
         # check if the post request has the file part
        # print(type(request.form), request.form.keys())
        # print(type(request.files), request.files.keys())
        # for k in request.form.keys():
        #     print(k,"---",request.form[k])
        # print("**"*10)
        # for k in request.files.keys():
        #     print(k,"---",request.files[k])

        files = {}
        for f in request.files.keys():
            # extract name of file
            filename = secure_filename(request.files[f].filename)
            uuid_here = f.split("_")[1]
            temp = {}
            """ {file_storage :{srctype:{}, target:{}, name:{}}}"""
            # getting src_type, target and name
            for k in request.form.keys():
                if k.split("_")[1] == uuid_here:
                    temp[k.split("_")[0]] = request.form[k]
            temp['uuid']=uuid_here
            files[request.files[f]]=temp
        # print("-"*20)
        # for f in files.keys():
        #     print("{} has uuid :{} name: {}, srctype: {}, targtetype: {}".format(f,files['uuid'],files[f]['name'],files[f]['srctype'],files[f]['target']))
        # print("-"*20)
        # return render_template('landing.html')
    
        if len(request.files) == 0:
            flash('No file part')
            return render_template('landing.html')

        # unique user id
        user_uuid=str(uuid.uuid1())
        # files_descp = []
        print(files.keys())
        for f in files.keys():
            # extract name of file
            filename = files[f]['name']
            # target extension
            originalExtension = [val for val in format_mapping.keys() if val==files[f]['srctype']][0]
            print(originalExtension)
            desiredExtension = files[f]['target']
            # new name
            filename = filename.split(".")[0]+"_"+str(datetime.datetime.now()).replace(" ", "").replace(".","")+"."+filename.split(".")[1]
            # saving files locally
            path =  os.path.join("uploads",filename)
            f.save(path)  
            if(check_extension(path, originalExtension.lower())):  
                print("Here")
                id = str(files[f]['uuid'])  # file id
                # [user_uuid,id,timestamp,desiredExtension]
                obj = User(user_uuid=user_uuid,file_uuid=id,name=filename,desiredExtension=desiredExtension,originalExtension=originalExtension,path=path)
                db.session.add(obj)
                db.session.commit()
            # logger.info(f"Created file {id}")
            else:
                os.remove(path)

        os.system('python3 convert.py')

        return redirect(url_for('.display_page',user_uuid=user_uuid)) 
        # user is directed to /display and using AJAX, converted files are displayed
    else:
        """Home page. User can upload files from here"""
        return render_template('landing.html')

    # print(PATHBASE)

@app.route('/display')
def display_page():
    user_uuid = request.args['user_uuid']
    print(user_uuid)
    """Display page to download files"""
    return render_template('display.html', user_uuid=user_uuid)

@app.route('/status/<id>')
def status_check(id):
    """Return JSON with info about whether the uploaded file has been parsed successfully."""
    query = User.query.filter(User.user_uuid == id).all()
    response = []

    for file in query:
        if file.status == 'Done':
            message = 'File parsed successfully.'
        elif file.status == 'Pending':
            message = 'File parsing pending.'
        else:
            message = 'File parsing failed.'

        status = file.status
        response.append({
            'user_id': file.user_uuid,
            'file_id': file.file_uuid,
            'status': status,
            'message': message
        })

    return jsonify(response)

    # if os.path.isdir(os.path.join(PATHBASE, 'uploads', id)):
    #     for row in fileparsers.DATA:
    #         if row['id']==id :
    #             stat, msg, err = row['status'], row['message'], bool(row['error_included'])
    #             break
    #     return {'status':stat, 'message':msg, 'error_included':err}
    # else :
    #     return '', 404

# def cleaner():
    
#     global app, PATHBASE
#     logger = logging.getLogger('fileclean')
#     logger.info('Cleaning up old files')
#     x=[]
#     for d in os.scandir(os.path.join(PATHBASE, 'uploads')):
#         if os.path.isdir(d):
#             try :
#                 shutil.rmtree(d, ignore_errors=True)
#                 x.append(d)
#             except :
#                 continue
#     logger.info("Removed"+str(x))
#     while True :
#         x = []
#         for i, (id, t) in enumerate(zip(fileparsers.DATA['id'], fileparsers.DATA['upload_time'])) :
#             if datetime.datetime.now() > t + fileparsers.UPLOAD_LIFETIME :
#                 try :
#                     shutil.rmtree(os.path.join(PATHBASE, 'uploads', id), ignore_errors=True)
#                     x.append(i)
#                     logger.info(f"Deleted {id}")
#                 except :
#                     logger.exception(f"Couldn't delete {id}")
#         fileparsers.DATA.remove_rows(x)
#         time.sleep(60 * 5)



if __name__ == '__main__':
    # _cleanerprocess = threading.Thread(target=cleaner)
    # _cleanerprocess.start()
    # Set the secret key to some random bytes. Keep this really secret!
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='127.0.0.1', port=5000, debug=True)
