from . import db

class WheelSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unlock_at = db.Column(db.DateTime, nullable=True)
    is_locked = db.Column(db.Boolean, default=False, nullable=False)
    custom_title = db.Column(db.String(255), default="Secret Romantic Date Surprise 💖")
    last_spin_result = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
