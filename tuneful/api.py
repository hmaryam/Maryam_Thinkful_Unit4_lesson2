import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

import models
import decorators
from tuneful import app
from database import session
from utils import upload_path

@app.route("/api/songs", methods=["GET"])
@decorators.accept("application/json")
def songs_get():
    """ Get a list of songs """
    
    songs = session.query(models.Song)
    songs = songs.all()
    
    
    data = json.dumps([song.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/songs", methods=["POST"])
@decorators.accept("application/json")
def songs_post():
    """ Add a new song """
    data = request.json
    
    # Add the post to the database
    song = models.Song(file=data["file"])
    session.add(song)
    session.commit()
    
    # Return a 201 Created, containing the post as JSON and with the
    # Location header set to the location of the post
    data = json.dumps(song.as_dictionary())
    headers = {"Location": url_for("post_get", id=song.id)}
    return Response(data, 201, headers=headers, mimetype="application/json")

@app.route("/api/songs/<int:id>", methods=["DELETE"])
@decorators.accept("application/json")
def song_delete(id):
    song = session.query(models.Song).get(id)
    
    if not song:
        message = "Could not find song with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
    
    session.query(models.Song).filter(models.Song.id == id).delete(synchronize_session=False)
    
    posts = session.query(models.Song).all()
    
    data = json.dumps([song.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/files", methods=["POST"])
@decorators.require("multipart/form-data")
@decorators.accept("application/json")
def file_post():
    file = request.files.get("file")
    if not file:
        data = {"message": "Could not find file data"}
        return Response(json.dumps(data), 422, mimetype="application/json")
    
    filename = secure_filename(file.filename)
    db_file = models.File(filename=filename)
    session.add(db_file)
    session.commit()
    file.save(upload_path(filename))
    
    data = db_file.as_dictionary()
    return Response(json.dumps(data), 201, mimetype="application/json")
