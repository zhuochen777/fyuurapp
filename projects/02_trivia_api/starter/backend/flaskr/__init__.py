import os
from xml.dom.pulldom import ErrorHandler
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [item.format() for item in selection]
  current_questions = questions[start:end]

  return current_questions



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # CORS(app)
  cors = CORS(app, resources={r'/api/*': {'origin': '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow_Methods', 'GET, PACTH, POST, DELETE, OPTIONS')
    return response

  '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    selection = Category.query.order_by(Category.id).all()
    current_categories = paginate_questions(request, selection)

    if len(current_categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': {cat.id: cat.type for cat in selection}
    })


  '''
  @TODO:
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
  def get_paginated_questions():
    questions = Question.query.all()
    categories = Category.query.all()

    current_questions = paginate_questions(request, questions)
    formatted_categories = [item.format() for item in categories]

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(questions),
      'current_category': None,
      'categories': formatted_categories
    })


  '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      delete_question = Question.query.filter(Question.id == question_id).one_or_none()

      if not delete_question:
        abort(404)

      delete_question.delete()

      questions = Question.query.all()
      current_questions = paginate_questions(request, questions)

      return jsonify({
        'success': True,
        'delete_question_id': question_id,
        'current_questions': current_questions,
        'total_num_questions': len(questions)
      })
    except:
      abort(422)

  '''
  @TODO:
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

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
    searchTerm = body.get('searchTerm', None)

    try:
      if searchTerm:
        search_questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
        current_questions = paginate_questions(request, search_questions)

        questions = Question.query.all()

        return jsonify({
          'success': True,
          'current_category': None,
          'questions': current_questions,
          'total_questions': len(questions)
        })

      else:
        question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
        question.insert()

        questions = Question.query.all()
        current_questions = paginate_questions(request, questions)

        return jsonify({
          'success': True,
          'current_category': question.category,
          'questions': current_questions,
          'total_questions': len(questions)
        })

    except:
      abort(405)
  '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''


  '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_basedOn_category(category_id):
    filtered_questions = Question.query.filter(Question.category == category_id).all()

    if len(filtered_questions) == 0:
      abort(404)

    questions = paginate_questions(request, filtered_questions)

    total_questions = Question.query.all()

    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(total_questions),
      'current_category': category_id
    })

  '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
    body = request.get_json()

    try:
      previous_questions = body.get('previous_questions', None)
      quiz_category = body.get('quiz_category', None)
      quiz_category_id = quiz_category['id']

      if previous_questions is None:
        if quiz_category_id is None:
          questions = Question.query.all()
        else:
          questions = Question.query.filter(Question.category == quiz_category_id).all()
      else:
        if quiz_category_id is None:
          questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
        else:
          questions = Question.query.filter(Question.category == quiz_category_id, Question.id.notin_(previous_questions)).all()

      question = random.choice(questions).format()

      return jsonify({
        'success': True,
        'question': question
      })
    except:
      abort(422)

  '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'error': 404,
      'success': False,
      'message': 'resource not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'error': 422,
      'success': False,
      'message': 'unprocessable'
    }), 422

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      'error': 405,
      'success': False,
      'message': 'method not allowed'
    }), 405

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      'error': 500,
      'success': False,
      'message': 'internal server error'
    }), 500

  return app
