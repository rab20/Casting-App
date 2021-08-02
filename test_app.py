import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Assignments, Actors, Movies


class CastingTestCase(unittest.TestCase):
    """This class represents the Casting test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # self.executive_producer = os.environ['EXECUTIVE_PRODUCER']
        # self.casting_director = os.environ['CASTING_DIRECTOR']
        # self.casting_assistant = os.environ['CASTING_ASSISTANT']
        self.executive_producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZhazhHYmMzR3l0cERaRjB3M0d3OCJ9.eyJpc3MiOiJodHRwczovL2JoYXJhdC1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNDI1NTA2NjA0NDgwMzIwMTYwMSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2Mjc3NDE2NzAsImV4cCI6MTYyNzgyODA3MCwiYXpwIjoiUnR5QVhuR3ZSY2xmQm00WTZpblpaQXhpUnlvc1pONWMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6YXNzaWdubWVudHMiLCJkZWxldGU6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6YXNzaWdubWVudHMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6YXNzaWdubWVudHMiLCJwb3N0Om1vdmllcyJdfQ.KdxLlms0i0LOdylCbigMK23nzac_D9RSJ-yM1VD_1zmC_DjfcTU7QrPixHMbPudIQBM1E0Pwj-fyyqiKNtII4BLH4d8V1Ex2gHSAA3R1obxldAfLFZ5BmbIjMCrXbMIIoYfWaeXGCd_yPqnqHMzWJRwniXsKk1OxNvWYl0tUrCmuiu4FITzFwWg2YXir3uQ3PBfMMRH5xaHidNEs-Wo3TvO1i237ELPo69lUk3bH_f6bPCxY5GHC38Os1dZNLEIzn-E3_OKN648aiJzcvksAk6T-WhKoft-s617Ps5kpoB5cVJeQDMtL1a41mf1FOd8HKfy5_TRCbGYEO8R0gATtKw'
        self.casting_director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZhazhHYmMzR3l0cERaRjB3M0d3OCJ9.eyJpc3MiOiJodHRwczovL2JoYXJhdC1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNjUzNzIxMDI5ODY2NDk2NTg5NyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2Mjc3MzM1OTYsImV4cCI6MTYyNzc0MDc5NiwiYXpwIjoiUnR5QVhuR3ZSY2xmQm00WTZpblpaQXhpUnlvc1pONWMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6YXNzaWdubWVudHMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDphc3NpZ25tZW50cyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDphc3NpZ25tZW50cyJdfQ.ezagEsCo_CKnx-_Gw7au85p9kJaqAlmOMb1YOLHTJf4Xp-sDNYYtXrKqpieA5oPj0W7tgrsQUWX0QRA0KP5mUO0urNHnvlbLtbQi-zWDyi3-KDj8NsXZhCbKyRrWoepdJCTjRIGz99mzCl7-vjMN4uSIRoCw2LRRsDAWVhXZt9Nb7ZcGUou9_g3b8iz-0cDD4KW-ZkEGS0mJ_-WWGuw6maITwe6PxeVjGqzgm4r90NgGgWike0eFDOxBqpqXGC9nXYgcVVj31ctY3PTkH3mZJbAZUNg38j8q1Y1VhxEqc5C1Zp7XhFHhY8SK862o_ex9E2jUGw7QBjvg5chVJHU93g'
        self.casting_assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZhazhHYmMzR3l0cERaRjB3M0d3OCJ9.eyJpc3MiOiJodHRwczovL2JoYXJhdC1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGZkNjdlZmQwNTY3NTAwNzBkOTVlOTUiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjI3NzMzNDgxLCJleHAiOjE2Mjc3NDA2ODEsImF6cCI6IlJ0eUFYbkd2UmNsZkJtNFk2aW5aWkF4aVJ5b3NaTjVjIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6W119.RfkXaKj_hI1Jm432BKC-t50x5OjfQFRsbO1d3EjjHPW0vUYhFblrXJnt67QL5gWe_A5Wu9xLwXqz-Lo5LQ9eEl-Q_TpuvhN7VDHDXezECMpLXKK78FVtqqHFp-663VIzaP2qedKKAV4YR8pLgv_rimlcV3GRtViqJp9rsQG7sJ18a1PpFEewljDv5SA8uBhh09ADwYWAqGn6aS-h3GmmqCULxKT0i9u5nvudGGGGSOrv3vtckiriop-e9ZO4owspAOcwTxpGAWjA1myXwUVgyO2itmMBhnwutNRWJVff3ovjqDAKFL-ehsNHoHhevG3VuPiK9poJ3xBz1Y_r9fT1YQ'

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_actor = {
            'name': 'Actor19',
            'age': 22,
            'gender': 'Female'
        }

        self.new_movie = {
            'title': 'NewMovie',
            'release_date': '2024-12-12'
        }

        self.new_assignment = {
            'movie_id': 14,
            'actor_id': 14
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Conditions to test actors endpoints without RBAC
    """

    def test_get_paginated_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_404_actors_beyond_valid_page(self):
        res = self.client().get('/actors?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor(self):
        res = self.client().delete('/actors/11',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 11).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 11)
        self.assertTrue(len(data['actors']))
        self.assertEqual(actor, None)

    def test_422_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/1000',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_actor(self):
        total_actors_initial = len(Actors.query.all())
        res = self.client().post('/actors',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json=self.new_actor)
        data = json.loads(res.data)
        total_actors_final = len(Actors.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['actor']))
        self.assertEqual(total_actors_final, total_actors_initial + 1)

    def test_405_if_actor_creation_not_allowed(self):
        res = self.client().post('/actors/45',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_update_actor(self):
        res = self.client().patch('/actors/10',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json={'name': 'Bharat'})
        data = json.loads(res.data)
        updated_actor = Actors.query.filter(Actors.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(updated_actor.name, 'Bharat')

    def test_400_for_failed_actor_update(self):
        res = self.client().patch('/actors/45',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    """
    Conditions to test movies endpoints without RBAC
    """

    def test_get_paginated_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_404_movies_beyond_valid_page(self):
        res = self.client().get('/movies?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        res = self.client().delete('/movies/11',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 11).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 11)
        self.assertTrue(len(data['movies']))
        self.assertEqual(movie, None)

    def test_422_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/1000',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_movie(self):
        total_movies_initial = len(Movies.query.all())
        res = self.client().post('/movies',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json=self.new_movie)
        data = json.loads(res.data)
        total_movies_final = len(Movies.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['movie']))
        self.assertEqual(total_movies_final, total_movies_initial + 1)

    def test_405_if_movie_creation_not_allowed(self):
        res = self.client().post('/movies/45',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_update_movie(self):
        res = self.client().patch('/movies/10',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json={'title': 'Titanic'})
        data = json.loads(res.data)
        updated_movie = Movies.query.filter(Movies.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(updated_movie.title, 'Titanic')

    def test_400_for_failed_movie_update(self):
        res = self.client().patch('/movies/45',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    """
    Conditions to test assignments endpoints without RBAC
    """

    def test_get_paginated_assignments(self):
        res = self.client().get('/assignments')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['assignments']))

    def test_404_assignments_beyond_valid_page(self):
        res = self.client().get('/assignments?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_assignment(self):
        res = self.client().delete('/assignments/11',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        assignment = Assignments.query.filter(
            Assignments.id == 11).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 11)
        self.assertTrue(len(data['assignments']))
        self.assertEqual(assignment, None)

    def test_422_if_assignment_does_not_exist(self):
        res = self.client().delete('/assignments/1000',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_assignment(self):
        total_assignments_initial = len(Assignments.query.all())
        res = self.client().post('/assignments',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json=self.new_assignment)
        data = json.loads(res.data)
        total_assignments_final = len(Assignments.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['assignment']))
        self.assertEqual(total_assignments_final,
                         total_assignments_initial + 1)

    def test_405_if_assignemnt_creation_not_allowed(self):
        res = self.client().post('/assignments/45',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json=self.new_assignment)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_update_assignment(self):
        res = self.client().patch('/assignments/10',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json={'actor_id': 1})
        data = json.loads(res.data)
        updated_assignment = Assignments.query.filter(
            Assignments.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(updated_assignment.actor_id, 1)

    def test_400_for_failed_assignment_update(self):
        res = self.client().patch('/assignments/45',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    """
    RBAC Authentications for casting_assistant
    """

    def test_create_new_actor_casting_assistant(self):
        res = self.client().post('/actors',
                                 headers={"Authorization": "Bearer {}".format(self.casting_assistant)}, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertEqual(data['error'], 'unauthorized')

    def test_get_movies_casting_assistant(self):
        res = self.client().post('/movies',
                                 headers={"Authorization": "Bearer {}".format(self.casting_assistant)}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    """
    RBAC Authentications for casting_director
    """

    def test_create_new_actor_casting_director(self):
        res = self.client().post('/actors',
                                 headers={"Authorization": "Bearer {}".format(self.casting_director)}, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], 21)

    def test_create_new_movie_casting_director(self):
        res = self.client().post('/movies',
                                 headers={"Authorization": "Bearer {}".format(self.casting_director)}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertEqual(data['error'], 'unauthorized')

    """
    RBAC Authentications for executive_producer
    """

    def test_create_new_movie_executive_producer(self):
        res = self.client().post('/movies',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], 5)
    
    def test_delete_movie_executive_producer(self):
        res = self.client().delete('/movies/10',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        movie = Movies.query.filter(
            Movies.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 10)
        self.assertTrue(len(data['movies']))
        self.assertEqual(movie, None)

    def test_update_movie_executive_producer(self):
        res = self.client().patch('/movies/5',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json={'title': 'Titanic'})
        data = json.loads(res.data)
        updated_movie = Movies.query.filter(Movies.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(updated_movie.title, 'Titanic')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
