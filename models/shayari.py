from . import db

class Shayari(db.Model):
    __tablename__ = "shayari"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=True)
    body = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    is_private = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Shayari {self.title or 'Romantic'}>"
