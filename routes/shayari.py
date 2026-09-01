import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
from models import db
from models.shayari import Shayari

shayari_bp = Blueprint("shayari", __name__)

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}

def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@shayari_bp.route("/")
def shayari():
    # Only show public shayari on the public page
    items = Shayari.query.filter_by(is_private=False).order_by(Shayari.id.desc()).all()
    return render_template("shayari/shayari.html", shayaris=items)

@shayari_bp.route("/add", methods=["GET", "POST"])
def add_shayari():
    if not session.get("logged_in"):
        flash("Please log in as admin to add Shayari. ❤️", "error")
        return redirect(url_for("auth.login", next=request.url))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("text", "").strip()  # maps to body
        photo_file = request.files.get("photo")
        is_private = bool(request.form.get("is_private"))

        if not body:
            flash("Please enter the Shayari text. ❤️", "error")
            return render_template("shayari/add.html")

        # Save Optional Photo
        photo_filename = None
        if photo_file and photo_file.filename != "":
            if allowed_image(photo_file.filename):
                # Put private shayari photos in private folder, public in public
                folder_key = "PRIVATE_PHOTO_FOLDER" if is_private else "PUBLIC_PHOTO_FOLDER"
                upload_folder = current_app.config[folder_key]
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
                return render_template("shayari/add.html")

        # Create Shayari
        new_shayari = Shayari(
            title=title or None,
            body=body,
            image=photo_filename,
            is_private=is_private
        )
        db.session.add(new_shayari)
        db.session.commit()

        flash("Shayari saved successfully! ❤️", "success")
        if is_private:
            return redirect(url_for("private.private_shayari"))
        return redirect(url_for("shayari.shayari"))

    return render_template("shayari/add.html")
