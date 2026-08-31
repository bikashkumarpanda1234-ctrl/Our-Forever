# Our Forever ❤️

A romantic personal-memory website built with Flask.

## Features
- Romantic home page with photo memories and shayari
- Gallery and albums
- Videos and music pages
- Relationship timeline
- Letters
- Password-protected private gallery
- Simple admin dashboard
- SQLite database
- Separate CSS/JS modules and animation.css equivalent: `static/css/animations.css`

## Run
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open: http://127.0.0.1:5000

Change `PRIVATE_PASSWORD` and `SECRET_KEY` in `.env`.
