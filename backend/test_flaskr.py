import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_user = "postgres"
        self.database_pass = "postgres"
        self.database_path = "postgresql://{}:{}@{}/{}".\
            format(self.database_user, self.database_pass,\
                'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test valid GET /categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    # Test valid GET /questions
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    # Test if page is out of reach
    def test_outofreach_questions_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Test deleting question by id
    def test_delete_question(self):
        # Creating test question
        question = Question(
            question = 'Test Question',
            answer = 'The Answer',
            category = 3,
            difficulty = 1
        )
        question.insert()
        id = question.id

        # Delete the question
        res = self.client().delete(f'/questions/{id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id)

    # Test deleting non existing question
    def test_delete_non_exist_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # Test adding new question
    def test_post_question(self):
        # Creating test question
        question = {
            'question' : 'Test Question',
            'answer' : 'The Answer',
            'category' : 3,
            'difficulty' : 1
        }

        #Totals
        total_before = len(Question.query.all())
        res = self.client().post('/questions', json = question)
        data = json.loads(res.data)
        total_after = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(total_after, total_before+1)

    # Test unprocessable post question
    def test_unprocessable_post_question(self):
        # Creating test question
        question = {
            'question' : 'Test Question',
            'answer' : 'The Answer',
            'category': 1000
        }

        res = self.client().post('/questions', json = question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # Test performing search query
    def test_search_query(self):
        query = {'searchTerm': 'world'}
        res = self.client().post('/questions', json = query)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    # Test search term which isn't found
    def test_wrong_search_query(self):
        query = {'searchTerm': 'Don\'t Exist'}
        res = self.client().post('/questions', json = query)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Test getting category questions
    def test_category_questions(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    # Test if no category is sent
    def test_no_category_questions(self):
        res = self.client().get('/categories/3000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # Test quiz game
    def test_quiz_game(self):
        previous = {
            'previous_questions' : [],
            'quiz_category': {
                'type': 'Art',
                'id': 2
            }
        }
        res = self.client().post('/quizzes', json = previous)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    # Test if quiz category is None
    def test_null_quiz_category(self):
        previous = {
            'previous_questions' : []
        }
        res = self.client().post('/quizzes', json = previous)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
