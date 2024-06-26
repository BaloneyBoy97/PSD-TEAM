# python -m unittest discover -s tests -p "integration_test_email.py" 
import unittest
import os
import json
import sqlite3
from flask_testing import TestCase
from environment.app import app
import authentication.operation as auth_ops
from werkzeug.security import generate_password_hash
import time

class EmailIntegrationTest(TestCase):
    def create_app(self):
        """
        Setting up testing environment with Flask
        """
        app.config['TESTING'] = True
        app.config['MAIL_SUPPRESS_SEND'] = False  # Enable sending emails
        app.config['DATABASE'] = 'test_appdata.db'
        app.config['JWT_SECRET_KEY'] = '4e19f3de1b8c3d2abe69c857f724f3ba02bde9bb35688d6215043531a2765514'
        return app
    
    def setUp(self):
        """
        Setting test database and database path configuration
        removing existing database from testing environment
        ensure test isolation and prevent database locking
        """
        self.test_database = app.config['DATABASE']
        auth_ops.set_database_path(self.test_database)
        
        if os.path.exists(self.test_database):
            os.remove(self.test_database)
        
        """
        Mimicking appdata.db create identical db setup
        insert mock data into db for unit test
        """
        conn = sqlite3.connect(self.test_database)
        curr = conn.cursor()

        curr.executescript("""
            CREATE TABLE IF NOT EXISTS userdata(
                userid INTEGER PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                isAdmin BOOLEAN NOT NULL DEFAULT 0
            );
        """)

        hashed_password1 = generate_password_hash('password1', method='pbkdf2:sha256', salt_length=16)
        hashed_password2 = generate_password_hash('password2', method='pbkdf2:sha256', salt_length=16)

        try:
            curr.executemany("INSERT OR IGNORE INTO userdata (userid, email, username, password) VALUES (?, ?, ?, ?)", [
                (1, 'user1@unittest.com', 'user1', hashed_password1),
                (2, 'user2@unittest.com', 'user2', hashed_password2)
            ])
        except sqlite3.IntegrityError:
            pass

        conn.commit()
        conn.close()

        """
        Give 5 retries attempts to log in test user
        use to detect database locking issue
        """
        retries = 5
        for _ in range(retries):
            try:
                login_response = self.client.post('/auth/login', data=json.dumps({
                    'email': 'user1@unittest.com',
                    'password': 'password1'
                }), content_type='application/json')

                self.assertEqual(login_response.status_code, 200, "Login failed during setup")
                self.token = json.loads(login_response.data)['access_token']
                break
            except sqlite3.OperationalError:
                time.sleep(1)
        else:
            self.fail("Database locking issue detected")
    
    def tearDown(self):
        """
        remove test database after unit test
        """
        if os.path.exists(self.test_database):
            os.remove(self.test_database)

    def test_user_registration_email(self):
        """
        Test that a registration email is sent upon successful user registration
        """
        response = self.client.post('/auth/register', data=json.dumps({
            'email': 'zanxiang.wang@outlook.com',
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'User registered successfully!')

if __name__ == '__main__':
    unittest.main()