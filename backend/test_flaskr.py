import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

# change this variable on each test
delete_question_id = 4
delete_category_id = 2
create_category_name = 'testing1'

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_USER = os.getenv('DB_USER')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            self.DB_USER, 
            self.DB_PASSWORD, 
            'localhost:5432', 
            self.database_name)
        setup_db(self.app, self.database_path)
        
        """ variables used in testing routes 
            If the database is meddled with tests can fail!
            NOTE: if you run multiple tests you need to update variables on top""" 

        self.new_category = {'category': create_category_name}
        self.science_category = {'category': 'Science'}
        self.new_question = {
            'question': 'New question?',
            'answer': 'Yes',
            'difficulty': 5,
            'category': 1
        }
        self.new_search = {'searchTerm': 'question'}
        self.question_to_update = 1
        self.updated_question = {
            'question': 'Updated question?',
            'answer': 'Yes',
            'difficulty': 5,
            'category': 1
        }
        self.unexistent_question_search = {'searchTerm': 'hdkerefdsgsd'}
        self.test_previous_questions = ['16', '17', '18']
        self.test_quiz_category = {'type': 'Art', 'id': '2'}
        self.test_unanswered_question_id = 19

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

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
    
    # create_category() tests
    def test_create_category(self):
        res = self.client().post('/categories', json=self.new_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['category'], self.new_category['category'])

    def test_409_category_already_exists(self):
        res = self.client().post('/categories', json=self.science_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Already exists')
    
    def test_422_test_new_category_none(self):
        res = self.client().post('/categories', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # delete_category() tests
    def test_delete_question(self):
        res = self.client().delete('/category/' + str(delete_category_id))
        data = json.loads(res.data)

        category = Category.query.filter(
            Category.id == delete_category_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['category_id'], delete_category_id)
        self.assertEqual(category, None)

    def test_404_category_does_not_exist(self):
        res = self.client().delete('category/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    # get_questions() tests:
    # receive questions success
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'] > 0)
        self.assertEqual(data['current_category'], 0)

    # receive empty object
    def test_404_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    # create_question() tests
    # create question success
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    # posting empty object
    def test_422_creating_new_questions_without_values(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # delete_question(question_id) tests
    # delete success
    def test_delete_question(self):
        res = self.client().delete('/questions/' + str(delete_question_id))
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.id == delete_question_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question_id'], delete_question_id)
        self.assertEqual(question, None)
    # question to delete doesn't exist
    def test_404_question_does_not_exist(self):
        res = self.client().delete('question/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    # update_question(question_id) test
    # testing update
    def test_update_question(self):
        res = self.client().put('/questions/2', json=self.updated_question)
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 2).one_or_none()
        

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question.format()['question'], self.updated_question['question'])
        self.assertEqual(question.format()['answer'], self.updated_question['answer'])
        self.assertEqual(question.format()['difficulty'], self.updated_question['difficulty'])
        self.assertEqual(question.format()['category'], self.updated_question['category'])
    
    def test_400_question_does_not_exist(self):
        res = self.client().put('/questions/1000', json=self.updated_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    # search_question() test
    # search success
    def test_search_question(self):
        res = self.client().post('/questions/search', json=self.new_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'] > 0)
    # search error
    def test_422_search_question_invalid(self):
        res = self.client().post('/questions/search', 
            json=self.unexistent_question_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # category_questions(category_id) test
    def test_get_category_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'] > 0)
    # error not valid category
    def test_404_category_not_found(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')


    # get_quizzes() test
    # get the quiz that wasn't answered yet 
    def test_get_quizzes(self):
        res = self.client().post('/quizzes', json={
            "quiz_category": self.test_quiz_category, 
            "previous_questions": self.test_previous_questions
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['id'], self.test_unanswered_question_id)

    def test_get_quizzes_no_more_questions(self):
        self.test_previous_questions.append(self.test_unanswered_question_id)
        res = self.client().post('/quizzes', json={
            "quiz_category":self.test_quiz_category, 
            "previous_questions": self.test_previous_questions
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'no more questions')
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()