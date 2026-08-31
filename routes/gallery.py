from flask import Blueprint, render_template
from models.memory import Memory
gallery_bp = Blueprint("gallery", __name__)

@gallery_bp.route("/")
def gallery():
    memories = Memory.query.filter_by(is_private=False).order_by(Memory.id.desc()).all()
    return render_template("gallery/gallery.html", memories=memories)

@gallery_bp.route("/photo/<int:memory_id>")
def photo(memory_id):
    memory = Memory.query.get_or_404(memory_id)
    return render_template("gallery/photo.html", memory=memory)

@gallery_bp.route("/album/<int:album_id>")
def album(album_id):
    return render_template("gallery/album.html", album_id=album_id)
