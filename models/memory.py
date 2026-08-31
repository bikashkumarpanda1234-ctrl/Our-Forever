from . import db


class Memory(db.Model):
    __tablename__ = "memories"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(160),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    image = db.Column(
        db.String(255),
        nullable=True
    )

    is_private = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<Memory {self.title}>"