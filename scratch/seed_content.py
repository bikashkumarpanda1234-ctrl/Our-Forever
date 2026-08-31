import os
import sys
import shutil

# Add project directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db
from models.memory import Memory
from models.letter import Letter

# Paths of uploaded images
UPLOADED_IMAGES = [
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788102498404.png",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788102515546.png",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788102533292.png",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788102570712.png",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788102601817.jpg"
]

def seed_data():
    app = create_app()
    with app.app_context():
        # Destination folder
        dest_folder = app.config["PUBLIC_PHOTO_FOLDER"]
        os.makedirs(dest_folder, exist_ok=True)

        copied_filenames = []

        # 1. Copy images to the media folder
        print("Copying uploaded photos...")
        for i, src_path in enumerate(UPLOADED_IMAGES):
            if os.path.exists(src_path):
                filename = os.path.basename(src_path)
                dest_path = os.path.join(dest_folder, filename)
                shutil.copy2(src_path, dest_path)
                copied_filenames.append(filename)
                print(f"Copied {filename} to {dest_path}")
            else:
                print(f"Warning: Source path {src_path} not found.")

        # Ensure we have filenames to reference
        if not copied_filenames:
            print("Error: No files were copied.")
            return

        # 2. Add memories to the database so they appear on the Home Page
        memories_data = [
            ("Beautiful Ruha at the Beach 🌊", "The waves were singing, but my eyes were only on you. Your smile is brighter than the summer sun.", copied_filenames[0]),
            ("Hold My Hand Forever 🤝", "Looking back at me, guiding me forward. As long as I hold your hand, I know I'm home.", copied_filenames[1]),
            ("A Sweet Kiss of Love 💋", "A sweet, gentle moment that felt like time stood still. My heart beats faster every time you're close.", copied_filenames[2]),
            ("Leaning on Your Shoulder 🤗", "Safe in your warmth, leaning on your shoulder. The best place in the world is right next to you.", copied_filenames[3]),
            ("A Precious Flower for You 🌸", "A little token of love from our walk together. Like this flower, my love for you blooms more beautiful every day.", copied_filenames[4])
        ]

        print("Seeding memories...")
        for title, desc, img_name in memories_data:
            # Check if memory already exists
            existing = Memory.query.filter_by(image=img_name).first()
            if not existing:
                mem = Memory(title=title, description=desc, image=img_name, is_private=False)
                db.session.add(mem)
        
        # 3. Create 50+ long beautiful romantic letters
        print("Generating 50+ beautiful letters...")
        
        # Paragraph builders for letters
        intros = [
            "My dearest Ruha, as I sit down to write this, my heart is filled with thoughts of you.",
            "Dearest Ruha, every day I spend with you becomes the new best day of my life.",
            "My love, writing to you is like opening a box of the sweetest memories we share.",
            "To my favorite person in the world, I hope these words bring a smile to your face.",
            "Ruha, my love, you are the first thing on my mind when I wake and the last when I sleep.",
            "Dear Ruha, sometimes words feel too small to express the depth of what I feel for you.",
            "My beautiful partner, I was just thinking about the day we met, and my heart melted all over again."
        ]
        
        bodies_1 = [
            "Your laughter is my favorite melody. Whenever you smile, the entire world seems to light up. I find myself constantly captivated by the way you look at me, with so much kindness and love in your eyes.",
            "You have this magical way of making all my worries disappear with just a simple hug. Being wrapped in your arms is my ultimate sanctuary, a place where I feel completely safe, cherished, and understood.",
            "I cherish all our little conversations, our inside jokes, and even our quiet silences. Whether we are walking along the beach or just sitting together doing nothing, every second with you is a treasure.",
            "Thank you for being my constant supporter, my best friend, and my greatest comfort. Your strength inspires me, and your gentle soul makes me want to be the best version of myself every single day.",
            "I love the way you hold my hand, tracing patterns on my skin as if writing silent promises. It's in these tiny, quiet details that I realize how blessed I am to walk through life with you."
        ]

        bodies_2 = [
            "I promise to always stand by your side, through every storm and every sunny sky. I want to build a future full of warmth, laughter, and endless adventure with you. You are my today, my tomorrow, and my forever.",
            "Every time I look at you, I see my entire future in your eyes. I see a home filled with warmth, cozy evenings, endless conversations, and a lifetime of shared dreams. You are the love of my life, Ruha.",
            "I want to explore every corner of the world with you, holding your hand and making memories. But even if we stay in one place, just being next to you is the greatest journey I could ever ask for.",
            "No matter where life takes us, my love for you will remain constant, growing deeper and stronger with every passing heartbeat. You have my heart, fully and unconditionally, for the rest of my days.",
            "I love you not only for who you are, but for who I am when I am with you. You bring out a softness and a joy in me that I never knew existed, and for that, I will love you forever."
        ]

        outros = [
            "Forever yours, with all my love and heart.",
            "Yours and only yours, today and always.",
            "Sending you a thousand kisses and all the warmth in my heart.",
            "With all my love, forever and ever.",
            "I love you more than words can say. Yours, now and forever.",
            "Looking forward to our next beautiful moment together. All my love."
        ]

        # Titles for 55 letters
        letter_titles = [
            "The Way Your Eyes Shine ✨",
            "Our Unforgettable Beach Walk 🌊",
            "When Time Stood Still 🕰️",
            "The Magic of Your Smile 😊",
            "Holding Your Hand 🤝",
            "My Favorite Safe Place 🤗",
            "To My Sunshine ☀️",
            "Our Quiet Coffee Evenings ☕",
            "Thinking of You Tonight 🌙",
            "The First Time I Saw You 😍",
            "A Promise of Forever 💍",
            "The Melody of Your Laugh 🎵",
            "Your Warmth in the Winter ❄️",
            "Underneath the Starlit Sky 🌟",
            "Cozy Rainy Days 🌧️",
            "My Heart Beats for You 💓",
            "Our Shared Dreams 💭",
            "The Beauty of Your Soul 🌸",
            "Your Hugs are Home 🏡",
            "A Walk to Remember 🚶‍♂️",
            "Growing Older Together 👵👴",
            "You are My Comfort Zone 🥰",
            "The Sweetest Moments 🍓",
            "My Favorite Nickname for You 🤫",
            "The Day We Shared a Kiss 💋",
            "Every Little Thing You Do 📝",
            "Our Lazy Sunday Mornings 🥞",
            "When I Miss You Most 📞",
            "You are My Inspiration 🎨",
            "A Love Letter with No End ♾️",
            "Your Kindness Melts Me 🍦",
            "To the Girl of My Dreams 🎀",
            "My Eternal Love Letter 💌",
            "Our Midnight Chats 💬",
            "A Lifetime is Not Enough ⏳",
            "You Make Me Believe in Magic 🪄",
            "The Softness of Your Touch 🪶",
            "My Favorite View is You 🌄",
            "The First Day of Forever 🗓️",
            "Your Voice is My Sanctuary 🗣️",
            "The Perfect Love Story 📖",
            "Dancing in the Living Room 💃",
            "Every Heartbeat Whispers Your Name 🗣️",
            "The Flower in My Book 🏵️",
            "My Forever Valentine 🌹",
            "You are My Anchor ⚓",
            "When I Hold Your Hand 🫱🫲",
            "The Best Decision I Ever Made 🎯",
            "A Million Reasons to Love You 🔢",
            "In Your Eyes, I am Home 👀",
            "My Everyday Blessing 🙌",
            "The Future We are Building 🏗️",
            "To My Beautiful Ruha 👸",
            "Our Silent Understandings 🤫",
            "Love That Knows No Bounds 🚀"
        ]

        # Delete existing auto-seeded letters to avoid duplicates
        Letter.query.filter(Letter.title.in_(letter_titles)).delete()
        db.session.commit()

        # Seed 55 letters
        for index, title in enumerate(letter_titles):
            # Alternate through intros, bodies, outros
            intro = intros[index % len(intros)]
            body1 = bodies_1[index % len(bodies_1)]
            body2 = bodies_2[index % len(bodies_2)]
            outro = outros[index % len(outros)]
            
            full_body = f"{intro}\n\n{body1}\n\n{body2}\n\n{outro}"
            
            # Attach one of the copied pictures dynamically (or no picture for some, but user requested with pics attached)
            attached_img = copied_filenames[index % len(copied_filenames)]
            
            # Make some private, some public (e.g. alternate)
            is_priv = (index % 3 == 0) # 1/3 of the letters are private
            
            new_letter = Letter(
                title=title,
                body=full_body,
                is_private=is_priv,
                image=attached_img
            )
            db.session.add(new_letter)

        db.session.commit()
        print("Successfully seeded 5 memories and 55 beautiful letters!")

if __name__ == "__main__":
    seed_data()
