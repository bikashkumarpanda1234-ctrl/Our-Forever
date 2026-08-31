from . import db
class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    artist = db.Column(db.String(120))
    file = db.Column(db.String(255))
    cover = db.Column(db.String(255))
    is_private = db.Column(db.Boolean, default=False, nullable=False)
    is_background = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

