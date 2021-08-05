import os
from typing import AsyncGenerator
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from flask_migrate import Migrate
from sqlalchemy.sql.sqltypes import Date, DateTime

# database_path = os.environ['DATABASE_URL']
database_path = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
# database_name = "castingdb"
# database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'postgres','localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

'''
Assignments

'''
class Assignments(db.Model):  
  __tablename__ = 'Assignments'

  id = Column(Integer, primary_key=True)
  movie_id = Column(Integer, ForeignKey('Movies.id'))
  actor_id = Column(Integer, ForeignKey('Actors.id'))

  def __init__(self, movie_id, actor_id):
    self.movie_id = movie_id
    self.actor_id = actor_id

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    movie_title = Movies.query.filter(Movies.id == self.movie_id).all()
    for el in movie_title:
      # print (el.title) 
      title_val = el.title

    actor_name = Actors.query.filter(Actors.id == self.actor_id).all()
    for el in actor_name:
      # print (el.name)
      name_val = el.name

    return {
      'id': self.id,
      'movie_id': self.movie_id,
      'movie_title': title_val, 
      'actor_id': self.actor_id,
      'actor_name': name_val
    }

'''
Movies

'''
class Movies(db.Model):  
  __tablename__ = 'Movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(Date)
  assignments = relationship('Assignments', backref="Movies", lazy=True)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date
    }

'''
Actors

'''
class Actors(db.Model):  
  __tablename__ = 'Actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)
  assignments = relationship('Assignments', backref="Actors", lazy=True)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
    }
