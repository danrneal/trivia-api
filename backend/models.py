"""Model objects used to model data for the db

Attributes:
    DB_DIALECT: A str representing the dialect of the db
    DB_HOST: A str representing the host of the db
    DB_PORT: An int representing the port the db is running on
    DB_NAME: A str representing the db in which to connect to
    DB_PATH: A str representing the location of the db
    db: A SQLAlchemy service

Classes:
    Question()
    Category()
"""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

DB_DIALECT = "postgresql"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "trivia"

DB_PATH = f"{DB_DIALECT}://{DB_HOST}:{DB_PORT}/{DB_NAME}"

db = SQLAlchemy()


def setup_db(app, database_path=DB_PATH):
    """Binds a flask application and a SQLAlchemy service

    Args:
        app: A flask app
        database_path: A str representing the location of the db
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = "../frontend/public"
    db.app = app
    db.init_app(app)
    db.create_all()


class Question(db.Model):
    """A model representing a trivia question

    Attributes:
        id: An int that serves as the unique identifier for a question
        question: A str representing the content of the question
        answer: A str representing the answer to the question
        category_id: The id of the category that the question belongs to
        rating: An int representing the rating of the question
        difficulty: An int representing the difficulty of the question
    """

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    rating = Column(Integer)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category_id, rating, difficulty):
        self.question = question
        self.answer = answer
        self.category_id = category_id
        self.rating = rating
        self.difficulty = difficulty

    def insert(self):
        """Inserts a new question object into the db"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates an existing question object in the db"""
        db.session.commit()

    def delete(self):
        """Deletes an existing question object from the db"""
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """Formats the question object as a dict

        Returns:
            question: A dict representing the question object
        """
        question = {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "category_id": self.category_id,
            "rating": self.rating,
            "difficulty": self.difficulty,
        }
        return question


class Category(db.Model):
    """A model representing a category of trivia questions

    Attributes:
        id: An int that serves as the unique identifier for a category
        name: A str representing the name of the category
    """

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    questions = relationship("Question", backref="category")

    def __init__(self, name):
        self.name = name

    def insert(self):
        """Inserts a new category object into the db"""
        db.session.add(self)
        db.session.commit()

    def format(self):
        """Formats the category object as a dict

        Returns:
            category: A dict representing the category object
        """
        category = {
            "id": self.id,
            "name": self.name,
        }
        return category


class User(db.Model):
    """A model representing a user

    Attributes:
        id: An int that serves as the unique identifier for a user
        username: A str representing the name of the user
        score: An int representing the lifetime score of a user
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    score = Column(Integer, default=0)

    def __init__(self, username, score):
        self.username = username
        self.score = score

    def insert(self):
        """Inserts a new user object into the db"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates an existing user object in the db"""
        db.session.commit()

    def format(self):
        """Formats the user object as a dict

        Returns:
            user: A dict representing the user object
        """
        user = {
            "id": self.id,
            "username": self.username,
            "score": self.score,
        }
        return user
