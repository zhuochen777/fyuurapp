# Trivia API


## Introduction

Trivia is an application where team members can hold trivia on a regular basis and play the game. It creates communication and bonding experiences within the whole team. This application can:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started
### Pre-requisites and Local Development
1. Developers using this application should have the following on their local machine:
- virtualenv
- SQLAlchemy ORM
- PostgreSQL
- Python3
- Flask-Migrate
You can download and install the dependencies mentioned above using pip as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```

2. Initialize and activate a virtual env using:
```
python -m virtualenv env
source env/bin/activate
```
Note in Windows using:
```
python -m virtualenv env
source env/Scripts/activate
```

### Backend
From the backend folder to install packages, run pip install requirements.txt

To run the application run the following commands:
```
export FLASK_APP=flaskr
export FLASK_DEBUG=1
flask run
```
The commands put the application in development and directs it to use the __init__.py in flaskr folder. The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

### Frontend
Developers must have Node and Node Package Manager(NPM) installed on their machine.

To install project dependencies, from the frontend folder, run:
```
npm install
```

To run the application, run:
```
npm start
```
The application frontend will run on http://127.0.0.1:3000/ by default.

### Test
To run tests, navigate to the backend folder and in trivia.psql make sure owner is username on your machine. Run the following commands:
```
dropdb trivia_test
createdb trivia_test
psql -f trivia.psql -U {username} -d trivia_test
python3 test_flaskr.py
```
 The first time running the tests, omit the dropdb command.
 All tests are kept in test_flaskr.py and should be updated accordingly when app functionality changes.

## API Reference
### Getting Started
- Base URL: At present this app can only be run locally. The backend is hosted at gttp://127.0.0.1:5005/ by default.
- Authentication: This version of the application does not require authentication or API keys

### Error Handling
Errors are returned in JSON format as following:
```
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```
The API will return four error types when requests fail:
- 404: Resource Not Found
- 422: Unprocessable
- 405: Mathod Not Allowed
- 500: Internal Server Error

### End Points
#### GET /categories
Returns success value, all available trivia question categories including their id and type.
Sample: curl http://127.0.0.1:5000/categories
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```
#### GET /questions
Returns success value, a list of questions, number of total questions, current category, categories. Results are paginated in groups of 10. Include a request argument to choose page number starting from 1.
Sample: curl http://127.0.0.1:5000/questions
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    <!-- other questions are displayed here if applicable-->
  ],
  "success": true,
  "total_questions": 23
}
```
#### DELETE /questions/<int:question_id>
Deletes the question of given id if exists. Returns success value, the id of the deleted book, total number of questions and the questions list.
Sample: curl http://127.0.0.1:5000/questions/16 -X DELETE
```
{
  "current_questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
<!-- other questions are displayed here if applicable-->
  ],
  "delete_question_id": 16,
  "success": true,
  "total_num_questions": 22
}
```
#### POST /questions
If search term exists in request, it returns success value, current category, total number of questions and the list of questions that contain search term in question value.
Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "better"}'
```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    <!-- other questions are displayed here if applicable-->
  ],
  "success": true,
  "total_questions": 22
}
```
If search term does not exists in request, it creates a new question based on request and returns success value, current category, question list, total number of questions.
Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "test question", "answer": "test answer", "category": "1", "difficulty": "1"}'
```
{
  "current_category": 1,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
<!-- other questions are displayed here if applicable-->
  ],
  "success": true,
  "total_questions": 23
}
```
#### GET /categories/<int:category_id>/questions
Returns success value, current category, list of questions based on current category, total number of questions.
Sample: curl http://127.0.0.1:5000/categories/2/questions
```
{
  "current_category": 2,
  "questions": [
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    }
    <!-- other questions are displayed here if applicable-->
  ],
  "success": true,
  "total_questions": 23
}
```
#### POST /quizzes
Generates a random quiz other than previously chosen one. If category is specified, pick the quiz from that category. If not, pick it from all categories.
Sample: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [18, 19], "quiz_category": {"id": 2, "type": "Art"}}'
```
{
  "question": {
    "answer": "Mona Lisa",
    "category": 2,
    "difficulty": 3,
    "id": 17,
    "question": "La Giaconda is better known as what?"
  },
  "success": true
}
```
