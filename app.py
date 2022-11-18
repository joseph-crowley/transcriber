from flask import Flask
app = Flask(__name__)

##########################################################################################
### set up app
##########################################################################################

## whisper setup

import whisper
model = whisper.load_model("tiny")

## GUI setup

#     template here has two replacetags: header and paragraph
with open('./html/page_template.html', 'r') as f:
    html_template = f.read()

def fill_template(header='',paragraph='',additional_html=''):
    result = html_template.replace("HEADING_REPLACETAG", header)
    result = result.replace("PARAGRAPH_REPLACETAG", paragraph)
    result = result.replace("ADDITIONALHTML_REPLACETAG", additional_html)
    with open('./html/tmp.html','w') as f:
        f.write(result)
    return render_template('./html/tmp.html')

## file setup

import os
import subprocess
from flask import flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'mp3', 'm4a'}
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

##########################################################################################
### route definitions
##########################################################################################

@app.route("/")
def greet_the_guest():
    uploads = subprocess.check_output('ls ./uploads', \
                                             shell=True).decode('ascii').split('\n')[:-1]

    additional_html = ''
    for u in uploads:
        additional_html += f'  <p>{u}'
        additional_html += \
              f'  <a href="http://127.0.0.1:5000/uploads/{u}" target="_blank">Listen</a>'
        additional_html += \
              f'  <a href="http://127.0.0.1:5000/transcribe/{u}" target="_blank">Read</a>'
        additional_html += '</p>'

    additional_html += '  <p>Or try '
    additional_html += \
           '  <a href="http://127.0.0.1:5000/upload" target="_blank">uploading a file</a>'
    additional_html += ' </p>'

    return fill_template(header="Transcribe some audio!", \
                         paragraph="Select from existing audio:", \
                         additional_html=additional_html)

@app.route("/transcribe")
def transcribe():
    transcription = model.transcribe("./uploads/audio.mp3")
    return fill_template(header="Transcription of Audio", paragraph=transcription['text'])

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))

    # fill out template

    additional_html = '''
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''
    return fill_template(header="Upload New File", \
                         paragraph="Select a file for transcription (*.mp3):", \
                         additional_html=additional_html)

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/transcribe/<name>')
def transcribe_file(name):
    transcription = model.transcribe(os.path.join(app.config['UPLOAD_FOLDER'], name))
    return fill_template(header="Transcription of Audio", paragraph=transcription['text'])
