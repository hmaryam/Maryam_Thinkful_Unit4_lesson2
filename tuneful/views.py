from flask import render_template, send_from_directory

from tuneful import app
from utils import upload_path

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(upload_path(), filename)