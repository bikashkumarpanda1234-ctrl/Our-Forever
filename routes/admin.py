import os
from flask import Blueprint, render_template, redirect, url_for, request, session, flash, current_app
from werkzeug.utils import secure_filename
from models import db
from models.memory import Memory
from models.video import Video
from models.music import Music
from models.letter import Letter
from models.timeline import Timeline
from models.shayari import Shayari

admin_bp = Blueprint("admin", __name__)

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}
ALLOWED_AUDIO_EXTENSIONS = {"mp3", "wav", "ogg", "m4a", "webm", "opus", "aac"}

def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def allowed_audio(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS

@admin_bp.before_request
def check_admin_login():
    if not session.get("logged_in"):
        flash("Please log in as admin first. ❤️", "error")
        return redirect(url_for("auth.login", next=request.url))

def admin_required():
    return session.get("logged_in")

@admin_bp.route("/")
def dashboard():
    from models.gift import Gift
    from models.shayari import Shayari
    from models.music import Music
    from models.letter import Letter
    from models.timeline import Timeline

    counts = {
        "public_photos": Memory.query.filter_by(is_private=False).count(),
        "private_photos": Memory.query.filter_by(is_private=True).count(),
        "public_videos": Video.query.filter_by(is_private=False).count(),
        "private_videos": Video.query.filter_by(is_private=True).count(),
        "public_music": Music.query.filter_by(is_private=False).count(),
        "private_music": Music.query.filter_by(is_private=True).count(),
        "journey": Timeline.query.count(),
        "public_letters": Letter.query.filter_by(is_private=False).count(),
        "private_letters": Letter.query.filter_by(is_private=True).count(),
        "public_gifts": Gift.query.filter_by(is_private=False).count(),
        "private_gifts": Gift.query.filter_by(is_private=True).count(),
        "public_shayari": Shayari.query.filter_by(is_private=False).count(),
        "private_shayari": Shayari.query.filter_by(is_private=True).count()
    }
    return render_template("admin/dashboard.html", counts=counts)

# =========================================================
# MEMORIES CRUD
# =========================================================

@admin_bp.route("/memories")
def memories():
    if not admin_required(): return redirect(url_for("auth.login"))
    items = Memory.query.order_by(Memory.id.desc()).all()
    return render_template("admin/memories.html", memories=items)

@admin_bp.route("/add-memory", methods=["GET", "POST"])
def add_memory():
    if not admin_required(): return redirect(url_for("auth.login"))
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        is_private = bool(request.form.get("is_private"))
        file = request.files.get("photo")

        if not title:
            flash("Title is required. ❤️", "error")
            return render_template("admin/add_memory.html")

        photo_filename = None
        if file and file.filename != "":
            if allowed_image(file.filename):
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
            else:
                flash("Invalid image format. ❤️", "error")
                return render_template("admin/add_memory.html")

        m = Memory(
            title=title,
            description=description,
            image=photo_filename,
            is_private=is_private
        )
        db.session.add(m)
        db.session.commit()

        flash("Memory added successfully! ❤️", "success")
        return redirect(url_for("admin.memories"))

    return render_template("admin/add_memory.html")

@admin_bp.route("/edit-memory/<int:memory_id>", methods=["GET", "POST"])
def edit_memory(memory_id):
    if not admin_required(): return redirect(url_for("auth.login"))
    m = Memory.query.get_or_404(memory_id)
    if request.method == "POST":
        m.title = request.form.get("title", m.title).strip()
        m.description = request.form.get("description", m.description).strip()
        db.session.commit()
        flash("Memory updated successfully! ❤️", "success")
        return redirect(url_for("admin.memories"))
    return render_template("admin/edit_memory.html", memory=m)

@admin_bp.route("/delete-memory/<int:memory_id>")
def delete_memory(memory_id):
    if not admin_required(): return redirect(url_for("auth.login"))
    m = Memory.query.get_or_404(memory_id)
    # Delete associated file
    if m.image:
        folder_key = "PRIVATE_PHOTO_FOLDER" if m.is_private else "PUBLIC_PHOTO_FOLDER"
        file_path = os.path.join(current_app.config[folder_key], m.image)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                current_app.logger.error(f"Error removing memory photo: {e}")

    db.session.delete(m)
    db.session.commit()
    flash("Memory deleted! ❤️", "success")
    return redirect(url_for("admin.memories"))

# =========================================================
# VIDEOS CRUD
# =========================================================

@admin_bp.route("/videos")
def videos():
    if not admin_required(): return redirect(url_for("auth.login"))
    items = Video.query.order_by(Video.id.desc()).all()
    return render_template("admin/videos.html", videos=items)

@admin_bp.route("/edit-video/<int:video_id>", methods=["GET", "POST"])
def edit_video(video_id):
    if not admin_required(): return redirect(url_for("auth.login"))
    v = Video.query.get_or_404(video_id)
    if request.method == "POST":
        v.title = request.form.get("title", v.title).strip()
        v.description = request.form.get("description", v.description).strip()
        db.session.commit()
        flash("Video updated! ❤️", "success")
        return redirect(url_for("admin.videos"))
    return render_template("admin/edit_video.html", video=v)

@admin_bp.route("/delete-video/<int:video_id>")
def delete_video(video_id):
    if not admin_required(): return redirect(url_for("auth.login"))
    v = Video.query.get_or_404(video_id)
    if v.path:
        folder_key = "PRIVATE_VIDEO_FOLDER" if v.is_private else "PUBLIC_VIDEO_FOLDER"
        file_path = os.path.join(current_app.config[folder_key], v.path)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                current_app.logger.error(f"Error removing video file: {e}")

    db.session.delete(v)
    db.session.commit()
    flash("Video deleted! ❤️", "success")
    return redirect(url_for("admin.videos"))

# =========================================================
# MUSIC CRUD
# =========================================================

@admin_bp.route("/music")
def music():
    if not admin_required(): return redirect(url_for("auth.login"))
    items = Music.query.order_by(Music.id.desc()).all()
    return render_template("admin/music.html", music=items)

@admin_bp.route("/edit-music/<int:music_id>", methods=["GET", "POST"])
def edit_music(music_id):
    if not admin_required(): return redirect(url_for("auth.login"))
    m = Music.query.get_or_404(music_id)
    if request.method == "POST":
        m.title = request.form.get("title", m.title).strip()
        m.artist = request.form.get("artist", m.artist).strip()

        song_file = request.files.get("song")
        cover_file = request.files.get("cover")

        if song_file and song_file.filename != "":
            if allowed_audio(song_file.filename):
                songs_folder = current_app.config["MUSIC_FOLDER"]
                os.makedirs(songs_folder, exist_ok=True)
                song_filename = secure_filename(song_file.filename)
                base, ext = os.path.splitext(song_filename)
                counter = 1
                while os.path.exists(os.path.join(songs_folder, song_filename)):
                    song_filename = f"{base}_{counter}{ext}"
                    counter += 1
                song_file.save(os.path.join(songs_folder, song_filename))
                m.file = song_filename

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
                m.cover = cover_filename

        db.session.commit()
        flash("Song details updated! ❤️", "success")
        return redirect(url_for("admin.music"))
    return render_template("admin/edit_music.html", music=m)

@admin_bp.route("/delete-music/<int:music_id>")
def delete_music(music_id):
    if not admin_required(): return redirect(url_for("auth.login"))
    m = Music.query.get_or_404(music_id)
    if m.file:
        file_path = os.path.join(current_app.config["MUSIC_FOLDER"], m.file)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                current_app.logger.error(f"Error removing song file: {e}")
    if m.cover:
        cover_path = os.path.join(current_app.config["MUSIC_COVER_FOLDER"], m.cover)
        if os.path.exists(cover_path):
            try:
                os.remove(cover_path)
            except Exception as e:
                current_app.logger.error(f"Error removing cover file: {e}")

    db.session.delete(m)
    db.session.commit()
    flash("Song deleted! ❤️", "success")
    return redirect(url_for("admin.music"))

# =========================================================
# JOURNEY / TIMELINE CRUD
# =========================================================

@admin_bp.route("/timeline")
def timeline():
    if not admin_required(): return redirect(url_for("auth.login"))
    items = Timeline.query.order_by(Timeline.date.desc()).all()
    return render_template("admin/timeline.html", timeline=items)

@admin_bp.route("/edit-timeline/<int:timeline_id>", methods=["GET", "POST"])
def edit_timeline(timeline_id):
    if not admin_required(): return redirect(url_for("auth.login"))
    t = Timeline.query.get_or_404(timeline_id)
    if request.method == "POST":
        t.date = request.form.get("date", t.date).strip()
        t.title = request.form.get("title", t.title).strip()
        t.description = request.form.get("description", t.description).strip()
        db.session.commit()
        flash("Timeline event updated! ❤️", "success")
        return redirect(url_for("admin.timeline"))
    return render_template("admin/edit_timeline.html", event=t)

@admin_bp.route("/delete-timeline/<int:timeline_id>")
def delete_timeline(timeline_id):
    if not admin_required(): return redirect(url_for("auth.login"))
    t = Timeline.query.get_or_404(timeline_id)
    if t.image:
        file_path = os.path.join(current_app.config["PUBLIC_PHOTO_FOLDER"], t.image)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                current_app.logger.error(f"Error removing event photo: {e}")

    db.session.delete(t)
    db.session.commit()
    flash("Timeline event deleted! ❤️", "success")
    return redirect(url_for("admin.timeline"))

# =========================================================
# LETTERS CRUD
# =========================================================

@admin_bp.route("/letters")
def letters():
    if not admin_required(): return redirect(url_for("auth.login"))
    items = Letter.query.order_by(Letter.id.desc()).all()
    return render_template("admin/letters.html", letters=items)

@admin_bp.route("/edit-letter/<int:letter_id>", methods=["GET", "POST"])
def edit_letter(letter_id):
    if not admin_required(): return redirect(url_for("auth.login"))
    l = Letter.query.get_or_404(letter_id)
    if request.method == "POST":
        l.title = request.form.get("title", l.title).strip()
        l.body = request.form.get("letter", l.body).strip()
        db.session.commit()
        flash("Letter content updated! ❤️", "success")
        return redirect(url_for("admin.letters"))
    return render_template("admin/edit_letter.html", letter=l)

@admin_bp.route("/delete-letter/<int:letter_id>")
def delete_letter(letter_id):
    if not admin_required(): return redirect(url_for("auth.login"))
    l = Letter.query.get_or_404(letter_id)
    if l.image:
        file_path = os.path.join(current_app.config["PUBLIC_PHOTO_FOLDER"], l.image)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                current_app.logger.error(f"Error removing letter photo: {e}")

    db.session.delete(l)
    db.session.commit()
    flash("Letter deleted! ❤️", "success")
    return redirect(url_for("admin.letters"))

# =========================================================
# SHAYARI CRUD
# =========================================================

@admin_bp.route("/shayari")
def shayari():
    if not admin_required(): return redirect(url_for("auth.login"))
    items = Shayari.query.order_by(Shayari.id.desc()).all()
    return render_template("admin/shayari.html", shayaris=items)

@admin_bp.route("/edit-shayari/<int:shayari_id>", methods=["GET", "POST"])
def edit_shayari(shayari_id):
    if not admin_required(): return redirect(url_for("auth.login"))
    s = Shayari.query.get_or_404(shayari_id)
    if request.method == "POST":
        s.title = request.form.get("title", s.title).strip()
        s.body = request.form.get("text", s.body).strip()
        db.session.commit()
        flash("Shayari details updated! ❤️", "success")
        return redirect(url_for("admin.shayari"))
    return render_template("admin/edit_shayari.html", shayari=s)

@admin_bp.route("/delete-shayari/<int:shayari_id>")
def delete_shayari(shayari_id):
    if not admin_required(): return redirect(url_for("auth.login"))
    s = Shayari.query.get_or_404(shayari_id)
    if s.image:
        file_path = os.path.join(current_app.config["PUBLIC_PHOTO_FOLDER"], s.image)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                current_app.logger.error(f"Error removing shayari photo: {e}")

    db.session.delete(s)
    db.session.commit()
    flash("Shayari deleted! ❤️", "success")
    return redirect(url_for("admin.shayari"))


# =========================================================
# GIFTS CRUD
# =========================================================

@admin_bp.route("/gifts")
def gifts():
    if not admin_required(): return redirect(url_for("auth.login"))
    from models.gift import Gift
    items = Gift.query.order_by(Gift.id.desc()).all()
    return render_template("admin/gifts.html", gifts=items)

@admin_bp.route("/edit-gift/<int:gift_id>", methods=["GET", "POST"])
def edit_gift(gift_id):
    if not admin_required(): return redirect(url_for("auth.login"))
    from models.gift import Gift
    g = Gift.query.get_or_404(gift_id)
    if request.method == "POST":
        g.title = request.form.get("title", g.title).strip()
        g.description = request.form.get("description", g.description).strip()
        g.giver = request.form.get("giver", g.giver)
        db.session.commit()
        flash("Gift details updated! ❤️", "success")
        return redirect(url_for("admin.gifts"))
    return render_template("admin/edit_gift.html", gift=g)

@admin_bp.route("/delete-gift/<int:gift_id>")
def delete_gift(gift_id):
    if not admin_required(): return redirect(url_for("auth.login"))
    from models.gift import Gift
    g = Gift.query.get_or_404(gift_id)
    if g.image:
        file_path = os.path.join(current_app.config["PUBLIC_PHOTO_FOLDER"], g.image)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                current_app.logger.error(f"Error removing gift photo: {e}")

    db.session.delete(g)
    db.session.commit()
    flash("Gift deleted! ❤️", "success")
    return redirect(url_for("admin.gifts"))

