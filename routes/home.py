import os
from flask import Blueprint, render_template, current_app

from models.memory import Memory
from models.video import Video
from models.music import Music
from models.letter import Letter
from models.timeline import Timeline
from models.shayari import Shayari

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    # Home page = all public memories for long romantic story
    memories = (
        Memory.query
        .filter_by(is_private=False)
        .order_by(Memory.id.asc())
        .all()
    )

    # Previews for other sections (limit to 3 for recent activity)
    shayaris = Shayari.query.order_by(Shayari.id.desc()).limit(3).all()
    videos = Video.query.filter_by(is_private=False).order_by(Video.id.asc()).all()
    tracks = Music.query.order_by(Music.id.desc()).limit(3).all()
    timeline = Timeline.query.filter(Timeline.image.isnot(None)).order_by(Timeline.id.asc()).all()
    letters = Letter.query.filter_by(is_private=False).order_by(Letter.id.desc()).limit(3).all()

    return render_template(
        "home/index.html",
        memories=memories,
        shayaris=shayaris,
        videos=videos,
        tracks=tracks,
        timeline=timeline,
        letters=letters
    )