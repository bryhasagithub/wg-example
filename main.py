import os
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

#UPLOAD_FOLDER = '/Users/bry/wg-example/uploads'
UPLOAD_FOLDER = '/Users/brian/wg-example/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'json'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_attrs(filename):
    head, tail = os.path.split(filename)
    file_obj = {
        "name": str(tail),
        "path": str(head),
        "owner": os.stat(filename).st_uid,
        "size": os.stat(filename).st_size,
        "permissions": os.stat(filename).st_mode
    }

    return file_obj

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'data' : 'No file selected for uploading'}), 400
        file = request.files['file']
        # user submits an empty filename
        if file.filename == '':
            return jsonify({'data' : 'No file selected for uploading'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            resp = jsonify({'data' : 'File uploaded successfully!'})
            resp.status_code = 201
            return resp

    if request.method == 'GET':
        # return list of content inside UPLOAD_FOLDER at root upload level
        content_list = []
        for item in os.listdir(UPLOAD_FOLDER):

            if os.path.isfile(os.path.join(UPLOAD_FOLDER, item)):
                content_list.append(get_file_attrs(os.path.join(UPLOAD_FOLDER, item)))

            elif os.path.isdir(os.path.join(UPLOAD_FOLDER, item)):
                content_list.append(item)

        resp = jsonify({'data' : content_list})
        resp.status_code = 200
        return resp

    else:
        resp = jsonify({'data' : 'Please refer to the Git focumentation for this REST API'})
        resp.status_code = 400
        return resp

@app.route('/<path:path>',methods=['GET'])
def get_content(path):
    # return content or list of contents within the requested path.
    if os.path.isfile(os.path.join(UPLOAD_FOLDER, path)):
        return send_from_directory(app.config['UPLOAD_FOLDER'], path)

    elif os.path.isdir(os.path.join(UPLOAD_FOLDER, path)):
        content_list = []
        for item in os.listdir(os.path.join(UPLOAD_FOLDER, path)):
            # handle if file type
            if os.path.isfile(os.path.join(UPLOAD_FOLDER, path, item)):
                file_verbose = get_file_attrs(os.path.join(UPLOAD_FOLDER, path, item))
                content_list.append(file_verbose)

            # handle if dir type
            elif os.path.isdir(os.path.join(UPLOAD_FOLDER, item)):
                content_list.append(item)

        resp = jsonify({'data' : content_list})
        resp.status_code = 200
        return resp

    else:
        resp = jsonify({'data' : 'No file(s) or directory(s) found for ' + path})
        resp.status_code = 404
        return resp

if __name__ == "__main__":
    app.run(debug=True, port=8000)

