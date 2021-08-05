# Casting Agency - Udacity Capstone Project
The Casting Agency Project models a company that is responsible for managing actors, creating movies and assigning actors to those movies. The application can be used to view, add, delete, modify the below entities:
- Actors - Contains Actor name, age and gender
- Movies - Contains Movie title and release date
- Assignments - Assign actors to movies.

Application URL - https://rab-casting-app.herokuapp.com/actors

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
```bash
python -m venv <name of venv>
venv\Scripts\activate.bat
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./starter` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Auth0 setup
You need to setup an Auth0 account.

Environment variables needed: (setup.sh)

```bash
export AUTH0_DOMAIN="xxxxxxxxxx.auth0.com" # Choose your tenant domain
export ALGORITHMS="RS256"
export API_AUDIENCE="casting" # Create an API in Auth0

```


### Roles
Below are the roles and their access levels
```
- Casting Assistant - Can view actors, movies and assignments
- Casting Director - Can view/modify movies and view/add/modify/delete actors and view/add/modify/delete assignments
- Executive Producer - Can view/add/modify/delete movies, actors and assignments
```

### Permissions
Following permissions should be created under created API settings.

```bash
view:actors
view:movies
view:assignments
post:actors
post:movies
post:assignments
delete:actors
delete:movies
delete:assignments
update:actors
update:movies
update:assignments

```

### JWT Token
JWT Token can be created using the below URL.
```bash
https://YOUR_DOMAIN/authorize?audience=API_IDENTIFIER&scope=SCOPE&response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=https://YOUR_APP/callback&state=STATE
```

## API Endpoints
```
Below are the API endpoints

```js
GET '/actors?page=${integer}'
- Fetches a paginated set of actor details. 
- Request Arguments: page - integer
- Returns: An object with 10 paginated actor details.
{
  "actors": [
    {
      "age": 25, 
      "gender": "Male", 
      "id": 1, 
      "name": "Actor1"
    }
  ], 
  "success": true
}
```

```js
GET '/movies?page=${integer}'
- Fetches a paginated set of movie details. 
- Request Arguments: page - integer
- Returns: An object with 10 paginated movie details.
{
  "movies": [
    {
      "id": 1, 
      "release_date": "Sat, 01 Jan 2022 00:00:00 GMT", 
      "title": "Movie1"
    }
  ], 
  "success": true
}
```

```js
GET '/assignments?page=${integer}'
- Fetches a paginated set of assignemnt details. This give the deatils of actors assigned to movies along with the name of the Actor and Title of the movie. 
- Request Arguments: page - integer
- Returns: An object with 10 paginated assignment details.
{
  "assignments": [
    {
      "actor_id": 2, 
      "actor_name": "Actor2", 
      "id": 1, 
      "movie_id": 1, 
      "movie_title": "Movie1"
    }
  ], 
  "success": true
}
```

```js
DELETE '/actors/${actor_id}'
- Deletes a specified actor using the id of the actor.
- Request Arguments: actor_id - integer
- Returns: An object with 10 paginated actor details where page = 1. Along with this the ID of the entry deleted, success message and appropriate HTTP response code is returned.
{
    "deleted": 9,
    "actors": [
      {
      	"age": 25, 
      	"gender": "Male", 
      	"id": 1, 
      	"name": "Actor1"
      }
    ],
    "success": true
}
```

```js
DELETE '/movies/${movie_id}'
- Deletes a specified movie using the id of the movie.
- Request Arguments: movie_id - integer
- Returns: An object with 10 paginated movie details where page = 1. Along with this the ID of the entry deleted, success message and appropriate HTTP response code is returned.
{
    "deleted": 9,
    "movies": [
        {
            "id": 1,
            "release_date": "Sat, 01 Jan 2022 00:00:00 GMT",
            "title": "Movie1"
        }
    ],
    "success": true
}
```

```js
DELETE '/assignments/${assignment_id}'
- Deletes a specified assignment using the id of the assignment.
- Request Arguments: assignment_id - integer
- Returns: An object with 10 paginated assignment details where page = 1. Along with this the ID of the entry deleted, success message and appropriate HTTP response code is returned.
{
    "deleted": 9,
    "assignments": [
    	{
      	   "actor_id": 2, 
           "actor_name": "Actor2", 
           "id": 1, 
           "movie_id": 1, 
           "movie_title": "Movie1"
    	}
    ],
    "success": true
}
```

```js
POST '/actors'
- Sends a post request in order to add a new actor. 
- Request Body: 
{
    "name": "Actor16",
    "age": 22,
    "gender": "Female"
}
- Returns: a single new actor object 
{
    "actor": [
        {
            "age": 22,
            "gender": "Female",
            "id": 16,
            "name": "Actor16"
        }
    ],
    "created": 16,
    "success": true
}
```

```js
POST '/movies'
- Sends a post request in order to add a new movie. 
- Request Body: 
{
    "title": "Movie7",
    "release_date": "2024-12-12"
}
- Returns: a single new movie object 
{
    "created": 7,
    "movie": [
        {
            "id": 7,
            "release_date": "Thu, 12 Dec 2024 00:00:00 GMT",
            "title": "Movie7"
        }
    ],
    "success": true
}
```

```js
POST '/assignments'
- Sends a post request in order to add a new assignment.
- Request Body: 
{
    "movie_id": 4,
    "actor_id": 4
}
- Returns: a single new assignment object 
{
    "assignment": [
        {
            "actor_id": 4,
            "actor_name": "Actor4",
            "id": 3,
            "movie_id": 4,
            "movie_title": "NewMovie"
        }
    ],
    "created": 3,
    "success": true
}
```

```js
PATCH '/actors/${actor_id}'
- Update a specified actor using the id of the actor.
- Request Arguments: actor_id - integer
- Request Body : 
{
    "name": "Dwayne Johnson"
}
- Returns: a single updated actor object.
{
    "actor": [
        {
            "age": 22,
            "gender": "Female",
            "id": 20,
            "name": "Dwayne Johnson"
        }
    ],
    "success": true,
    "updated": 20
}
```

```js
PATCH '/movies/${movie_id}'
- Update a specified movie using the id of the movie.
- Request Arguments: movie_id - integer
- Request Body : 
{
    "title": "Jumanji"
}
- Returns: a single updated actor object.
{
    "movie": [
        {
            "id": 7,
            "release_date": "Thu, 12 Dec 2024 00:00:00 GMT",
            "title": "Jumanji"
        }
    ],
    "success": true,
    "updated": 7
}
```

```js
PATCH '/assignments/${assignment_id}'
- Update a specified assignment using the id of the assignment.
- Request Arguments: assignment_id - integer
- Request Body : 
{
    "actor_id": 4,
    "movie_id": 4
}
- Returns: a single updated actor object.
{
    "movie": [
        {
            "actor_id": 4,
            "actor_name": "Actor4",
            "id": 3,
            "movie_id": 4,
            "movie_title": "NewMovie"
        }
    ],
    "success": true,
    "updated": 3
}
```

```

## Testing
Testcases can be referred from below -  
```
- Using Postman - Casting Agency.postman_collection.json
- Using Unittest - test_app.py - Update the JWTs
```
# Casting-app
