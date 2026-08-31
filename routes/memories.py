from flask import Blueprint, render_template
from models.memory import Memory
memories_bp = Blueprint("memories", __name__)

@memories_bp.route("/")
def memories():
    items = Memory.query.filter_by(is_private=False).order_by(Memory.id.desc()).all()
    return render_template("gallery/gallery.html", memories=items)
