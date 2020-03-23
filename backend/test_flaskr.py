"""Test objects used to test the behavior of endpoints in the flaskr app

Classes:
    QuestionTestCase()
"""

import unittest
from flaskr import app, QUESTIONS_PER_PAGE
from models import DB_DIALECT, DB_HOST, DB_PORT, setup_db, Question


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

    def test_get_questions_out_of_range_fail(self):
        """Test failed question retrieval when page number is out of range"""

        total_pages = -(-Question.query.count() // QUESTIONS_PER_PAGE)

        response = self.client().get(f'questions?page={total_pages+1}')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json.get('success'), False)
        self.assertEqual(response.json.get('message'), 'Not Found')

    def test_search_questions_success(self):
        """Test successful search of questions"""

        search = {
            'search_term': 'what',
        }

        response = self.client().post('/questions', json=search)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)
        self.assertIsNone(response.json.get('created_question_id'))
        self.assertTrue(response.json.get('questions'))
        self.assertTrue(response.json.get('total_questions'))
        self.assertIsNone(response.json.get('current_category_id'))
        self.assertTrue(response.json.get('categories'))

    def test_search_questions_no_results_success(self):
        """Test a search of questions that returned no results"""

        search = {
            'search_term': 'M155P311ED'
        }

        response = self.client().post('/questions', json=search)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)
        self.assertIsNone(response.json.get('created_question_id'))
        self.assertEqual(response.json.get('questions'), [])
        self.assertEqual(response.json.get('total_questions'), 0)
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

    def test_create_question_no_info_fail(self):
        """Test failed question creation when info is missing"""

        response = self.client().post('/questions')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json.get('success'), False)
        self.assertEqual(response.json.get('message'), 'Bad Request')

    def test_delete_question_success(self):
        """Test successful deletion of question"""

        question_id = Question.query.order_by(Question.id.desc()).first().id
        response = self.client().delete(f'/questions/{question_id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)
        self.assertEqual(response.json.get('deleted_question_id'), question_id)

    def test_delete_question_out_of_range_fail(self):
        """Test failed questions deletion when question does not exist"""

        question_id = Question.query.order_by(Question.id.desc()).first().id
        response = self.client().delete(f'/questions/{question_id+1}')

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json.get('success'), False)
        self.assertEqual(response.json.get('message'), 'Unprocessable Entity')


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

    def test_get_category_questions_success(self):
        """Test successful retrieval of questions from a category"""

        response = self.client().get('/categories/1/questions')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)
        self.assertTrue(response.json.get('questions'))
        self.assertTrue(response.json.get('total_questions'))
        self.assertEqual(response.json.get('current_category_id'), 1)
        self.assertTrue(response.json.get('categories'))

    def test_get_category_questions_out_of_range_fail(self):
        """Test failed category question retrieval when page is out of range"""

        total_pages = -(-Question.query.filter(
            Question.category_id == 1
        ).count() // QUESTIONS_PER_PAGE)

        response = self.client().get(
            f'/categories/1/questions?page={total_pages+1}'
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json.get('success'), False)
        self.assertEqual(response.json.get('message'), 'Not Found')


class QuizTestCase(unittest.TestCase):
    """This class represents the test cases for the quiz endpoints

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

    def test_create_quiz_success(self):
        """Test the successful creation of a quiz"""

        questions = Question.query.filter(Question.category_id == 1).all()
        question_ids = [question.id for question in questions]
        question_id = question_ids.pop()

        quiz = {
            'quiz_category_id': 1,
            'previous_question_ids': question_ids,
        }

        response = self.client().post('/quizzes', json=quiz)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)
        self.assertTrue(response.json.get('question'))
        self.assertEqual(response.json.get('question')['id'], question_id)

    def test_create_quiz_no_category_success(self):
        """Test the successful creation of a quiz without a category"""

        quiz = {
            'quiz_category_id': 0,
            'previous_question_ids': [],
        }

        response = self.client().post('/quizzes', json=quiz)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)
        self.assertTrue(response.json.get('question'))

    def test_create_quiz_no_question_success(self):
        """Test the successful creation of a quiz that returned no question"""

        questions = Question.query.filter(Question.category_id == 1).all()
        question_ids = [question.id for question in questions]

        quiz = {
            'quiz_category_id': 1,
            'previous_question_ids': question_ids,
        }

        response = self.client().post('/quizzes', json=quiz)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)
        self.assertIsNone(response.json.get('question'))

    def test_create_quiz_no_info_fail(self):
        """Test failed quiz creation when info is missing"""

        response = self.client().post('/quizzes')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json.get('success'), False)
        self.assertEqual(response.json.get('message'), 'Bad Request')


if __name__ == "__main__":
    unittest.main()
