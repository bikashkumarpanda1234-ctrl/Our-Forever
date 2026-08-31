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
UPLOADED_IMAGES_4 = [
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103342188.png",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103348021.png",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103380473.png",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103396802.png",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103404277.jpg"
]

def seed_fourth_data():
    app = create_app()
    with app.app_context():
        # Destination folder
        dest_folder = app.config["PUBLIC_PHOTO_FOLDER"]
        os.makedirs(dest_folder, exist_ok=True)

        copied_filenames = []

        # 1. Copy images to the media folder
        print("Copying fourth set of uploaded photos...")
        for i, src_path in enumerate(UPLOADED_IMAGES_4):
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
            ("A Coziest Smile Together 🧸", "Smiling close, captured inside. You make every ordinary place feel extraordinary.", copied_filenames[0]),
            ("Auto Ride Adventures 🛺", "Riding around the city, heads resting close. Every simple journey with you is a lovely adventure.", copied_filenames[1]),
            ("Warm Embraces Indoor 🤗", "An indoor selfie of sweet comfort. Leaning back in your embrace is the safest place on earth.", copied_filenames[2]),
            ("Bright Sun and Sandy Walks 🏖️", "Another beautiful beach walk selfie, smiling under the open sky. Holding onto you always.", copied_filenames[3]),
            ("Simple Walks by the Scooter 🛵", "Standing together outside on our casual evening walks. Everyday moments made special with you.", copied_filenames[4])
        ]

        print("Seeding fourth set of memories...")
        for title, desc, img_name in memories_data:
            existing = Memory.query.filter_by(image=img_name).first()
            if not existing:
                mem = Memory(title=title, description=desc, image=img_name, is_private=False)
                db.session.add(mem)

        # 3. Update all love letters to distribute all 20 images
        print("Updating letters to attach new pictures...")
        letters = Letter.query.order_by(Letter.id.desc()).all()
        for idx, letter in enumerate(letters):
            all_images = [
                "media_1788103342188.png", "media_1788103348021.png", "media_1788103380473.png", 
                "media_1788103396802.png", "media_1788103404277.jpg",
                "media_1788103267696.jpg", "media_1788103286432.jpg", "media_1788103301475.jpg", 
                "media_1788103313042.jpg", "media_1788103325090.png",
                "media_1788102814471.png", "media_1788102819316.jpg", "media_1788102830446.jpg",
                "media_1788102847159.jpg", "media_1788102855096.png",
                "media_1788102498404.png", "media_1788102515546.png", "media_1788102533292.png",
                "media_1788102570712.png", "media_1788102601817.jpg"
            ]
            letter.image = all_images[idx % len(all_images)]

        db.session.commit()
        print("Successfully seeded 5 more memories and updated letter attachments!")

if __name__ == "__main__":
    seed_fourth_data()
