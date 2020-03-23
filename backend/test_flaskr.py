"""Test objects used to test the behavior of endpoints in the flaskr app

Classes:
    QuestionTestCase()
"""

import unittest
from flaskr import app
from models import DB_DIALECT, DB_HOST, DB_PORT, setup_db


class QuestionTestCase(unittest.TestCase):
    """This class represents the test cases for the question endpoints

    Attributes:
        app: A flask app from the flaskr app
        client: A test client for the flask app to while testing
        db_name: A str representing the name of the test database
        db_path: A str representing the location of the test database
        new_book: A dict representing a new book to use in tests
    """

    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.db_name = 'trivia_test'
        self.db_path = f'{DB_DIALECT}://{DB_HOST}:{DB_PORT}/{self.db_name}'
        setup_db(self.app, self.db_path)

    def tearDown(self):
        """Executed after each test"""

    def test_get_questions_success(self):
        """Test successful retrieval of questions"""

        response = self.client().get('/questions')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)
        self.assertTrue(response.json.get('questions'))
        self.assertTrue(response.json.get('total_questions'))
        self.assertTrue(response.json.get('categories'))


if __name__ == "__main__":
    unittest.main()
