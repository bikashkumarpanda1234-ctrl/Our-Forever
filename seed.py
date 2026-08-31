import sys
import pathlib
sys.stdout.reconfigure(encoding='utf-8')
from app import app
from models import db
from models.memory import Memory
from models.letter import Letter
from models.timeline import Timeline

with app.app_context():
    db.create_all()
    photos = sorted([p.name for p in pathlib.Path('media/photos/public').glob('*') if p.is_file() and p.name != '.gitkeep'])
    existing = {m.image for m in Memory.query.all()}
    titles = [
        'A Beautiful Day ❤️', 'One of My Favourite Moments 🥰', 'Just You and Me 💕', 
        'A Memory I Will Keep ✨', 'Our Little Adventure 🌲', 'Forever Looks Good on Us 💖',
        'Smiles & Sunshine ☀️', 'Cozy Moments 🤗', 'Holding Hands 🤝', 'My Favorite View 🌸'
    ]
    for i, photo in enumerate(photos):
        if photo not in existing:
            db.session.add(Memory(
                title=titles[i % len(titles)],
                description='A moment that holds infinite love and warmth in our hearts.',
                image=photo,
                is_private=False
            ))
    
    if Letter.query.count() == 0:
        db.session.add(Letter(title='For the one I choose, every day', body='No matter how many days pass, I want to keep choosing you. ❤️'))
    if Timeline.query.count() == 0:
        db.session.add(Timeline(date='The beginning', title='When our story started', description='Add your real date and story here.'))
    
    db.session.commit()
    print('Seed complete ❤️')

