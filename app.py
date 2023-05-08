from flask import Flask, flash, request, redirect, url_for, redirect, render_template
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

# only run once
# with app.app_context():
#     # os.remove("instance")
#     db.create_all()

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
    file_types = {"pdf":"PDF","docx":"Word","xlsx":"XLSX"}
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    if 'pdf' in file_type:
        return 'PDF' == file_types[ext]
    elif 'word' in file_type:
        return 'Word' == file_types[ext]
    elif 'spreadsheet' in file_type:
        return 'XLSX' == file_types[ext]
    elif 'png' in file_type:
        return 'PNG' == file_types[ext]
    else:
        return 'Unknown' == file_types[ext]

@app.route('/upload', methods=['POST','GET'])
def upload_page():
    if request.method == 'POST':
         # check if the post request has the file part
        print(type(request.form), request.form.keys())
        print(type(request.files), request.files.keys())
        return render_template('landing.html')
        if 'formFile' not in request.files:
            flash('No file part')
            return render_template('landing.html')
        # else fetching the files
        files = request.files.getlist('formFile')
            
        # target extension
        originalExtension = request.form['fileType']
        desiredExtension = request.form['targettype']

        # unique user id
        user_uuid=str(uuid.uuid1())
        # files_descp = []

        for f in files:
            # extract name of file
            filename = secure_filename(f.filename)
            # new name
            filename = filename.split(".")[0]+"_"+str(datetime.datetime.now()).replace(" ", "").replace(".","")+"."+filename.split(".")[1]
            # saving files locally
            path =  os.path.join("uploads",filename)
            f.save(path)  
            if(check_extension(path, originalExtension)):  
                print("Here")
                id = str(uuid.uuid1())  # file id
                # [user_uuid,id,timestamp,desiredExtension]
                obj = User(user_uuid=user_uuid,file_uuid=id,name=filename,desiredExtension=desiredExtension,originalExtension=originalExtension,path=path)
                db.session.add(obj)
                db.session.commit()
            # logger.info(f"Created file {id}")
            else:
                os.remove(path)

        os.system('python convert.py')

        return redirect(f'/display', 303) 
        # user is directed to /display and using AJAX, converted files are displayed
    else:
        """Home page. User can upload files from here"""
        return render_template('landing.html')

    # print(PATHBASE)

@app.route('/display')
def display_page():
    """Display page to download files"""
    return render_template('display.html')

# @app.route('/status/<id>')
# def status_check(id):
#     """Return JSON with info about whether the uploaded file has been parsed successfully."""
#     if os.path.isdir(os.path.join(PATHBASE, 'uploads', id)):
#         for row in fileparsers.DATA:
#             if row['id']==id :
#                 stat, msg, err = row['status'], row['message'], bool(row['error_included'])
#                 break
#         return {'status':stat, 'message':msg, 'error_included':err}
#     else :
#         return '', 404

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
