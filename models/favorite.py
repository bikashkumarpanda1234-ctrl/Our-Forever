from . import db
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    memory_id = db.Column(db.Integer, nullable=False)
