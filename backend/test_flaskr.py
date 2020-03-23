"""Test objects used to test the behavior of endpoints in the flaskr app

Classes:
    QuestionTestCase()
"""

import unittest
from flaskr import app
from models import DB_DIALECT, DB_HOST, DB_PORT, setup_db


class CategoryTestCase(unittest.TestCase):
    """This class represents the test cases for the category endpoints

    Attributes:
        app: A flask app from the flaskr app
        client: A test client for the flask app to while testing
        db_name: A str representing the name of the test database
        db_path: A str representing the location of the test database
    """

    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.db_name = 'trivia_test'
        self.db_path = f'{DB_DIALECT}://{DB_HOST}:{DB_PORT}/{self.db_name}'
        setup_db(self.app, self.db_path)

    def tearDown(self):
        """Executed after each test"""

    def test_get_categories_success(self):
        """Test successful retrieval of categories"""

        response = self.client().get('/categories')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)
        self.assertTrue(response.json.get('categories'))


class QuestionTestCase(unittest.TestCase):
    """This class represents the test cases for the question endpoints

    Attributes:
        app: A flask app from the flaskr app
        client: A test client for the flask app to while testing
        db_name: A str representing the name of the test database
        db_path: A str representing the location of the test database
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
        self.assertIsNone(response.json.get('current_category_id'))
        self.assertTrue(response.json.get('categories'))

    def test_create_question_success(self):
        """Test successful creation of question"""

        new_question = {
            'question': "What's the answer to life the universe & everything?",
            'answer': "42",
            'category_id': 1,
            'difficulty': 5,
        }

        response = self.client().post('/questions', json=new_question)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)

    def test_delete_question_success(self):
        """Test successful deletion of question"""

        response = self.client().get('/questions')
        question_id = response.json.get('questions')[0]['id']
        response = self.client().delete(f'/questions/{question_id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)
        self.assertEqual(response.json.get('deleted_question_id'), question_id)


if __name__ == "__main__":
    unittest.main()
