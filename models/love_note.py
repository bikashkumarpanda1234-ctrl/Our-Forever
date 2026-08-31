from . import db

class LoveNote(db.Model):
    __tablename__ = "love_notes"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    color = db.Column(db.String(30), default="note-pink")  # e.g., note-pink, note-yellow, note-blue, note-green
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<LoveNote {self.id}>"
