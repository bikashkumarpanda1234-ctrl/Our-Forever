from . import db

class Gift(db.Model):
    __tablename__ = "gifts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=False)  # Gift photo file
    giver = db.Column(db.String(80), nullable=False)   # "he_gave" or "she_gave"
    date = db.Column(db.String(100), nullable=True)
    note = db.Column(db.Text, nullable=True)
    is_private = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Gift {self.title}>"
