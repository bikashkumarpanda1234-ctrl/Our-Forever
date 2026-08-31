import os
from flask import Blueprint, render_template, request, session, redirect, url_for, current_app, flash, abort, send_from_directory
from werkzeug.utils import secure_filename
from models import db
from models.memory import Memory
from models.video import Video
from models.music import Music
from models.letter import Letter
from models.gift import Gift
from models.shayari import Shayari

private_bp = Blueprint("private", __name__)

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "webm", "mov", "avi"}

def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def allowed_video(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

@private_bp.before_request
def check_private_unlocked():
    # Allow access to unlock page and lock page without checking session
    if request.endpoint in ['private.unlock', 'private.lock']:
        return
    if not session.get("private_unlocked"):
        return redirect(url_for("private.unlock", next=request.url))

@private_bp.route("/", methods=["GET", "POST"])
def unlock():
    next_page = request.args.get("next")
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == current_app.config["PRIVATE_PASSWORD"]:
            session["private_unlocked"] = True
            session["logged_in"] = True
            session["username"] = "admin"
            next_url = request.form.get("next")
            if next_url:
                return redirect(next_url)
            return redirect(url_for("private.dashboard"))
        return render_template("private/unlock.html", error="Wrong password ❤️", next=next_page)
    
    if session.get("private_unlocked"):
        return redirect(url_for("private.dashboard"))
        
    return render_template("private/unlock.html", next=next_page)

@private_bp.route("/dashboard")
def dashboard():
    from models.love_note import LoveNote
    photo_count = Memory.query.filter_by(is_private=True).count()
    video_count = Video.query.filter_by(is_private=True).count()
    music_count = Music.query.filter_by(is_private=True).count()
    letter_count = Letter.query.filter_by(is_private=True).count()
    gift_count = Gift.query.filter_by(is_private=True).count()
    shayari_count = Shayari.query.filter_by(is_private=True).count()
    note_count = LoveNote.query.count()

    return render_template(
        "private/dashboard.html",
        photo_count=photo_count,
        video_count=video_count,
        music_count=music_count,
        letter_count=letter_count,
        gift_count=gift_count,
        shayari_count=shayari_count,
        note_count=note_count
    )

@private_bp.route("/gallery")
def private_gallery():
    memories = Memory.query.filter_by(is_private=True).order_by(Memory.id.desc()).all()
    return render_template("private/gallery.html", memories=memories)

@private_bp.route("/videos")
def private_videos():
    videos = Video.query.filter_by(is_private=True).order_by(Video.id.desc()).all()
    return render_template("private/videos.html", videos=videos)

@private_bp.route("/music")
def private_music():
    tracks = Music.query.filter_by(is_private=True).order_by(Music.id.desc()).all()
    return render_template("private/music.html", tracks=tracks)

@private_bp.route("/letters")
def private_letters():
    letters = Letter.query.filter_by(is_private=True).order_by(Letter.id.desc()).all()
    return render_template("private/letters.html", letters=letters)

@private_bp.route("/gifts")
def private_gifts():
    he_gifts = Gift.query.filter_by(is_private=True, giver="he_gave").order_by(Gift.id.desc()).all()
    she_gifts = Gift.query.filter_by(is_private=True, giver="she_gave").order_by(Gift.id.desc()).all()
    return render_template("private/gifts.html", he_gifts=he_gifts, she_gifts=she_gifts)

@private_bp.route("/shayari")
def private_shayari():
    shayaris = Shayari.query.filter_by(is_private=True).order_by(Shayari.id.desc()).all()
    return render_template("private/shayari.html", shayaris=shayaris)

@private_bp.route("/upload/photo", methods=["POST"])
def upload_private_photo():
    file = request.files.get("photo")
    title = request.form.get("title", "Our Private Memory ❤️").strip()
    description = request.form.get("description", "").strip()

    if not file or file.filename == "":
        flash("No photo file selected. ❤️", "error")
        return redirect(url_for("private.private_gallery"))

    if not allowed_image(file.filename):
        flash("Invalid image format. ❤️", "error")
        return redirect(url_for("private.private_gallery"))

    upload_folder = current_app.config["PRIVATE_PHOTO_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(file.filename)
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(os.path.join(upload_folder, filename)):
        filename = f"{base}_{counter}{ext}"
        counter += 1

    file.save(os.path.join(upload_folder, filename))

    new_memory = Memory(
        title=title or "Our Private Memory ❤️",
        description=description,
        image=filename,
        is_private=True
    )
    db.session.add(new_memory)
    db.session.commit()

    flash("Private memory photo uploaded! ❤️", "success")
    return redirect(url_for("private.private_gallery"))

@private_bp.route("/upload/video", methods=["POST"])
def upload_private_video():
    file = request.files.get("video")
    title = request.form.get("title", "Our Private Video ❤️").strip()
    description = request.form.get("description", "").strip()

    if not file or file.filename == "":
        flash("No video file selected. ❤️", "error")
        return redirect(url_for("private.private_videos"))

    if not allowed_video(file.filename):
        flash("Invalid video format. ❤️", "error")
        return redirect(url_for("private.private_videos"))

    upload_folder = current_app.config["PRIVATE_VIDEO_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(file.filename)
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(os.path.join(upload_folder, filename)):
        filename = f"{base}_{counter}{ext}"
        counter += 1

    file.save(os.path.join(upload_folder, filename))

    new_video = Video(
        title=title or "Our Private Video ❤️",
        description=description,
        path=filename,
        is_private=True
    )
    db.session.add(new_video)
    db.session.commit()

    flash("Private memory video uploaded! ❤️", "success")
    return redirect(url_for("private.private_videos"))

@private_bp.route("/notes")
def private_notes():
    from models.love_note import LoveNote
    notes = LoveNote.query.order_by(LoveNote.id.desc()).all()
    return render_template("private/notes.html", notes=notes)

@private_bp.route("/notes/add", methods=["POST"])
def add_note():
    from models.love_note import LoveNote
    body = request.form.get("body", "").strip()
    color = request.form.get("color", "note-pink").strip()

    if not body:
        flash("Note content cannot be empty. ❤️", "error")
        return redirect(url_for("private.private_notes"))

    new_note = LoveNote(body=body, color=color)
    db.session.add(new_note)
    db.session.commit()
    flash("Love note posted to the wall! 💌", "success")
    return redirect(url_for("private.private_notes"))

@private_bp.route("/notes/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    from models.love_note import LoveNote
    note = LoveNote.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash("Love note deleted. 🗑️", "success")
    return redirect(url_for("private.private_notes"))

@private_bp.route("/lock")
def lock():
    session.pop("private_unlocked", None)
    session.pop("logged_in", None)
    session.pop("username", None)
    flash("Secret place locked. ❤️", "success")
    return redirect(url_for("private.unlock"))