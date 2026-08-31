import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
from models import db
from models.music import Music

music_bp = Blueprint("music", __name__)

ALLOWED_AUDIO_EXTENSIONS = {"mp3", "wav", "ogg", "m4a", "webm", "opus", "aac"}
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}

def allowed_audio(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS

def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@music_bp.route("/")
def music():
    # Only show public tracks on the public page
    tracks = Music.query.filter_by(is_private=False).order_by(Music.id.desc()).all()
    return render_template("music/music.html", tracks=tracks)

@music_bp.route("/api/playlist")
def api_playlist():
    from flask import jsonify
    tracks = Music.query.filter_by(is_private=False).order_by(Music.id.asc()).all()
    data = [{"id": t.id, "title": t.title, "artist": t.artist, "file": t.file} for t in tracks]
    return jsonify(data)

@music_bp.route("/add", methods=["GET", "POST"])
def add_music():
    if not session.get("logged_in"):
        flash("Please log in to manage music. ❤️", "error")
        return redirect(url_for("private.unlock", next=request.url))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        artist = request.form.get("artist", "").strip()
        song_file = request.files.get("song")
        cover_file = request.files.get("cover")
        is_private = bool(request.form.get("is_private"))
        is_background = bool(request.form.get("is_background"))

        if not title:
            flash("Please enter a song title. ❤️", "error")
            return render_template("music/add.html")

        if not song_file or song_file.filename == "":
            flash("Please select an audio file to upload. ❤️", "error")
            return render_template("music/add.html")

        if not allowed_audio(song_file.filename):
            flash("Invalid audio format. Allowed formats: mp3, wav, ogg, m4a. ❤️", "error")
            return render_template("music/add.html")

        # Save Audio File
        songs_folder = current_app.config["MUSIC_FOLDER"]
        os.makedirs(songs_folder, exist_ok=True)
        song_filename = secure_filename(song_file.filename)
        base, ext = os.path.splitext(song_filename)
        counter = 1
        while os.path.exists(os.path.join(songs_folder, song_filename)):
            song_filename = f"{base}_{counter}{ext}"
            counter += 1
        song_file.save(os.path.join(songs_folder, song_filename))

        # Save Cover File if present
        cover_filename = None
        if cover_file and cover_file.filename != "":
            if allowed_image(cover_file.filename):
                covers_folder = current_app.config["MUSIC_COVER_FOLDER"]
                os.makedirs(covers_folder, exist_ok=True)
                cover_filename = secure_filename(cover_file.filename)
                c_base, c_ext = os.path.splitext(cover_filename)
                c_counter = 1
                while os.path.exists(os.path.join(covers_folder, cover_filename)):
                    cover_filename = f"{c_base}_{c_counter}{c_ext}"
                    c_counter += 1
                cover_file.save(os.path.join(covers_folder, cover_filename))
            else:
                flash("Invalid cover image format. Skipped uploading cover. ❤️", "warning")

        # Handle setting as background song
        if is_background:
            Music.query.update({Music.is_background: False})

        # Insert to DB
        new_track = Music(
            title=title,
            artist=artist or "Our Love Song",
            file=song_filename,
            cover=cover_filename,
            is_private=is_private,
            is_background=is_background
        )
        db.session.add(new_track)
        db.session.commit()

        flash("Song added successfully! ❤️", "success")
        if is_private:
            return redirect(url_for("private.private_music"))
        return redirect(url_for("music.music"))

    return render_template("music/add.html")

@music_bp.route("/set-bg/<int:music_id>")
def set_background(music_id):
    if not session.get("logged_in"):
        flash("Please log in as admin first. ❤️", "error")
        return redirect(url_for("private.unlock", next=request.url))

    # Reset all other background flags
    Music.query.update({Music.is_background: False})
    
    # Set selected track
    track = Music.query.get_or_404(music_id)
    track.is_background = True
    db.session.commit()
    
    flash(f"'{track.title}' is now set as the site background music! 🌸", "success")
    return redirect(request.referrer or url_for("music.music"))
