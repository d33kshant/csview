import os
from flask import Flask, render_template, request, redirect

UPLOAD_DIR = "uploads"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def is_csv(filename: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == "csv"

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            return "No files selected"
        file = request.files["file"]
        if file.filename == '':
            return "No files selected"
        if file and is_csv(file.filename):
            file.save(os.path.join(UPLOAD_DIR, file.filename))
            return redirect(f"/view/{file.filename}")
        else:
            return "Not a csv file"
    return render_template("upload.html")