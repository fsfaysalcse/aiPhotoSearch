from flask import Flask, request, jsonify, render_template
import os
import face_recognition
import database_manager
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_images():
    if 'files[]' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    files = request.files.getlist('files[]')
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process the image for face recognition
            image = face_recognition.load_image_file(filepath)
            face_encodings = face_recognition.face_encodings(image)

            # Save the image info and face encodings to the database
            for encoding in face_encodings:
                database_manager.insert_face_encoding(encoding, filepath)

    return jsonify({'message': 'Files successfully uploaded'})

if __name__ == '__main__':
    app.run(debug=True)
