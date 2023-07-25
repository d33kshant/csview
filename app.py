import os, math, pandas as pd
from flask import Flask, render_template, request, redirect

UPLOAD_DIR = "uploads"
MAX_ITEM_PER_PAGE = 20

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

@app.route("/view/<filename>")
def view(filename):
    sort_by = request.args.get('sort_by', None)
    sort_desc = request.args.get('desc', 0, type=int)

    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * MAX_ITEM_PER_PAGE

    file_path = os.path.join(UPLOAD_DIR, filename)
    csv = pd.read_csv(file_path)
    page_count = math.ceil(len(csv.index) / MAX_ITEM_PER_PAGE )
    
    if sort_by != '' and sort_by in csv.keys():
        csv = csv.sort_values(sort_by.lower(), ascending=bool(sort_desc))

    csv = csv.iloc[offset:offset+MAX_ITEM_PER_PAGE]

    columns = csv.keys().to_list()
    rows = []
    for item in zip(csv.index.tolist(), csv.values.tolist()):
        rows.append([item[0]]+item[1])
    return render_template("view.html", columns=columns, rows=rows, page_count=page_count)

if __name__ == "__main__":
    app.run(debug=True)