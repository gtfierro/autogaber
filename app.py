import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename, SharedDataMiddleware
import docker
import time
import yaml
import difflib

c = docker.Client()

ALLOWED_EXTENSIONS = {'py'}

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # limit max upload to 16 MB
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath('.'), 'uploads')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def run_file(filename):
    container = c.create_container('python', 'python /mnt/vol/{0}'.format(filename), volumes=['/mnt/vol'])
    c.start(container, binds={app.config['UPLOAD_FOLDER']: '/mnt/vol'})
    time.sleep(6)
    result = c.logs(container)
    c.stop(container)
    return result

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/<assignment>/upload', methods=['GET','POST'])
def test_assignment(assignment):
    assignment = yaml.load(open('assignments/{0}.yaml'.format(assignment)))
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            expected = assignment['Output'].strip()
            user = run_file(filename).strip()
            print expected
            print user
            print ''.join(difflib.unified_diff(expected, user))
            return redirect('/')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <h3>{0}</h3>
    <p>{1}</p>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''.format(assignment['Title'], assignment['Description'])


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print run_file(filename)
            return redirect('/')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)
