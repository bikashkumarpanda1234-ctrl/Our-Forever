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
UPLOADED_IMAGES_5 = [
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103422360.png",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103430198.jpg",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103441044.jpg",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103453176.jpg",
    "C:/Users/bikas/.gemini/antigravity/brain/3b650a95-fa62-4cfd-b697-42c28dbd0b01/.user_uploaded/media_1788103460988.jpg"
]

def seed_fifth_data():
    app = create_app()
    with app.app_context():
        # Destination folder
        dest_folder = app.config["PUBLIC_PHOTO_FOLDER"]
        os.makedirs(dest_folder, exist_ok=True)

        copied_filenames = []

        # 1. Copy images to the media folder
        print("Copying fifth set of uploaded photos...")
        for i, src_path in enumerate(UPLOADED_IMAGES_5):
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
            ("Lovely Dinner Date 🍽️", "Sitting at the table with you, chatting and sharing sweet laughs over a cozy dinner date.", copied_filenames[0]),
            ("Walking the Old Streets 🏛️", "A close selfie from our exploration. The ancient background fades when I look at your face.", copied_filenames[1]),
            ("Standing Hand in Hand 🤝", "Barefoot and happy, standing together in front of the white shrine steps. Peaceful moments.", copied_filenames[2]),
            ("Sitting on the Temple Steps ⛩️", "Taking a break on the steps, making silly pout faces. The best laughs are always yours.", copied_filenames[3]),
            ("Cozy Mirror Peace Selfie ✌️", "A cute mirror selfie. Two hearts, one reflection, peace signs, and endless comfort together.", copied_filenames[4])
        ]

        print("Seeding fifth set of memories...")
        for title, desc, img_name in memories_data:
            existing = Memory.query.filter_by(image=img_name).first()
            if not existing:
                mem = Memory(title=title, description=desc, image=img_name, is_private=False)
                db.session.add(mem)

        # 3. Update all love letters to distribute all 25 images
        print("Updating letters to attach new pictures...")
        letters = Letter.query.order_by(Letter.id.desc()).all()
        for idx, letter in enumerate(letters):
            all_images = [
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
        print("Successfully seeded 5 final memories and updated letter attachments!")

if __name__ == "__main__":
    seed_fifth_data()
