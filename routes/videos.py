import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
from models import db
from models.video import Video

videos_bp = Blueprint("videos", __name__)

ALLOWED_VIDEO_EXTENSIONS = {"mp4", "webm", "mov", "avi"}

def allowed_video(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

@videos_bp.route("/")
def videos():
    items = Video.query.filter_by(is_private=False).order_by(Video.id.desc()).all()
    return render_template("videos/videos.html", videos=items)

@videos_bp.route("/add", methods=["GET", "POST"])
def add_video():
    if not session.get("logged_in"):
        flash("Please log in to manage videos. ❤️", "error")
        return redirect(url_for("private.unlock", next=request.url))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        is_private = bool(request.form.get("is_private"))
        file = request.files.get("video")

        if not title:
            flash("Please enter a video title. ❤️", "error")
            return render_template("videos/add.html")

        if not file or file.filename == "":
            flash("Please select a video file to upload. ❤️", "error")
            return render_template("videos/add.html")

        if not allowed_video(file.filename):
            flash("Invalid video format. Allowed formats: mp4, webm, mov, avi. ❤️", "error")
            return render_template("videos/add.html")

        # Determine folder based on privacy
        folder_key = "PRIVATE_VIDEO_FOLDER" if is_private else "PUBLIC_VIDEO_FOLDER"
        upload_folder = current_app.config[folder_key]
        os.makedirs(upload_folder, exist_ok=True)

        filename = secure_filename(file.filename)
        base, extension = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(upload_folder, filename)):
            filename = f"{base}_{counter}{extension}"
            counter += 1

        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # Save to DB
        new_video = Video(
            title=title,
            description=description,
            path=filename,  # store filename
            is_private=is_private
        )
        db.session.add(new_video)
        db.session.commit()

        flash("Video uploaded successfully! ❤️", "success")
        if is_private:
            return redirect(url_for("private.private_gallery"))
        return redirect(url_for("videos.videos"))

    return render_template("videos/add.html")
