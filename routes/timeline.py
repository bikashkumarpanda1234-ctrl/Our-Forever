import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
from models import db
from models.timeline import Timeline

timeline_bp = Blueprint("timeline", __name__)

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}

def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@timeline_bp.route("/")
def timeline():
    items = Timeline.query.order_by(Timeline.date.asc()).all()
    return render_template("timeline/timeline.html", items=items)

@timeline_bp.route("/add", methods=["GET", "POST"])
def add_timeline():
    if not session.get("logged_in"):
        flash("Please log in as admin to manage timeline events. ❤️", "error")
        return redirect(url_for("auth.login", next=request.url))

    if request.method == "POST":
        date = request.form.get("date", "").strip()
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        photo_file = request.files.get("photo")

        if not date or not title:
            flash("Please enter date and title. ❤️", "error")
            return render_template("timeline/add.html")

        # Save Optional Photo
        photo_filename = None
        if photo_file and photo_file.filename != "":
            if allowed_image(photo_file.filename):
                upload_folder = current_app.config["PUBLIC_PHOTO_FOLDER"]
                os.makedirs(upload_folder, exist_ok=True)
                photo_filename = secure_filename(photo_file.filename)
                base, ext = os.path.splitext(photo_filename)
                counter = 1
                while os.path.exists(os.path.join(upload_folder, photo_filename)):
                    photo_filename = f"{base}_{counter}{ext}"
                    counter += 1
                photo_file.save(os.path.join(upload_folder, photo_filename))
            else:
                flash("Invalid image format. Allowed formats: jpg, jpeg, png, webp, gif. ❤️", "error")
                return render_template("timeline/add.html")

        # Create Timeline
        new_event = Timeline(
            date=date,
            title=title,
            description=description,
            image=photo_filename
        )
        db.session.add(new_event)
        db.session.commit()

        flash("Journey event added successfully! ❤️", "success")
        return redirect(url_for("timeline.timeline"))

    return render_template("timeline/add.html")
