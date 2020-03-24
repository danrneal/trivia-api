"""A flask-based trivia API

Users can add questions to the trivia database, view questions in the database,
and play a triva game using those questions

    Usage: flask run

Attributes:
    QUESTIONS_PER_PAGE: An int that is a global constant representing how many
        questions to show on a page
    app: A flask Flack object creating the flask app
"""

import os
import random
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from models import setup_db, Question, Category, User

QUESTIONS_PER_PAGE = 10

app = Flask(__name__)
setup_db(app)
CORS(app)


def paginate_questions(questions, page):
    """Retrieve questions for the current page only

    Args:
        questions: A list of Question objects
        page: An int representing the page number to retieive questions for

    Returns:
        A list of dicts representing questions for the given page
    """
    questions = [question.format() for question in questions]
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    current_questions = questions[start:end]

    return current_questions


@app.after_request
def after_request(response):
    """Adds response headers after request

    Args:
        response: The response object to add headers to

    Returns:
        response: The response object that the headers were added to
    """

    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type, Authorization, true'
    )
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS'
    )

    return response


@app.route('/questions', methods=['GET'])
def get_questions():
    """Route handler for endpoint showing questions for a given page

    Returns:
        response: A json object representing questions for a given page
    """

    questions = Question.query.order_by(Question.id).all()
    page = request.args.get('page', 1, type=int)
    current_questions = paginate_questions(questions, page)

    if not current_questions:
        abort(404)

    categories = Category.query.order_by(Category.id).all()
    categories = {category.id: category.name for category in categories}

    response = jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(questions),
        'current_category_id': None,
        'categories': categories,
    })

    return response


@app.route('/questions', methods=['POST'])
def create_question():
    """Route handler for endpoint to create a questoin

    Returns:
        response: A json object containing the id of the question that was
            created
    """

    try:

        search_term = request.json.get('search_term')

        if search_term is not None:

            questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')
            ).order_by(Question.id).all()
            page = request.args.get('page', 1, type=int)
            current_questions = paginate_questions(questions, page)

            categories = Category.query.order_by(Category.id).all()
            categories = {
                category.id: category.name
                for category in categories
            }

            response = jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'current_category_id': None,
                'categories': categories,
            })

        else:

            question = Question(
                question=request.json.get('question'),
                answer=request.json.get('answer'),
                category_id=request.json.get('category_id'),
                rating=request.json.get('rating'),
                difficulty=request.json.get('difficulty'),
            )

            question.insert()

            response = jsonify({
                'success': True,
                'created_question_id': question.id,
            })

    except AttributeError:
        abort(400)

    return response


@app.route('/questions/<int:question_id>', methods=['PATCH'])
def patch_question_rating(question_id):
    """Route handler for endpoint updating the rating of a single question

    Args:
        question_id: An int representing the identifier for the question to
            update the rating of

    Returns:
        response: A json object stating if the request was successful
    """

    question = Question.query.get(question_id)

    if question is None:
        abort(422)

    try:

        rating = request.json.get('rating')

        if rating:
            question.rating = int(rating)

        question.update()

    except AttributeError:
        abort(400)

    response = jsonify({
        'success': True,
        'updated_question_id': question_id,
    })

    return response


@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """Route handler for endpoint to delete a single question

    Args:
        question_id: An int representing the identifier for a question to
            delete

    Returns:
        response: A json object containing the id of the question that was
            deleted
    """

    question = Question.query.get(question_id)
    if question is None:
        abort(422)

    question.delete()

    response = jsonify({
        'success': True,
        'deleted_question_id': question_id,
    })

    return response


@app.route('/categories', methods=['GET'])
def get_categories():
    """Route handler for endpoint showing all categories

    Returns:
        response: A json object representing all categories
    """

    categories = Category.query.order_by(Category.id).all()
    categories = {category.id: category.name for category in categories}

    response = jsonify({
        'success': True,
        'categories': categories,
    })

    return response


@app.route('/categories', methods=['POST'])
def create_category():
    """Route handler for endpoint to create a category

    Returns:
        response: A json object containing the id of the category that was
            created
    """

    name = request.form.get('name')

    if name is not None:

        icon = request.files.get('icon')

        if icon is not None:

            if icon.content_type != 'image/svg+xml':
                abort(400)

            ext = os.path.splitext(icon.filename)[1]
            filename = secure_filename(name.lower() + ext)
            icon.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        category = Category(name=name)
        category.insert()
        response = jsonify({
            'success': True,
            'created_category_id': category.id,
        })
    else:
        abort(400)

    return response


@app.route('/categories/<int:category_id>/questions')
def get_category_questions(category_id):
    """Route handler for endpoint showing all questions for a specific category

    Args:
        category_id: An int representing the identifier for a category to
            retrieve questions for

    Returns:
        response: A json object representing questions for a specific category
    """

    questions = Question.query.filter(
        Question.category_id == category_id
    ).order_by(Question.id).all()
    page = request.args.get('page', 1, type=int)
    current_questions = paginate_questions(questions, page)

    if not current_questions:
        abort(404)

    categories = Category.query.order_by(Category.id).all()
    categories = {category.id: category.name for category in categories}

    response = jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(questions),
        'current_category_id': category_id,
        'categories': categories,
    })

    return response


@app.route('/quizzes', methods=['POST'])
def create_quiz():
    """Route handler for endpoint starting a new quiz

    Returns:
        response: A json object representing a random question given the
            specified parameters
    """

    try:

        quiz_category_id = request.json.get('quiz_category_id')
        previous_question_ids = request.json.get('previous_question_ids')

        questions = Question.query.filter(
            ~Question.id.in_(previous_question_ids)
        )

        if quiz_category_id != 0:
            questions = questions.filter(
                Question.category_id == quiz_category_id
            )

        questions = questions.all()

        if questions:
            question = random.choice(questions).format()
        else:
            question = None

        response = jsonify({
            'success': True,
            'question': question,
        })

    except AttributeError:
        abort(400)

    return response


@app.route('/users', methods=['GET'])
def get_users():
    """Route handler for endpoint showing all users

    Returns:
        response: A json object representing all users
    """

    users = User.query.order_by(User.id).all()
    users = {user.id: user.username for user in users}

    response = jsonify({
        'success': True,
        'users': users,
    })

    return response


@app.route('/users', methods=['POST'])
def create_user():
    """Route handler for endpoint to create a user

    Returns:
        response: A json object containing the id of the user that was created
    """

    try:

        user = User(username=request.json.get('username'))

        user.insert()

        response = jsonify({
            'success': True,
            'created_user_id': user.id,
        })

    except AttributeError:
        abort(400)

    return response


@app.errorhandler(400)
def bad_request(error):  # pylint: disable=unused-argument
    """Error handler for 400 bad request

    Args:
        error: unused

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify({
        'success': False,
        'error_code': 400,
        'message': 'Bad Request',
    })
    return response, 400


@app.errorhandler(404)
def not_found(error):  # pylint: disable=unused-argument
    """Error handler for 404 not found

    Args:
        error: unused

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify({
        'success': False,
        'error_code': 404,
        'message': 'Not Found',
    })
    return response, 404


@app.errorhandler(405)
def method_not_allowed(error):  # pylint: disable=unused-argument
    """Error handler for 405 method not allowed

    Args:
        error: unused

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify({
        'success': False,
        'error_code': 405,
        'message': 'Method Not Allowed',
    })
    return response, 405


@app.errorhandler(422)
def unprocessable_entity(error):  # pylint: disable=unused-argument
    """Error handler for 422 unprocessable entity

    Args:
        error: unused

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify({
        'success': False,
        'error_code': 422,
        'message': 'Unprocessable Entity',
    })
    return response, 422


@app.errorhandler(500)
def internal_server_error(error):  # pylint: disable=unused-argument
    """Error handler for 500 internal server error

    Args:
        error: unused

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify({
        'success': False,
        'error_code': 500,
        'message': 'Internal Server Error',
    })
    return response, 500
