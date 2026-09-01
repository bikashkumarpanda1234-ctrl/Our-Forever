import unittest
from app import app
from flask import session
from models import db
from models.music import Music

class PrivateIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

        # Seed a test private track
        with self.app.app_context():
            # Clean up first
            Music.query.filter_by(file='test_private_song.mp3').delete()
            db.session.commit()

            self.test_track = Music(
                title='Test Private Song',
                artist='Test Artist',
                file='test_private_song.mp3',
                cover='test_cover.jpg',
                is_private=True
            )
            db.session.add(self.test_track)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            Music.query.filter_by(file='test_private_song.mp3').delete()
            db.session.commit()

    def test_music_add_redirects_to_auth_login(self):
        # Accessing /music/add should redirect to /auth/login with next parameter
        response = self.client.get('/music/add', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth/login', response.headers['Location'])
        self.assertIn('next=', response.headers['Location'])

    def test_unlock_sets_private_unlocked_session(self):
        # Posting correct password to /private/ should unlock secret gallery without auto-logging in as admin
        with self.client:
            password = self.app.config.get('PRIVATE_PASSWORD', 'PoonamBikash@123')
            response = self.client.post('/private/', data={
                'password': password,
                'next': '/private/dashboard'
            }, follow_redirects=False)
            
            # Check redirect
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.headers['Location'], '/private/dashboard')
            
            # Check session values: private_unlocked MUST be True, logged_in MUST NOT be True
            self.assertTrue(session.get('private_unlocked'))
            self.assertFalse(session.get('logged_in'))

    def test_locked_private_music_redirects_to_unlock(self):
        # Accessing private song when locked redirects to /private/
        response = self.client.get('/media/music/test_private_song.mp3', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/private/', response.headers['Location'])

    def test_unlocked_private_music_allows_access(self):
        # Accessing private song when unlocked does not redirect
        with self.client:
            password = self.app.config.get('PRIVATE_PASSWORD', 'PoonamBikash@123')
            self.client.post('/private/', data={'password': password}, follow_redirects=False)
            
            # Access song (should result in 404 because file is not on disk, but NOT a 302 redirect)
            response = self.client.get('/media/music/test_private_song.mp3', follow_redirects=False)
            self.assertNotEqual(response.status_code, 302)
