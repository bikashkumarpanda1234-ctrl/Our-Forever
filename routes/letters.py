import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
from models import db
from models.letter import Letter

letters_bp = Blueprint("letters", __name__)

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}

def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@letters_bp.route("/")
def letters():
    # Only show public letters on the public page
    items = Letter.query.filter_by(is_private=False).order_by(Letter.id.desc()).all()
    return render_template("letters/letters.html", letters=items)

@letters_bp.route("/<int:letter_id>")
def letter(letter_id):
    item = Letter.query.get_or_404(letter_id)
    # Check if the letter is private
    if item.is_private and not session.get("private_unlocked"):
        flash("You need to unlock the Secret Place to read this letter. ❤️", "error")
        return redirect(url_for("private.unlock", next=request.url))
    return render_template("letters/letter.html", letter=item)

@letters_bp.route("/add", methods=["GET", "POST"])
def add_letter():
    if not session.get("logged_in"):
        flash("Please log in as admin to write letters. ❤️", "error")
        return redirect(url_for("auth.login", next=request.url))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("letter", "").strip()
        photo_file = request.files.get("photo")
        is_private = bool(request.form.get("is_private"))

        if not title or not body:
            flash("Please enter title and letter content. ❤️", "error")
            return render_template("letters/add.html")

        # Save Optional Photo
        photo_filename = None
        if photo_file and photo_file.filename != "":
            if allowed_image(photo_file.filename):
                # Save photo inside the public photo folder (same as public timeline/letters images)
                # Note: letters images are served publicly, but if the letter itself is private, we can put it in private photo folder!
                # Yes, let's put it in PRIVATE_PHOTO_FOLDER if private to keep it 100% secure!
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
                return render_template("letters/add.html")

        # Create Letter
        new_letter = Letter(
            title=title,
            body=body,
            image=photo_filename,
            is_private=is_private
        )
        db.session.add(new_letter)
        db.session.commit()

        flash("Letter saved successfully! ❤️", "success")
        if is_private:
            return redirect(url_for("private.private_letters"))
        return redirect(url_for("letters.letters"))

    return render_template("letters/add.html")
