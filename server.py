import os
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template, session, send_file, send_from_directory, safe_join, abort
from werkzeug.utils import secure_filename
import cv2

from morph import CreateAffineTransform, CreateControlPoints, CreateTriangle


UPLOAD_FOLDER = './uploaded_images'
MORPH_FOLDER = './output_gif'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MORPH_FOLDER'] = MORPH_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home_page():
    return render_template("index.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if (('image1' not in request.files) or ('image2' not in request.files)):
            return jsonify({"File(s) attached": False})
        file1 = request.files['image1']
        file2 = request.files['image2']
        if file1.filename == '' or file2.filename == '':
            return jsonify({"filename(s)": None})
        if (file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename)):
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            flash('Files Uploaded', category='info')
            connectedname = filename1 + "|" + filename2
            return render_template("index.html", connectedname = connectedname)


@app.route('/morph/<images>', methods=['GET'])
def morph(images):
    # USE IMAGE HASHED NAMES IN FUTURE
    image_one_path = os.path.join(app.config['UPLOAD_FOLDER'], images.split("|")[0])
    image_two_path = os.path.join(app.config['UPLOAD_FOLDER'], images.split("|")[1])

    image_one = CreateControlPoints(image_one_path)
    image_two = CreateControlPoints(image_two_path)
    image_one_control_pts = image_one.create_control_points()
    image_two_control_pts = image_two.create_control_points()
    flash('Control Points Created.', category='info')
    del_tri = CreateTriangle(image_one_control_pts, image_two_control_pts).create_triangles()
    flash('Delaunay Triangles Created.', category='info')
    affine = CreateAffineTransform(del_tri, image_one_path, image_two_path, image_one_control_pts, image_two_control_pts)
    affine.perform_affine_transform(40)
    flash('Applied Affine Transform.', category='info')
    try:
        flash('Downloading Now...', category='info')
        return send_from_directory(app.config["MORPH_FOLDER"], filename= 'morphed.gif', as_attachment=True)
    except (FileNotFoundError):
        abort(404)



if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'flaskishereandsoismorphing'
    app.debug = True
    app.run()
