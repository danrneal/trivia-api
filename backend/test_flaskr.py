import unittest
from flaskr import app
from models import DB_DIALECT, DB_HOST, DB_PORT, setup_db



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.db_name = 'trivia_test'
        self.db_path = f'{DB_DIALECT}://{DB_HOST}:{DB_PORT}/{self.db_name}'
        setup_db(self.app, self.db_path)

    def tearDown(self):
        """Executed after reach test"""

    """
    TODO
    Write at least one test for each test for successful operation and for
    expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
