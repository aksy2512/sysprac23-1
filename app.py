from flask import Flask, render_template, request, redirect, send_file
from dotenv import load_dotenv

# import fileparsers
import os
import shutil
import datetime
import threading
import logging
import uuid
import time
# from astropy.table import Table

load_dotenv()
PATHBASE = os.path.abspath(os.path.dirname(__file__))

app = Flask('sysprac')


logger = logging.getLogger('webserver')
logging.basicConfig(level=logging.INFO,
    format='%(name)-10s %(levelname)-8s [%(asctime)s] %(message)s',
)

# ***************************************
# BEGIN server route definitions
# ***************************************


@app.route('/')
def landing_page():
    """Home page. User can upload files from here"""
    return render_template('landing.html')


@app.route('/upload', methods=['POST'])
def upload_page():
    print(PATHBASE)

    id = str(uuid.uuid1())
    f = request.files['formFile']
    d = os.path.join(PATHBASE, 'uploads', id)
    print(d)
    if not os.path.isdir(d):
        os.mkdir(d)
    f.save(os.path.join(d,'raw'))
    
    logger.info(f"Created file {id}")
    
    # DATA = Table(names=('id','upload_time','filename','status','message','error_included'), 
    #          dtype=(str,datetime.datetime,'object',str,'object',bool))
    # Store for each file in data structure
    # [id,datetime.datetime.now(),f.filename,'PROCESSING status']
    # 



    #t = threading.Thread(target=<functions>,args=(id, request.form))
    #t.start()
    # execute functions internally for each uploaded file

    return redirect(f'/display', 303) 
    # user is directed to /display and using AJAX, converted files are displayed

@app.route('/display')
def display_page():
    """Display page to download files"""
    return render_template('display.html')

@app.route('/status/<id>')
def status_check(id):
    """Return JSON with info about whether the uploaded file has been parsed successfully."""
    if os.path.isdir(os.path.join(PATHBASE, 'uploads', id)):
        for row in fileparsers.DATA:
            if row['id']==id :
                stat, msg, err = row['status'], row['message'], bool(row['error_included'])
                break
        return {'status':stat, 'message':msg, 'error_included':err}
    else :
        return '', 404

def cleaner():
    
    global app, PATHBASE
    logger = logging.getLogger('fileclean')
    logger.info('Cleaning up old files')
    x=[]
    for d in os.scandir(os.path.join(PATHBASE, 'uploads')):
        if os.path.isdir(d):
            try :
                shutil.rmtree(d, ignore_errors=True)
                x.append(d)
            except :
                continue
    logger.info("Removed"+str(x))
    while True :
        x = []
        for i, (id, t) in enumerate(zip(fileparsers.DATA['id'], fileparsers.DATA['upload_time'])) :
            if datetime.datetime.now() > t + fileparsers.UPLOAD_LIFETIME :
                try :
                    shutil.rmtree(os.path.join(PATHBASE, 'uploads', id), ignore_errors=True)
                    x.append(i)
                    logger.info(f"Deleted {id}")
                except :
                    logger.exception(f"Couldn't delete {id}")
        fileparsers.DATA.remove_rows(x)
        time.sleep(60 * 5)



if __name__ == '__main__':
    # _cleanerprocess = threading.Thread(target=cleaner)
    # _cleanerprocess.start()
    app.run(host='127.0.0.1', port=5000, debug=True)
