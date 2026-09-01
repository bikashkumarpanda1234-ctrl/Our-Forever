import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
from models import db
from models.gift import Gift

gifts_bp = Blueprint("gifts", __name__)

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}

def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@gifts_bp.route("/")
def gifts():
    # Only show public gifts on the public page
    he_gifts = Gift.query.filter_by(giver="he_gave", is_private=False).order_by(Gift.id.desc()).all()
    she_gifts = Gift.query.filter_by(giver="she_gave", is_private=False).order_by(Gift.id.desc()).all()
    return render_template("gifts/gifts.html", he_gifts=he_gifts, she_gifts=she_gifts)

@gifts_bp.route("/add", methods=["GET", "POST"])
def add_gift():
    if not session.get("logged_in"):
        flash("Please log in as admin to add gifts. ❤️", "error")
        return redirect(url_for("auth.login", next=request.url))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        giver = request.form.get("giver", "he_gave")
        date = request.form.get("date", "").strip()
        note = request.form.get("note", "").strip()
        is_private = bool(request.form.get("is_private"))
        file = request.files.get("photo")

        if not title:
            flash("Please enter a gift title. ❤️", "error")
            return render_template("gifts/add.html")

        if not file or file.filename == "":
            flash("Please select a gift photo to upload. ❤️", "error")
            return render_template("gifts/add.html")

        if not allowed_image(file.filename):
            flash("Invalid image format. Allowed formats: jpg, jpeg, png, webp, gif. ❤️", "error")
            return render_template("gifts/add.html")

        # Save Photo inside appropriate directory based on privacy
        folder_key = "PRIVATE_PHOTO_FOLDER" if is_private else "PUBLIC_PHOTO_FOLDER"
        upload_folder = current_app.config[folder_key]
        os.makedirs(upload_folder, exist_ok=True)
        
        photo_filename = secure_filename(file.filename)
        base, ext = os.path.splitext(photo_filename)
        counter = 1
        while os.path.exists(os.path.join(upload_folder, photo_filename)):
            photo_filename = f"{base}_{counter}{ext}"
            counter += 1
        file.save(os.path.join(upload_folder, photo_filename))

        # Save to DB
        new_gift = Gift(
            title=title,
            description=description,
            image=photo_filename,
            giver=giver,
            date=date or None,
            note=note or None,
            is_private=is_private
        )
        db.session.add(new_gift)
        db.session.commit()

        flash("Gift added successfully! ❤️", "success")
        if is_private:
            return redirect(url_for("private.private_gifts"))
        return redirect(url_for("gifts.gifts"))

    return render_template("gifts/add.html")
