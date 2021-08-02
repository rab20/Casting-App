import os
from flask import Flask, request, abort, jsonify
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.session import Session
from flask_cors import CORS
import json
from auth.auth import AuthError, requires_auth
from database.models import setup_db, Assignments, Actors, Movies

REQUESTS_PER_PAGE = 10


def paginate_actors(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * REQUESTS_PER_PAGE
    end = start + REQUESTS_PER_PAGE

    actors = [actor.format() for actor in selection]
    current_selection = actors[start:end]

    return current_selection


def paginate_movies(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * REQUESTS_PER_PAGE
    end = start + REQUESTS_PER_PAGE

    movies = [movie.format() for movie in selection]
    current_selection = movies[start:end]

    return current_selection


def paginate_assignments(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * REQUESTS_PER_PAGE
    end = start + REQUESTS_PER_PAGE

    assignments = [assignment.format() for assignment in selection]
    current_selection = assignments[start:end]

    return current_selection


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''Display all the actors in the Database'''

    @app.route('/actors', methods=['GET'])
    def get_actors():
        selection = Actors.query.order_by(Actors.id).all()
        current_selection = paginate_actors(request, selection)

        if len(current_selection) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': current_selection
        }), 200

    '''Display all the movies in the Database'''

    @app.route('/movies', methods=['GET'])
    def get_movies():
        selection = Movies.query.order_by(Movies.id).all()
        current_selection = paginate_movies(request, selection)

        if len(current_selection) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': current_selection
        }), 200

    '''Display all the assignments in the Database'''

    @app.route('/assignments', methods=['GET'])
    def get_assignments():
        selection = Assignments.query.order_by(Assignments.id).all()
        current_selection = paginate_assignments(request, selection)

        if len(current_selection) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'assignments': current_selection
        }), 200

    '''Delete an actor from the Database'''

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        try:
            actor = Actors.query.filter(
                Actors.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            selection = Actors.query.order_by(Actors.id).all()
            current_selection = paginate_actors(request, selection)

            if len(current_selection) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'deleted': actor_id, 
                'actors': current_selection
            }), 200

        except:
            abort(422)

    '''Delete a movie from the Database'''

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        try:
            movie = Movies.query.filter(
                Movies.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            selection = Movies.query.order_by(Movies.id).all()
            current_selection = paginate_movies(request, selection)

            if len(current_selection) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'deleted': movie_id,
                'movies': current_selection
            }), 200

        except:
            abort(422)

    '''Delete assignments from the Database'''

    @app.route('/assignments/<int:assignment_id>', methods=['DELETE'])
    @requires_auth('delete:assignments')
    def delete_assignment(payload, assignment_id):
        try:
            assignment = Assignments.query.filter(
                Assignments.id == assignment_id).one_or_none()

            if assignment is None:
                abort(404)

            assignment.delete()

            selection = Assignments.query.order_by(Assignments.id).all()
            current_selection = paginate_assignments(request, selection)

            if len(current_selection) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'deleted': assignment_id,
                'assignments': current_selection
            }), 200

        except:
            abort(422)

    '''Post request to add a new actor to the Database'''

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        if body is None:
            abort(422)

        try:
            actor = Actors(name=new_name, age=new_age, gender=new_gender)

            actor.insert()

            new_actor = Actors.query.filter(
                Actors.name == new_name).first_or_404()

            return jsonify({
                'success': True,
                'created': actor.id,
                'actor': [new_actor.format()]
            }), 200

        except Exception as e:
            print(e)
            abort(422)

    '''Post request to add a new movie to the Database'''

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        if body is None:
            abort(422)

        try:
            movie = Movies(title=new_title, release_date=new_release_date)

            movie.insert()

            new_movie = Movies.query.filter(
                Movies.title == new_title).first_or_404()

            return jsonify({
                'success': True,
                'created':movie.id,
                'movie': [new_movie.format()]
            }), 200

        except Exception as e:
            print(e)
            abort(422)

    '''Post request to add a new assignment to the Database'''

    @app.route('/assignments', methods=['POST'])
    @requires_auth('post:assignments')
    def create_assignment(payload):
        body = request.get_json()

        new_movie_id = body.get('movie_id', None)
        new_actor_id = body.get('actor_id', None)

        if body is None:
            abort(422)

        try:
            assignment = Assignments(
                movie_id=new_movie_id, actor_id=new_actor_id)

            assignment.insert()

            new_assignment = Assignments.query.filter(
                Assignments.movie_id == new_movie_id).first_or_404()

            return jsonify({
                'success': True,
                'created': assignment.id,
                'assignment': [new_assignment.format()]
            }), 200

        except Exception as e:
            print(e)
            abort(422)

    '''Patch request to update the actor details in the Database'''

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        body = request.get_json()

        try:
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            updated_name = body.get('name')
            updated_age = body.get('age')
            updated_gender = body.get('gender')

            if updated_name:
                actor.name = updated_name

            if updated_age:
                actor.age = updated_age

            if updated_gender:
                actor.gender = updated_gender

            actor.update()

            updated_actor = Actors.query.filter(Actors.id == actor_id).first_or_404()

            return jsonify({
                'success': True,
                'updated': actor_id,
                'actor': [updated_actor.format()]
            }), 200

        except Exception as e:
            print(e)
            abort(400)

    '''Patch request to update the movie details in the Database'''

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        body = request.get_json()

        try:
            movie = Movies.query.filter(Movies.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            updated_title = body.get('title')
            updated_release_date = body.get('release_date')

            if updated_title:
                movie.title = updated_title

            if updated_release_date:
                movie.release_date = updated_release_date

            movie.update()

            updated_movie = Movies.query.filter(Movies.id == movie_id).first_or_404()

            return jsonify({
                'success': True,
                'updated': movie_id,
                'movie': [updated_movie.format()]
            }), 200

        except Exception as e:
            print(e)
            abort(400)

    '''Patch request to update the assignment details in the Database'''

    @app.route('/assignments/<int:assignment_id>', methods=['PATCH'])
    @requires_auth('patch:assignments')
    def update_assignment(payload, assignment_id):
        body = request.get_json()

        try:
            assignment = Assignments.query.filter(
                Assignments.id == assignment_id).one_or_none()

            if assignment is None:
                abort(404)

            updated_movie_id = body.get('movie_id')
            updated_actor_id = body.get('actor_id')

            if updated_movie_id:
                assignment.movie_id = updated_movie_id

            if updated_actor_id:
                assignment.actor_id = updated_actor_id

            assignment.update()

            updated_assignment = Assignments.query.filter(
                Assignments.id == assignment_id).first_or_404()

            return jsonify({
                'success': True,
                'updated': assignment_id,
                'movie': [updated_assignment.format()]
            }), 200

        except Exception as e:
            print(e)
            abort(400)

    '''
    Error handling 
    '''

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.error['code'],
            "message": error.error['description']
        }), error.status_code

    @app.errorhandler(401)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
