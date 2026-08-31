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
UPLOADED_IMAGES_6 = [
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103476379.jpg",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103484057.jpg",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103489405.jpg",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103495928.jpg"
]

def seed_sixth_data():
    app = create_app()
    with app.app_context():
        # Destination folder
        dest_folder = app.config["PUBLIC_PHOTO_FOLDER"]
        os.makedirs(dest_folder, exist_ok=True)

        copied_filenames = []

        # 1. Copy images to the media folder
        print("Copying sixth set of uploaded photos...")
        for i, src_path in enumerate(UPLOADED_IMAGES_6):
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
            ("Joyful Ride on Scooter 🛵", "Sitting on the scooter together outside. You look beautiful in teal and a leopard scarf!", copied_filenames[0]),
            ("Holding Hands and Laughing 🌿", "Walking hand in hand through the park, sharing genuine laughs. These simple walks are my favorite.", copied_filenames[1]),
            ("Lazy Cozy Sunday Rest 😴", "Lying down side-by-side, sharing a quiet, comfortable moment of pure warmth and rest.", copied_filenames[2]),
            ("Walk on the Forest Path 🌲", "Taking a trail walk together under the green trees. Every road is beautiful when walked with you.", copied_filenames[3])
        ]

        print("Seeding sixth set of memories...")
        for title, desc, img_name in memories_data:
            existing = Memory.query.filter_by(image=img_name).first()
            if not existing:
                mem = Memory(title=title, description=desc, image=img_name, is_private=False)
                db.session.add(mem)

        # 3. Update all love letters to distribute all 29 images
        print("Updating letters to attach new pictures...")
        letters = Letter.query.order_by(Letter.id.desc()).all()
        for idx, letter in enumerate(letters):
            all_images = [
                "media_1788103476379.jpg", "media_1788103484057.jpg", "media_1788103489405.jpg", "media_1788103495928.jpg",
                "media_1788103422360.png", "media_1788103430198.jpg", "media_1788103441044.jpg", 
                "media_1788103453176.jpg", "media_1788103460988.jpg",
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
        print("Successfully seeded 4 final memories and updated letter attachments!")

if __name__ == "__main__":
    seed_sixth_data()
