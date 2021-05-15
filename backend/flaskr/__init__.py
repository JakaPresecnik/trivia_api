import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  # helper function that takes the arguments of questions, categories and page,
  # it formats them and limits the respond to QUESTIONS_PER_PAGE 
  def paginate_questions(req, categories, questions):
    page = req.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_categories = {}
    for category in categories:
      c = category.format()
      formatted_categories[c['id']] = c['type']

    formatted_questions = [question.format() for question in questions]

    return {
      'paginated_questions': formatted_questions[start:end],
    	'paginated_categories': formatted_categories,
      'length': len(formatted_questions)
    }

  '''
  DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(res):
    res.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    res.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
    
    return res

  '''
  DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = {}
    for category in categories:
      formatted_category = category.format()
      formatted_categories[formatted_category['id']] = formatted_category['type']

    return jsonify({
      "success": True,
      "categories": formatted_categories
    }), 200

  # Added additional route that lets us create additional categories
  # It is not implemented in frontend as I want the commit to have more python than js :D
  @app.route('/categories', methods=['POST'])
  def create_category():
    body = request.get_json()
    categories = Category.query.with_entities(Category.type).all()
    categories_array = [type for (type, ) in categories]
    
    if not body:
      abort(422)

    new_category = body.get('category', None)

    if new_category in categories_array:
      abort(409)

    if new_category is None:
      abort(422)

    try:
      category = Category(type = new_category)
    
      category.insert()
      return jsonify({
        "success": True,
        "category": new_category
      }), 200
    except:
      abort(422)

  '''
  DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions', methods=['GET'])
  def get_questions():
    categories = Category.query.order_by(Category.id).all()
    questions = Question.query.order_by(Question.id).all()
    # It uses the helper function paginate_questions
    paginated_results = paginate_questions(request, categories, questions)
    
    if len(paginated_results['paginated_questions']) == 0:
      abort(404)

    return jsonify({
      "success": True,
      "questions": paginated_results['paginated_questions'],
      "total_questions": paginated_results['length'],
      "categories": paginated_results['paginated_categories'],
      "current_category": 0
    }), 200

  '''
  DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      
      return jsonify({
        "success": True,
        "question_id": question_id
      }), 200
    except:
      abort(422)

  '''
  DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    if not body:
      abort(422)
    # error handling on empty inputs
    new_question = body.get('question', None)
    if not new_question:
      abort(422)
    new_answer = body.get('answer', None)
    if not new_answer:
      abort(422)
    new_difficulty = body.get('difficulty', None)
    if not new_difficulty:
       abort(422)
    new_category = body.get('category', None)
    if not new_category:
      abort(422)
    
    try:
      question = Question(
        question=new_question, 
        answer=new_answer, 
        difficulty=new_difficulty, 
        category=new_category)
      question.insert()

      return jsonify({'success': True})
    except:
      abort(422)
    
  '''
  DONE: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_question():
    body = request.get_json()
    search_term = body.get('searchTerm', None)

    try:
      questions = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
      
      if not questions:
        abort(422)

      formatted_questions = [question.format() for question in questions]
     
      return jsonify({
        "success": True,
        "questions": formatted_questions,
        "total_questions": len(formatted_questions)
      }), 200
    except:
      abort(422)

  '''
  DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  # changed to string as the test fails when integer
  @app.route('/categories/<string:category_id>/questions', methods=['GET'])
  def category_questions(category_id):
    category = Category.query.filter(Category.id == category_id).first()

    if not category:
      abort(404)

    questions = Question.query.filter(Question.category == category_id).all()
      
    formatted_questions = [question.format() for question in questions]
    formatted_category = category.format()

    return jsonify({
      "success": True,
      "questions": formatted_questions,
      "total_questions": len(formatted_questions),
      "current_category": formatted_category['type']
    })

  '''
  DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quizzes():
    body = request.get_json()
    category = body['quiz_category']
    previous_questions = body['previous_questions']
    
    # If/else to set the questions for desired category 
    # or all categories, that are unanswered
    if category['id'] == 0:
      questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
    else:
      questions = Question.query.filter(
        Question.category == category['id'], 
        Question.id.notin_(previous_questions)).all()
    
    # If there are no more unanswerd questions send this
    if len(questions) == 0:
      return jsonify({
        "status": "no more questions"
      })

    # Randomize the question
    random_question = random.choice(questions).format()
    
    return jsonify({
      "success": True,
      "question": random_question
    }), 200

  '''
  DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "Internal Server Error"
    }), 500
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Not found"
    }), 404

  @app.errorhandler(422)
  def unprocassable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "Unprocessable"
    }), 422

  @app.errorhandler(409)
  def unprocassable(error):
    return jsonify({
      "success": False, 
      "error": 409,
      "message": "Already exists"
    }), 409


  return app

    