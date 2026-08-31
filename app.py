import os

from flask import (
    Flask,
    session,
    redirect,
    url_for,
    render_template,
    send_from_directory,
    request
)

from sqlalchemy import text

from config import Config
from models import db


def create_app():

    # ==================================================
    # CREATE FLASK APP
    # ==================================================

    app = Flask(__name__)

    # ==================================================
    # LOAD CONFIG
    # ==================================================

    app.config.from_object(Config)

    # ==================================================
    # MEDIA FOLDERS
    # ==================================================

    app.config["PUBLIC_PHOTO_FOLDER"] = os.path.join(
        app.root_path,
        "media",
        "photos",
        "public"
    )

    app.config["PRIVATE_PHOTO_FOLDER"] = os.path.join(
        app.root_path,
        "media",
        "photos",
        "private"
    )

    app.config["PUBLIC_VIDEO_FOLDER"] = os.path.join(
        app.root_path,
        "media",
        "videos",
        "public"
    )

    app.config["PRIVATE_VIDEO_FOLDER"] = os.path.join(
        app.root_path,
        "media",
        "videos",
        "private"
    )

    app.config["MUSIC_FOLDER"] = os.path.join(
        app.root_path,
        "media",
        "music",
        "songs"
    )

    app.config["MUSIC_COVER_FOLDER"] = os.path.join(
        app.root_path,
        "media",
        "music",
        "covers"
    )

    app.config["THUMBNAIL_FOLDER"] = os.path.join(
        app.root_path,
        "media",
        "thumbnails"
    )

    # ==================================================
    # CREATE FOLDERS
    # ==================================================

    folders = [
        app.config["PUBLIC_PHOTO_FOLDER"],
        app.config["PRIVATE_PHOTO_FOLDER"],
        app.config["PUBLIC_VIDEO_FOLDER"],
        app.config["PRIVATE_VIDEO_FOLDER"],
        app.config["MUSIC_FOLDER"],
        app.config["MUSIC_COVER_FOLDER"],
        app.config["THUMBNAIL_FOLDER"],
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    # ==================================================
    # UPLOAD SETTINGS
    # ==================================================

    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

    app.config["ALLOWED_IMAGE_EXTENSIONS"] = {
        "jpg",
        "jpeg",
        "png",
        "webp",
        "gif"
    }

    app.config["ALLOWED_VIDEO_EXTENSIONS"] = {
        "mp4",
        "webm",
        "mov",
        "avi"
    }

    app.config["ALLOWED_MUSIC_EXTENSIONS"] = {
        "mp3",
        "wav",
        "ogg",
        "m4a",
        "webm",
        "opus",
        "aac"
    }

    # ==================================================
    # ULTRA-FAST ASSET CACHING HANDLER
    # ==================================================
    @app.after_request
    def add_cache_header(response):
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            response.headers['Cache-Control'] = 'public, max-age=31536000'
        return response

    # ==================================================
    # DATABASE
    # ==================================================

    db.init_app(app)

    # ==================================================
    # IMPORT MODELS
    # ==================================================

    from models.user import User
    from models.memory import Memory
    from models.album import Album
    from models.video import Video
    from models.music import Music
    from models.letter import Letter
    from models.timeline import Timeline
    from models.favorite import Favorite
    from models.shayari import Shayari
    from models.gift import Gift
    from models.love_note import LoveNote
    from models.bucketlist import BucketItem
    from models.reason import LoveReason
    from models.wheel import WheelSettings

    # Avoid unused-import warnings
    _ = (
        User,
        Memory,
        Album,
        Video,
        Music,
        Letter,
        Timeline,
        Favorite,
        Shayari,
        Gift,
        LoveNote,
        BucketItem,
        LoveReason,
        WheelSettings
    )

    # ==================================================
    # CREATE DATABASE TABLES
    # ==================================================

    with app.app_context():
        db.create_all()

        # Seeding admin user
        if User.query.count() == 0:
            admin_user = User(username="admin")
            admin_user.set_password(app.config.get("PRIVATE_PASSWORD", "change-me"))
            db.session.add(admin_user)
            db.session.commit()

        # Seeding default public memories
        if Memory.query.filter_by(is_private=False).count() == 0:
            photos = [
                "love-1.jpg",
                "love-2.jpg",
                "love-3.jpg",
                "love-4.jpg",
                "love-5.jpg",
                "memory-1.jpg",
                "memory-2.jpg",
                "memory-3.jpg",
                "memory-4.jpg",
                "memory-5.webp"
            ]
            titles = [
                "Trishakti Dham Trip 🔱",
                "Under the Green Trees 🌳",
                "Gentle Touch of Love 💕",
                "A Private Sweet Kiss 💋",
                "Our Heart Gesture 💖",
                "A Day to Remember ☀️",
                "Under the Cozy Lights ✨",
                "Just You and Me 🥰",
                "Laughter & Joy 😄",
                "Our Little Adventure 🌲"
            ]
            descriptions = [
                "A blessed day spent together in front of Lord Shiva's statue.",
                "Feeling your warmth as I hold you close in nature's embrace.",
                "Whose gentle touch makes my heart beat faster and brings a smile to my face.",
                "A quiet and sweet private kiss that stays locked in our hearts forever.",
                "Making a heart sign together, indicating our commitment to each other.",
                "Sunny skies, happy hearts, and the perfect company.",
                "A magical evening spent talking for hours under the warm glow.",
                "In your arms is my favorite place in the entire world.",
                "Every laugh shared with you is a moment of pure happiness.",
                "Exploring new paths and making memories that will never fade."
            ]
            for i in range(10):
                db.session.add(Memory(
                    title=titles[i],
                    description=descriptions[i],
                    image=photos[i],
                    is_private=False
                ))
            db.session.commit()

        # Seeding shayaris
        if Shayari.query.count() == 0:
            shayari_list = [
                ("My Forever", "In a world full of temporary things, you are my forever. ❤️"),
                ("My Home", "I found my favourite person, and somehow, I also found my home. ✨"),
                ("Fate", "Some hearts meet by chance, but ours feels written by fate. 💕"),
                ("Ek Tum aur Main", "Ek tum, ek main, aur mohabbat bas... aur kya chahiye zindagi se? ❤️"),
                ("Muskurahat", "Zindagi mein chahe kitni bhi pareshaniyan hon, tumhara ek muskurata hua chehra sab theek kar deta hai. ✨"),
                ("Poori Duniya", "Tumko paakar aisa lagta hai jaise poori duniya mil gayi ho. 💕"),
                ("Haseen Ehsaas", "Aapke saath har din ek haseen ehsaas hai, aap door hain to lagta hai dil udas hai. 🌹"),
                ("Sochna Hi Kaafi Hai", "Tumhe sochna hi mere chehre par muskaan le aata hai. 🥰"),
                ("Aapki Aankhein", "Aapki aankhon mein humne kya dekha, ek naya jahan dekha. ❤️"),
                ("Mohabbat Ka Safar", "Mohabbat ki rahon mein chalta chala jaunga, jab tak tum saath ho... 🌸"),
                ("Beat of My Heart", "You are the beat of my heart, the light of my soul. ✨"),
                ("Tera Haath", "Tera haath pakad kar chalna mujhe sabse accha lagta hai. 💕"),
                ("Favorite Story", "Every love story is beautiful, but ours is my favorite. 🌹"),
                ("Poori Zindagi", "Humne to bas tumse mohabbat ki hai, poori zindagi tumhare naam ki hai. 💍"),
                ("Key to Happiness", "Your smile is the key to my happiness. 🥰"),
                ("Safe Haven", "Holding your hand makes me feel the safest person in the world. 💖"),
                ("Subah Aur Shaam", "Tumse hi subah hoti hai, tumse hi shaam hoti hai. 🌅"),
                ("Fall In Love Again", "Every time I look at you, I fall in love all over again. 💞"),
                ("Dil Fida Hai", "Teri har ada par dil fida hai, tera pyaar hi meri dawa hai. 🩹"),
                ("Sukoon", "Aapki baaton mein ek sukoon hai, jo dil ko behla deta hai. 💌"),
                ("Living Poetry", "You are the poetry I never knew how to write. ✍️"),
                ("Adhoori Zindagi", "Tumhare bina meri zindagi adhoori si lagti hai. 🥀"),
                ("Life's Best Thing", "The best thing to hold onto in life is each other. 🔗"),
                ("Sath Hum", "Hum dono ek dusre ke bina adhure hain, saath milkar hi hum poore hain. 👥"),
                ("Dil Ki Khwahish", "Dil ki bas ek hi khwahish hai, ki tum humesha mere paas raho. 🏡"),
                ("My Sunshine", "You are my sunshine on a rainy day. ☀️"),
                ("Pyaar Ka Asar", "Tumhare pyaar ne meri zindagi ko badal diya hai. 🔄"),
                ("Next To You", "I love you not only for who you are, but for who I am when I am with you. 💓"),
                ("Aankhon Ka Nasha", "Teri aankhon ke nashe mein dil doob gaya hai. 🍷"),
                ("Sacha Pyaar", "Aap se hi dil ka karaar hai, aap se hi sachha pyaar hai. 💗"),
                ("Skip a Beat", "You make my heart skip a beat every time you walk into the room. 💓"),
                ("Aasan Manzil", "Tera haath haath mein ho, to har manzil aasan lagti hai. 🛣️"),
                ("Easiest Thing", "Loving you is the easiest thing I have ever done. 🎈"),
                ("Har Khushi", "Tumse hi har khushi hai, tumhi meri zindagi ho. 🌟"),
                ("Favorite Sound", "Your voice is my favorite sound. 🔊"),
                ("Khas Rishta", "Kuch to khas hai humare rishte mein, jo hume dur hone nahi deta. 🗺️"),
                ("Best Part of Day", "You are the best part of my day. 🗓️"),
                ("Ujaala", "Tere chehre ki raunak se hi meri duniya me ujaala hai. 💡"),
                ("Warm Coffee", "Your love is like a warm cup of coffee on a cold day. ☕"),
                ("Sadaa Pyaar", "Humari kahani sabaq hai pyaar ka, jiski koi maut nahi. 🕰️"),
                ("Happiest Next to You", "I am happiest when I am right next to you. 😊"),
                ("Chhu Liya Dil", "Aapki har ek baat dil ko chhu leti hai. 💘"),
                ("Dream Come True", "You are my dream come true. 🌠"),
                ("Bitaya Har Lamha", "Tere saath bitaya har lamha yaadgaar hai. 📸"),
                ("Complete", "Your love is all I need to feel complete. 🧩"),
                ("Saanson Mein", "Tum meri saanson mein baste ho. 🫁"),
                ("Grow Old Together", "I want to grow old with you. 👴👵"),
                ("Humesha Muskaan", "Tere chehre par humesha muskaan bani rahe, yahi meri dua hai. 🤲"),
                ("Key to My Heart", "You hold the key to my heart. 🔑"),
                ("⏳ Humesha", "Mohabbat tumse hi thi, tumse hi hai, aur tumse hi rahegi. ⏳"),
                ("Adventure", "You are my greatest adventure. 🎒"),
                ("Jaan Hazir Hai", "Teri ek muskurahat par jaan bhi hazir hai. 💝"),
                ("Blessing", "Every moment spent with you is a blessing. 🙏"),
                ("Sahil", "Tumhi meri manzil ho, tumhi mera sahil ho. ⛵"),
                ("Cannot Picture Life", "I cannot picture my life without you. 🖼️"),
                ("Sath Humesha", "Hum dono ek sath humesha muskurate rahein. 😃"),
                ("Breathing Love", "Loving you is like breathing, I cannot stop. 🌬️"),
                ("Gift of Life", "Tum meri zindagi ka sabse haseen tofha ho. 🎁")
            ]
            for title, body in shayari_list:
                db.session.add(Shayari(title=title, body=body))
            db.session.commit()


        # Seeding letter
        if Letter.query.count() == 0:
            db.session.add(Letter(
                title='For the one I choose, every day',
                body='Dear Love,\n\nNo matter how many days pass, I want to keep choosing you. Every single day, in every single way, you are my favorite decision. When I look at your face and hold your hand, I see our little forever.\n\nWith Love ❤️',
                is_private=False
            ))
            db.session.commit()

        # Seeding timeline
        if Timeline.query.count() == 0:
            db.session.add(Timeline(
                date='2025-02-14',
                title='When our story started',
                description='A beautiful memory from our first day. The beginning of our little forever.'
            ))
            db.session.commit()

        # Seeding gifts
        if Gift.query.count() == 0:
            db.session.add(Gift(
                title="Teddy Bear 🧸",
                description="The soft teddy bear she gave me on Valentine's Day. It sits on my desk and reminds me of her cuddle.",
                image="love-4.jpg",
                giver="she_gave"
            ))
            db.session.add(Gift(
                title="Rose and Chocolates 🌹",
                description="The red rose and dairy milk chocolates I gave her on Rose Day.",
                image="love-5.jpg",
                giver="he_gave"
            ))
            db.session.commit()

        # Seeding music
        if Music.query.count() == 0:
            db.session.add(Music(
                title="Tum Se Hi 🌸",
                artist="Mohit Chauhan",
                file="tum_se_hi.mp3",
                cover=""
            ))
            db.session.add(Music(
                title="Zara Zara 🔥",
                artist="Bombay Jayashri",
                file="zara_zara.mp3",
                cover=""
            ))
            db.session.add(Music(
                title="Saanson Ko Saanson Mein 💕",
                artist="Babul Supriyo & Alka Yagnik",
                file="saanson_ko.mp3",
                cover=""
            ))
            db.session.commit()

        # Seeding Love Reasons
        if LoveReason.query.count() == 0:
            reasons_seed = [
                "The way your eyes light up when you laugh. ✨",
                "How you make every ordinary day feel extraordinary. ❤️",
                "Your warm hugs that make all my stress melt away. 🤗",
                "The sweet way you care for me even in small things. 🌸",
                "Your beautiful voice when you call my name. 🎶",
                "The comfort of holding your hand wherever we go. 🤝",
                "Because you are my safest place and my home. 🏡",
                "The silly faces you make to cheer me up. 😄",
                "How you understand me even when I don't say a word. 💕",
                "Because loving you is the easiest thing I have ever done. 💖"
            ]
            for r in reasons_seed:
                db.session.add(LoveReason(text=r))
            db.session.commit()

        # Seeding Bucket List
        if BucketItem.query.count() == 0:
            bucket_seed = [
                ("Watch Sunset Together on a Beach 🌅", "Romance 💖", True),
                ("Late Night Long Drive under the Stars 🚗✨", "Adventure 🎒", True),
                ("Bake a Heart-shaped Cake Together 🎂", "Romance 💖", False),
                ("Visit Taj Mahal Together 🕌", "Travel ✈️", False),
                ("Go on a Romantic Mountain Trekking Trip 🏔️", "Travel ✈️", False),
                ("Cook Our Favorite Dinner Together 🍝", "Romance 💖", False),
                ("Stargaze in a Quiet Open Field 🌌", "Adventure 🎒", False),
                ("Build Our Little Dream Home 🏡", "Milestones 💍", False)
            ]
            for title, cat, completed in bucket_seed:
                db.session.add(BucketItem(title=title, category=cat, is_completed=completed))
            db.session.commit()

        # Seeding WheelSettings
        if WheelSettings.query.count() == 0:
            db.session.add(WheelSettings(id=1, is_locked=False))
            db.session.commit()



    # ==================================================
    # IMPORT BLUEPRINTS
    # ==================================================

    from routes.home import home_bp
    from routes.auth import auth_bp
    from routes.gallery import gallery_bp
    from routes.memories import memories_bp
    from routes.videos import videos_bp
    from routes.music import music_bp
    from routes.timeline import timeline_bp
    from routes.letters import letters_bp
    from routes.private import private_bp
    from routes.admin import admin_bp
    from routes.shayari import shayari_bp
    from routes.gifts import gifts_bp
    from routes.extras import extras_bp

    # ==================================================
    # REGISTER BLUEPRINTS
    # ==================================================

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(gallery_bp, url_prefix="/gallery")
    app.register_blueprint(memories_bp, url_prefix="/memories")
    app.register_blueprint(videos_bp, url_prefix="/videos")
    app.register_blueprint(music_bp, url_prefix="/music")
    app.register_blueprint(timeline_bp, url_prefix="/timeline")
    app.register_blueprint(letters_bp, url_prefix="/letters")
    app.register_blueprint(private_bp, url_prefix="/private")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(shayari_bp, url_prefix="/shayari")
    app.register_blueprint(gifts_bp, url_prefix="/gifts")
    app.register_blueprint(extras_bp, url_prefix="/extras")



    # ==================================================
    # PUBLIC PHOTOS
    # ==================================================

    @app.route("/media/photos/public/<path:filename>")
    def public_photo(filename):
        res = send_from_directory(
            app.config["PUBLIC_PHOTO_FOLDER"],
            filename
        )
        res.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        return res

    # ==================================================
    # PRIVATE PHOTOS
    # ==================================================

    @app.route("/media/photos/private/<path:filename>")
    def private_photo(filename):
        if not session.get("private_unlocked"):
            return redirect(url_for("private.unlock"))
        res = send_from_directory(
            app.config["PRIVATE_PHOTO_FOLDER"],
            filename
        )
        res.headers["Cache-Control"] = "private, max-age=3600"
        return res

    # ==================================================
    # PUBLIC VIDEOS
    # ==================================================

    @app.route("/media/videos/public/<path:filename>")
    def public_video(filename):
        mime_types = {
            ".mp4": "video/mp4",
            ".webm": "video/webm",
            ".mov": "video/quicktime",
            ".avi": "video/x-msvideo"
        }
        ext = os.path.splitext(filename)[1].lower()
        mime = mime_types.get(ext, None)
        res = send_from_directory(
            app.config["PUBLIC_VIDEO_FOLDER"],
            filename,
            conditional=True,
            mimetype=mime
        )
        res.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        res.headers["Accept-Ranges"] = "bytes"
        return res

    # ==================================================
    # PRIVATE VIDEOS
    # ==================================================

    @app.route("/media/videos/private/<path:filename>")
    def private_video(filename):
        if not session.get("private_unlocked"):
            return redirect(url_for("private.unlock"))
        mime_types = {
            ".mp4": "video/mp4",
            ".webm": "video/webm",
            ".mov": "video/quicktime",
            ".avi": "video/x-msvideo"
        }
        ext = os.path.splitext(filename)[1].lower()
        mime = mime_types.get(ext, None)
        res = send_from_directory(
            app.config["PRIVATE_VIDEO_FOLDER"],
            filename,
            conditional=True,
            mimetype=mime
        )
        res.headers["Accept-Ranges"] = "bytes"
        return res

    # ==================================================
    # MUSIC
    # ==================================================

    @app.route("/media/music/<path:filename>")
    def music_file(filename):
        from models.music import Music
        private_track = Music.query.filter_by(
            file=filename,
            is_private=True
        ).first()

        if private_track and not session.get("private_unlocked"):
            return redirect(url_for("private.unlock", next=request.url))

        mime_types = {
            ".mp3": "audio/mpeg",
            ".webm": "audio/webm",
            ".m4a": "audio/mp4",
            ".ogg": "audio/ogg",
            ".wav": "audio/wav",
            ".aac": "audio/aac",
            ".opus": "audio/opus"
        }
        ext = os.path.splitext(filename)[1].lower()
        mime = mime_types.get(ext, "audio/mpeg")

        response = send_from_directory(
            app.config["MUSIC_FOLDER"],
            filename,
            conditional=True,
            mimetype=mime
        )
        response.headers["Accept-Ranges"] = "bytes"
        response.headers["Cache-Control"] = "public, max-age=31536000"
        return response

    # ==================================================
    # MUSIC COVERS
    # ==================================================

    @app.route("/media/music/covers/<path:filename>")
    def music_cover(filename):
        from models.music import Music
        track = Music.query.filter_by(cover=filename).first()
        if track and track.is_private:
            if not session.get("private_unlocked"):
                return redirect(url_for("private.unlock", next=request.url))

        return send_from_directory(
            app.config["MUSIC_COVER_FOLDER"],
            filename
        )

    # ==================================================
    # THUMBNAILS
    # ==================================================

    @app.route("/media/thumbnails/<path:filename>")
    def thumbnail_file(filename):

        return send_from_directory(
            app.config["THUMBNAIL_FOLDER"],
            filename
        )

    # ==================================================
    # DATABASE TEST
    # ==================================================

    @app.route("/db-test")
    def db_test():

        try:

            with db.engine.connect() as connection:

                connection.execute(
                    text("SELECT 1")
                )

            return """
            <!doctype html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Our Forever - Database Test</title>
            </head>

            <body style="
                font-family: Arial;
                text-align: center;
                padding: 80px;
                background: #fff5f7;
                color: #5a3040;
            ">

                <h1>❤️ Our Forever</h1>

                <h2>
                    Database Connected Successfully! ✅
                </h2>

                <p>Flask is running.</p>
                <p>SQLAlchemy is working.</p>
                <p>Database connection is working.</p>

            </body>
            </html>
            """

        except Exception as e:

            return f"""
            <!doctype html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Database Error</title>
            </head>

            <body style="
                font-family: Arial;
                padding: 50px;
                background: #fff5f7;
                color: #5a3040;
            ">

                <h1>Database Connection Failed ❌</h1>

                <pre>{e}</pre>

            </body>
            </html>
            """, 500

    # ==================================================
    # 404 ERROR
    # ==================================================

    @app.errorhandler(404)
    def page_not_found(error):

        try:

            return render_template(
                "404.html"
            ), 404

        except Exception:

            return (
                "404 - Page Not Found ❤️",
                404
            )

    # ==================================================
    # 500 ERROR
    # ==================================================

    @app.errorhandler(500)
    def server_error(error):

        try:

            return render_template(
                "500.html"
            ), 500

        except Exception:

            return (
                "500 - Something went wrong ❤️",
                500
            )

    # ==================================================
    # CONTEXT PROCESSORS
    # ==================================================

    @app.context_processor
    def inject_bg_song():
        from models.music import Music
        song = Music.query.filter_by(
            is_background=True,
            is_private=False
        ).first()
        return dict(default_bg_song=song)

    # ==================================================
    # RETURN APP
    # ==================================================

    return app


# ======================================================
# CREATE APPLICATION
# ======================================================

app = create_app()


# ======================================================
# RUN SERVER
# ======================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
