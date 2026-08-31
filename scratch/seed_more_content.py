import os
import sys
import shutil

# Add project directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db
from models.memory import Memory

# Paths of uploaded images
UPLOADED_IMAGES_2 = [
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788102814471.png",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788102819316.jpg",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788102830446.jpg",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788102847159.jpg",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788102855096.png"
]

def seed_more_data():
    app = create_app()
    with app.app_context():
        # Destination folder
        dest_folder = app.config["PUBLIC_PHOTO_FOLDER"]
        os.makedirs(dest_folder, exist_ok=True)

        copied_filenames = []

        # 1. Copy images to the media folder
        print("Copying more uploaded photos...")
        for i, src_path in enumerate(UPLOADED_IMAGES_2):
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
            ("Divine Moments at Ram Mandir 🛕", "Sitting on the temple steps with you, feeling blessed and peaceful in your presence.", copied_filenames[0]),
            ("Stunning in Lehenga at the Fest 🌌", "You looked absolutely breathtaking in your dark blue attire. My eyes were locked on you the whole evening.", copied_filenames[1]),
            ("Serene Smile in the Park 🌿", "A quiet afternoon spent amidst the greenery. Your gentle pose and sweet smile make my heart melt.", copied_filenames[2]),
            ("Happy Birthday My Star 🎂", "Celebrating your special day under the fairy lights. You are indeed better than you think you are, my love!", copied_filenames[3]),
            ("A Precious Little Baby Photo 👶", "Look at this cute little baby! Even back then, you were destined to bring so much joy into my life.", copied_filenames[4])
        ]

        print("Seeding more memories...")
        for title, desc, img_name in memories_data:
            # Check if memory already exists
            existing = Memory.query.filter_by(image=img_name).first()
            if not existing:
                mem = Memory(title=title, description=desc, image=img_name, is_private=False)
                db.session.add(mem)

        db.session.commit()
        print("Successfully seeded 5 additional memories!")

if __name__ == "__main__":
    seed_more_data()
