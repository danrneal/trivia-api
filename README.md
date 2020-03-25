# Trivia API

This app allows users to play a trivia quiz game based on questions and categories specified. Users can post new questions, rate existing questions, and play a trivia quiz from a given category or from all categories. This app uses a flask-based api in the backend, a postgresql database, and a react frontend. You will need python3, nodejs, and postgres installed to run the app.

## Set-up

Set-up a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see (venv) before your command prompt now. (You can type `deactivate` to exit the virtual environment any time.)

### Backend

Navigate to the backend folder

Install the requirements:

```bash
pip install -r requirements.txt
```

Set up your environment variables:

```bash
touch .env
echo FLASK_APP=flaskr >> .env
echo FLASK_ENV=development >> .env
```

### Frontend

Navigate to the frontend folder

Install the requirements:

```bash
npm install
```

## Usage

To start the backend, run the following command from the backend folder:

```bash
flask run
```

To start the frontend, run the following command in another terminal from the frontend folder:

```bash
npm start
```

Navigate to `http://127.0.0.1:3000/` to see the app in action!

## Screenshots

![Trivia App Homepage](https://i.imgur.com/xjnhoj4.png)
![Trivia App Add Question Page](https://i.imgur.com/8NTqu14.png)
![Trivia App Play Quiz Game Page](https://i.imgur.com/AkGyWfs.png)

## API Reference

### Base URL

When running locally with the built in flask server, the base url is as follows:

```bash
http://127.0.0.1:5000/
```

### Error Handling

Below are a list of errors that may be raised as part of the api

#### 400: Bad Reqeuest

This is returned when the requested is malformed in some way. (i.e. Required info is missing)

#### 404: Not Found

This is returned when the requested resource does not exist. (i.e. Attempting to view a page of questions that don't exist)

#### 405: Method Not Allowed

This is returned when the incorrect request method is specified at an endpoint. (i.e. Attempting to delete with specifying a specific question to delete)

#### 422: Unprocessable Entity

This is returned when the request is unable to be fuffilled in some way. (i.e. Attempting to update a question that has previously been deleted)

#### 500: Internal Server Error

This is returned when something there is a problem with the server.

### Endpoints

Questions:

#### GET /questions

Retrieve a list of paginated questions

```bash
curl http://127.0.0.1:5000/questions?page=1
```

- page (int) [optional]: Each page returns the next 10 results (default: 1)

```bash
{
  "success": true,
  "questions": [
    {
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
      "answer": "Apollo 13",
      "category_id": 5,
      "rating": 3,
      "difficulty": 4
    }
  ],
  "total_questions": 1,
  "current_category_id": null,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

#### POST /questions

Create a new question of search all questions

##### New Question

```bash
curl -X POST -H "Content-Type: application/json" -d '{"question": "What is the answer to life the universe and everything?", "answer": "42", "category_id": "1", "rating": "3", "difficulty": "5"}' http://127.0.0.1:5000/questions
```

- question (str): The content of the question
- answer (str): The answer to the question
- category_id (int): The id of the category that the question belongs to
- rating (int): The rating of the question
- difficulty (int): The difficulty of the question

```bash
{
  "success": true,
  "created_question_id": 24
}
```

##### Search Questions

```bash
curl -X POST -H "Content-Type: application/json" -d '{"search_term": "hanks"}' http://127.0.0.1:5000/questions
```

- search_term (str): The string to search for in the questions

```bash
{
  "success": true,
  "questions": [
    {
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
      "answer": "Apollo 13",
      "category_id": 5,
      "rating": 3,
      "difficulty": 4
    }
  ],
  "total_questions": 1,
  "current_category_id": null,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

#### PATCH /questions/<question_id>

Update a question's rating

```bash
curl -X PATCH -H "Content-Type: application/json" -d '{"rating": "5"}' http://127.0.0.1:5000/questions/2
```

- rating (int): The rating of the question

```bash
{
  "success": true,
  "updated_question_id": 2,
  "old_rating": 3,
  "new_rating": 5
}
```

#### DELETE /questions/<question_id>

Delete a question

```bash
curl -X DELETE http://127.0.0.1:5000/questions/2
```

```bash
{
  "success": true,
  "deleted_question_id": 2
}
```

Categories:

#### GET /categories

Retrieve all categories

```bash
curl http://127.0.0.1:5000/categories
```

```bash
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

#### POST /categories

Create a new category

```bash
curl -X POST -F "name=People" -F "icon=@/path/to/icon.svg" http://127.0.0.1:5000/categories
```

##### *Note: This request takes form data rather than json in order to accomadate the file upload for the category icon*

- name (str): The name of the category
- icon: An svg file that is the icon for the category

```bash
{
  "success": true,
  "created_category_id": 7
}
```

#### GET /categories/<category_id>/questions

Retrieve all questions belonging to a specific category

```bash
curl http://127.0.0.1:5000/categories/5/questions
```

```bash
{
  "success": true,
  "questions": [
    {
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
      "answer": "Apollo 13",
      "category_id": 5,
      "rating": 3,
      "difficulty": 4
    }
  ],
  "total_questions": 1,
  "current_category_id": 5,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

Quizzes:

#### POST /quizzes

```bash
curl -X POST -H "Content-Type: application/json" -d '{"quiz_category_id": "5", "previous_question_ids": []}' http://127.0.0.1:5000/quizzes
```

- quiz_category_id (int): The id of the category that the question belongs to (0 represents all categories)
- previous_question_ids: A list of ints representing the ids of previous questions

```bash
{
  "success": true,
  "question": {
    "id": 2,
    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
    "answer": "Apollo 13",
    "category_id": 5,
    "rating": 3,
    "difficulty": 4
  }
}
```

##### *Note: This endpoint returns a single question representing a random question in the given category, rather than a list of questions*

Users:

#### GET /users

Retrieve all questions

```bash
curl http://127.0.0.1:5000/users
```

```bash
{
  "success": true,
  "users": {
    "1": "Alice",
    "2": "Bob",
    "3": "Charlie"
  }
}
```

#### POST /users

Create a new user

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "David"}' http://127.0.0.1:5000/users
```

- username (str): The name of the user

```bash
{
  "success": true
  "created_user_id": 4
}
```

#### PATCH /users/<user_id>

Update a user's score

```bash
curl -X PATCH -H "Content-Type: application/json" -d '{"score": "2"}' http://127.0.0.1:5000/users/1
```

- score (int)

```bash
{
  "success": true,
  "updated_user_id": 1,
  "old_score": 1,
  "new_score": 3
}
```

## Testing Suite

The backend has a testing suite to test all of the API endpoints

To set up the test database:

```bash
cd ./backend
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
```

To run all the tests:

```bash
usage: test_flaskr.py
```

## Credit

[Udacity's Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)

## License

Trivia API is licensed under the [MIT license](https://github.com/danrneal/trivia-api/blob/master/LICENSE).
