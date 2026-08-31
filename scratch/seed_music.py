import os
import sys

# Add project directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db
from models.music import Music

HINDI_ROMANTIC_SONGS = [
    ("Tum Se Hi 🌸", "Pritam / Mohit Chauhan (Jab We Met)"),
    ("Kesariya 🌼", "Arijit Singh (Brahmastra)"),
    ("Apna Bana Le 💖", "Arijit Singh / Sachin-Jigar (Bhediya)"),
    ("Tum Hi Ho 🌹", "Arijit Singh (Aashiqui 2)"),
    ("Zara Zara 🍂", "Bombay Jayashri (Rehnaa Hai Terre Dil Mein)"),
    ("Raataan Lambiyan 🌌", "Jubin Nautiyal / Asees Kaur (Shershaah)"),
    ("Pehla Nasha 🍃", "Udit Narayan / Sadhana Sargam (Jo Jeeta Wohi Sikandar)"),
    ("Tujh Mein Rab Dikhta Hai ✨", "Roop Kumar Rathod (Rab Ne Bana Di Jodi)"),
    ("Tere Hawaale 🌻", "Arijit Singh / Shilpa Rao (Laal Singh Chaddha)"),
    ("Apna Bana Le 🍁", "Arijit Singh (Bhediya)"),
    ("O Maahi 🌟", "Arijit Singh (Dunki)"),
    ("Heeriye 💕", "Jasleen Royal / Arijit Singh"),
    ("Satranga 🌈", "Arijit Singh (Animal)"),
    ("Pehle Bhi Main 🌊", "Vishal Mishra (Animal)"),
    ("O Bedardeya 💔", "Arijit Singh (Tu Jhoothi Main Makkaar)"),
    ("Dil Diyan Gallan ❄️", "Atif Aslam (Tiger Zinda Hai)"),
    ("Kaise Hua 🔥", "Vishal Mishra (Kabir Singh)"),
    ("Tera Ban Jaunga 💞", "Akhil Sachdeva / Tulsi Kumar (Kabir Singh)"),
    ("Ve Maahi 🌾", "Arijit Singh / Asees Kaur (Kesari)"),
    ("Janam Janam 💫", "Arijit Singh / Antara Mitra (Dilwale)"),
    ("Samjhawan 🎈", "Arijit Singh / Shreya Ghoshal (Humpty Sharma Ki Dulhania)"),
    ("Sun Saathiya 🩰", "Priya Saraiya / Divya Kumar (ABCD 2)"),
    ("Zehnaseeb 🎀", "Chinmayi Sripada / Shekhar Ravjiani (Hasee Toh Phasee)"),
    ("Mast Magan 🕯️", "Arijit Singh (2 States)"),
    ("Saibo 🌸", "Shreya Ghoshal / Tochi Raina (Shor in the City)"),
    ("Raabta 🛸", "Arijit Singh / Hamsika Iyer (Agent Vinod)"),
    ("Dil Ko Karaar Aaya 🥰", "Yasser Desai / Neha Kakkar"),
    ("Baarish Ban Jaana 🌧️", "Stebin Ben / Payal Dev"),
    ("Thoda Thoda Pyaar ❤️", "Stebin Ben"),
    ("Lut Gaye 🥀", "Jubin Nautiyal"),
    ("Tum Hi Aana 🚪", "Jubin Nautiyal (Marjaavaan)"),
    ("Pal ⏳", "Arijit Singh / Shreya Ghoshal (Jalebi)"),
    ("Hale Dil 💔", "Harshit Saxena (Murder 2)"),
    ("Phir Mohabbat 🖤", "Mohit Chauhan / Arijit Singh (Murder 2)"),
    ("Dil Kyun Yeh Mera 🎈", "KK (Kites)"),
    ("Zindagi Do Pal Ki ⏳", "KK (Kites)"),
    ("Khuda Jaane 🕊️", "KK / Shilpa Rao (Bachna Ae Haseeno)"),
    ("Ahista Ahista 🚶‍♂️", "Arijit Singh (Laila Majnu)"),
    ("O Meri Laila 🏔️", "Atif Aslam / Jyotica Tangri (Laila Majnu)"),
    ("Nazm Nazm ✍️", "Arko (Bareilly Ki Barfi)"),
    ("Humsafar 🛶", "Akhil Sachdeva (Badrinath Ki Dulhania)"),
    ("Kinna Sona 🦁", "Jubin Nautiyal (Marjaavaan)"),
    ("Tera Fikr 💭", "Darshan Raval"),
    ("Asal Mein 🥺", "Darshan Raval"),
    ("Tum Se 💍", "Raghav Chaitanya / Varun Jain (Teri Baaton Mein Aisa Uljha Jiya)"),
    ("Chura Liya Hai Tumne 🎸", "Asha Bhosle / Mohammed Rafi (Yaadon Ki Baaraat)"),
    ("Kabira 🌾", "Tochi Raina / Rekha Bhardwaj (Yeh Jawaani Hai Deewani)"),
    ("Ban Ja Rani 👑", "Guru Randhawa (Tumhari Sulu)"),
    ("Dhadak Title Track 💓", "Ajay Gogavale / Shreya Ghoshal (Dhadak)"),
    ("Bolna 🗣️", "Arijit Singh / Asees Kaur (Kapoor & Sons)"),
    ("Ishq Wala Love 💘", "Shekhar Ravjiani / Salim Merchant (Student of the Year)"),
    ("Mere Bina 🚪", "Nikhil D'Souza (Crook)"),
    ("Dil Ibaadat 🕯️", "KK (Tum Mile)")
]

def seed_music():
    app = create_app()
    with app.app_context():
        # Clear existing seeded Hindi romantic songs to avoid duplicates
        existing_titles = [s[0] for s in HINDI_ROMANTIC_SONGS]
        Music.query.filter(Music.title.in_(existing_titles)).delete()
        db.session.commit()

        print("Seeding 50+ Hindi romantic songs...")
        for i, (title, artist) in enumerate(HINDI_ROMANTIC_SONGS):
            # Alternate private and public
            is_priv = (i % 4 == 0) # 1/4 of the tracks are private
            
            # The default song on disk is 'tum_se_hi.mp3'
            new_track = Music(
                title=title,
                artist=artist,
                file="tum_se_hi.mp3",
                cover=None,
                is_private=is_priv,
                is_background=False
            )
            db.session.add(new_track)
        
        db.session.commit()
        print(f"Successfully seeded {len(HINDI_ROMANTIC_SONGS)} Hindi romantic love songs!")

if __name__ == "__main__":
    seed_music()
