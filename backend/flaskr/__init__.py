import os
import random
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Question, Category

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
        'Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS'
    )

    return response


@app.route('/categories')
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


@app.route('/questions')
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


'''
@TODO:
Create an endpoint to POST a new question,
which will require the question and answer text,
category, and difficulty score.

TEST: When you submit a question on the "Add" tab,
the form will clear and the question will appear at the end of the last
page of the questions list in the "List" tab.
'''

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

'''
@TODO:
Create error handlers for all expected errors
including 404 and 422.
'''
