from flask import Flask
app = Flask(__name__)

##########################################################################################
### set up app
##########################################################################################

## whisper setup

import whisper
model = whisper.load_model("base")

## GUI setup

#     template here has two replacetags: header and paragraph
with open('./html/page_template.html', 'r') as f:
    html_template = f.read()

def fill_template(header='',paragraph='',additional_html=''):
    result = html_template.replace("HEADING_REPLACETAG", header)
    result = result.replace("PARAGRAPH_REPLACETAG", paragraph)
    result = result.replace("ADDITIONALHTML_REPLACETAG", additional_html)
    return result

## file uploading setup

import os
from flask import flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'mp3'}
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
    return fill_template(header="Just saying Hi", paragraph="Hello World")

@app.route("/transcribe")
def transcribe():
    transcription = model.transcribe("audio.mp3")
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
    return fill_template(header="Upload New File", paragraph="Select a file for transcription (*.mp3):", additional_html=additional_html)

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/transcribe/<name>')
def transcribe_file(name):
    transcription = model.transcribe(os.path.join(app.config['UPLOAD_FOLDER'], name))
    return fill_template(header="Transcription of Audio", paragraph=transcription['text'])
