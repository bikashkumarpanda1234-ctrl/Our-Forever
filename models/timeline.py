from . import db
class Timeline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(40), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

