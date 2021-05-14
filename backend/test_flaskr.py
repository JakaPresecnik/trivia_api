import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from sqlalchemy_utils import database_exists, create_database

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        # added a variable that is used to switch between initializing a database
        self.initialized = False
        self.user = "postgres"
        self.password = 'piko'
        self.database_server = 'localhost:5432'
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.user, self.password, self.database_server, self.database_name)
        engine = create_engine(self.database_path)
        # added a line that creates a database if it is none existant
        if not database_exists(engine.url):
            create_database(engine.url)
            self.initialized = True

        setup_db(self.app, self.database_path)
        # some variables to use for testing
        self.test_category = Category(type= 'Science')
        self.test_question = Question(question='Test question?', answer='Yes', difficulty=5,category=1)
        self.new_question = {
            'question': 'New question?',
            'answer': 'Yes',
            'difficulty': 5,
            'category': 1
        }
        self.new_search = {'searchTerm': 'question'}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables and add some data to the tables
            if self.initialized:
                self.db.create_all()
                self.db.session.add(self.test_category)
                self.db.session.add(self.test_question)
                self.db.session.commit()
                self.initialized = False
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # get_categories() test
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    # get_questions() test
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'] > 0)
        self.assertEqual(data['current_category'], 0)

    # create_question() test
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # delete_question(question_id) test
    # def test_delete_question(self):
    #     res = self.client().delete('/questions/2')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['question_id'], 2)
    
    # search_question() test
    def test_search_question(self):
        res = self.client().post('/questions/search', json=self.new_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'] > 0)

    # category_questions(category_id) test
    def test_get_category_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'] > 0)

    # get_quizzes() test
    # internal_server_error(error) test
    # not_found(error) test
    # unprocassable(error) test
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()