import os
from flask import Flask, request as req, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Pagination helper function
def paginate_questions(req, selection):
    page = req.args.get(
            'page',
            1,
            type = int
        )
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS & Allow all(*) for origins.
    CORS(app, resources={'/': {'origins': '*'}})

    # Setting up allowed Headers & Methods
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS'
        )
        return response

    # Categories GET method route
    @app.route('/categories')
    def get_categories():
        cats = Category.query.all()
        cats_dict = {cat.id: cat.type for cat in cats}

        if len(cats_dict) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': cats_dict
        })

    # Questions GET method route
    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(req, selection)

        cats = Category.query.all()
        cats_dict = {cat.id: cat.type for cat in cats}

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'categories': cats_dict,
            'current_category': None
        })

    # DELETE question by id
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            if question:
                question.delete()
                return jsonify({
                    'success': True,
                    'deleted': question_id
                })
            else:
                abort(404)
        except:
            abort(422)

    # Handle searching / posting new question & add it to db
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = req.get_json()
        # Check if search query
        if body.get('searchTerm'):
            search_term = body.get('searchTerm')
            search_exp = Question.question.ilike(f"%{search_term}%")
            selection = Question.query.filter(search_exp).all()

            if len(selection) == 0:
                abort(404)
            current_questions = paginate_questions(req, selection)
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'current_category': None
            })

        # If not search, add new question
        else:
            question = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category', None)

            try:
                question = Question(
                    question = question,
                    answer = answer,
                    category = category,
                    difficulty = difficulty
                )
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(req, selection)

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': current_questions,
                    'total_questions': len(selection)
                })
            except:
                abort(422)

    # GET questions based on category
    @app.route('/categories/<int:cat_id>/questions')
    def get_category_questions(cat_id):
        category = Category.query.filter_by(id=cat_id).one_or_none()

        # Check if category exist
        if category is None:
            abort(400)
        selection = Question.query.filter_by(category=category.id).all()
        current_questions = paginate_questions(req, selection)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': category.type
        })

    # Play the quiz
    @app.route('/quizzes', methods=['POST'])
    def random_question():
        body = req.get_json()
        category = body.get('quiz_category')
        previous = body.get('previous_questions')

        # Generate random question
        def random_question():
            return questions[random.randrange(0, len(questions), 1)]

        # Check if question already answered
        def answered_question(question):
            answered = False
            for q in previous:
                if(q == question.id):
                    answered = True

            return answered

        # Check if category or previous exist
        if category is None or previous is None:
            abort(400)

        # Check if category is selected
        if category['id'] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=category['id']).all()
        total_questions = len(questions)
        question = random_question()
        # Check if generated question already answered
        while answered_question(question):
            # Generate new question
            question = random_question()
            # If all question answered, no questions to return
            if len(previous) == total_questions:
                return jsonify({
                    'success': True
                })
        return jsonify({
            'success': True,
            'question': question.format()
        })

    # Custom json error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable'
        }), 422

    return app
