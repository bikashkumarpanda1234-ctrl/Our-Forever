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
UPLOADED_IMAGES_3 = [
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103267696.jpg",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103286432.jpg",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103301475.jpg",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103313042.jpg",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103325090.png"
]

def seed_third_data():
    app = create_app()
    with app.app_context():
        # Destination folder
        dest_folder = app.config["PUBLIC_PHOTO_FOLDER"]
        os.makedirs(dest_folder, exist_ok=True)

        copied_filenames = []

        # 1. Copy images to the media folder
        print("Copying third set of uploaded photos...")
        for i, src_path in enumerate(UPLOADED_IMAGES_3):
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
            ("A Watercolor Dream 🎨", "You look like a beautiful painting walked straight out of a dream. Gorgeous in yellow!", copied_filenames[0]),
            ("Lighting Up Our Lives 🪔", "Sitting gracefully in red, lighting diyas on the rangoli. You bring light to my world.", copied_filenames[1]),
            ("Elegance in Pink Saree 🌸", "Absolutely stunning in a traditional pink saree under the blue sky. You carry grace so effortlessly.", copied_filenames[2]),
            ("Playful Forest Selfie 🌲", "A cute, cheeky moment in the woods. Making silly faces is always better with you.", copied_filenames[3]),
            ("Double the Baby Cuteness 👶👶", "A lovely side-by-side look at childhood innocence. Precious toddler days!", copied_filenames[4])
        ]

        print("Seeding third set of memories...")
        for title, desc, img_name in memories_data:
            existing = Memory.query.filter_by(image=img_name).first()
            if not existing:
                mem = Memory(title=title, description=desc, image=img_name, is_private=False)
                db.session.add(mem)

        # 3. Update some letters with these new images
        print("Updating letters to attach new pictures...")
        letters = Letter.query.order_by(Letter.id.desc()).all()
        for idx, letter in enumerate(letters):
            # Distribute all copied images (beach set + temple set + new set = 15 images total)
            all_images = [
                "media_1788103267696.jpg", "media_1788103286432.jpg", "media_1788103301475.jpg", 
                "media_1788103313042.jpg", "media_1788103325090.png",
                "media_1788102814471.png", "media_1788102819316.jpg", "media_1788102830446.jpg",
                "media_1788102847159.jpg", "media_1788102855096.png",
                "media_1788102498404.png", "media_1788102515546.png", "media_1788102533292.png",
                "media_1788102570712.png", "media_1788102601817.jpg"
            ]
            letter.image = all_images[idx % len(all_images)]

        db.session.commit()
        print("Successfully seeded 5 new memories and updated letter attachments!")

if __name__ == "__main__":
    seed_third_data()
