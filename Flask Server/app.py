import os
from flask import Flask, render_template, request, redirect, send_file
from s3_functions import list_files, upload_file, show_image
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
BUCKET = "intelligent-driver-safety-system-s3-bucket"

# @app.route("/")
# def home():
#     contents = list_files(BUCKET)
#     return render_template('index.html')

@app.route("/")
def list():
    # contents = show_image(BUCKET)
    return render_template('index.html')

@app.route('/display')
def display():
    contents = show_image(BUCKET)
    return render_template('display.html', contents=contents)

@app.route('/team')
def team():
    return render_template('team.html')

if __name__ == '__main__':
    app.run(debug=True)
    