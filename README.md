# Trivia API
This project is a showcasing knowledge how to implement api with python. It can also be used as a template on the subject. The app allows people to have trivia using a webpage.

## Getting started
### Pre-requisites
In order to work with the project, you need to have the following installed on your computer:
- Python 3.7
- Postgresql
- Node.js
- Node Package Manager (NPM)

### Setup
The project is split onto two sections:
- [frontend](./frontend/README.md)
- [backend](./backend/README.md)
Go to individual folders and follow each setup.

#### Quick setup for frontend
Open a terminal, cd into frontend folder and run:
```
npm i
npm start
```
#### Quick setup for backend
There might be different variations of your systems so I recommend following the guide in [backend](./backend/README.md) folder!

Open another terminal, cd into backend folder and run:
```
py -3.7 -m venv venv
venv\Scripts\activate 
pip install -r requirements.txt
psql trivia < trivia.psql
set FLASK_APP=src/app.py
set FLASK_ENV=development
set DB_USER=postgres
set DB_PASSWORD=postgres
flask run --reload
```
**If you get errors, follow the guide in backend folder!**

## Full Stack Trivia
The application implemended with Front-end does the following:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

There are also other functionalities implemented on the backend. Use *API reference* as guidence.

## API Reference
### Getting started
- Base URL: This app can only be run locally and it is not hosted as a base URL. It is hosted at the default `http://127.0.0.1:5000/`.

### Error Handling
Errors are returned as JSON objects in this format:
```
{
      "success": False, 
      "error": 400,
      "message": "Bad request"
}
```
The API can return 5 types of errors when the request fails:
- 400: Bad request
- 404: Not found
- 409: Already exists
- 422: Unprocessable
- 500: Internal Server Error

### Endpoints
#### GET /categories
Returns an object categories with category id as key and category name as value.

**Sample return**
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
#### POST /categories
Creates a new category by sending JSON object to the api. Returns the newly created category.
- If the JSON object is empty, it should return 422 error. 
- If the category already exists it should return 409 error

*JSON object sent to API*
```
{
    "category": "Music"
}
```
**Sample return**
```
{
    "category": "Music",
    "success": true
}
```
#### DELETE /categories/{category_id}
Deletes the catagory of the provided ID. Returns the id of the category deleted.
**Sample return**
```
{
    "category_id": 1,
    "success": true
}
```
#### GET /questions
Returns categories and questions paginated in groups of 10. Add request argument to choose page number, default is 1.
**Sample return**
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
    "current_category": 0,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 1,
            "difficulty": 2,
            "id": 2,
            "question": "Test Question"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 19
}
```
#### POST /questions
Creates a new question by sending JSON object. It returns only status 200 if successfully submitted.
- If the body or any other input is empty it returns 422 error.
*JSON object sent to API*
```
{
    "question": "Make new question?",
    "answer": "Answer to the new question",
    "difficulty": 3,
    "category": 3
}
```
**Sample return**
```
{
    "success": true
}
```
#### POST /questions/search
Recieves a search term string and returns an array of questions that had that string inside the question
*JSON object sent to API*
```
{
    "searchTerm": "title"
}
```
**Sample return**
```
{
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "success": true,
    "total_questions": 2
}
```
#### DELETE /questions/{question_id}
Deletes the question of the provided ID. It returns the id of the question deleted.
**Sample return**
```
{
    "question_id": 1,
    "success": true
}
```
#### PUT /questions/{question_id}
It updates the question. It updates only the inputs that aren't empty, otherwise it ignores them when empty. It returns the newly updated question.
*JSON object sent to API*
```
{
    "question": "Update new question?",
    "answer": "Answer to the updated question"
}
```
**Sample return**
```
{
    "question": {
        "answer": "Answer to the updated question",
        "category": 1,
        "difficulty": 2,
        "id": 5,
        "question": "Update new question?"
    },
    "success": true
}
```
#### GET /categories/{category_id}/questions
Returns questions for the provided category ID. It returns list of questions, number of questions and category name.
**Sample return**
```
{
    "current_category": "Art",
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": true,
    "total_questions": 4
}
```
#### POST /quizzes
Recieves a question selected to play as 'quiz_category' and an array of IDs of questions already answered and returns one random question.
*JSON object sent to API*
```
{
    "quiz_category": {
        "type": "Art",
        "id": 2
        },
    "previous_questions": []
}
```
**Sample return**
```
{
    "question": {
        "answer": "One",
        "category": 2,
        "difficulty": 4,
        "id": 18,
        "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    "success": true
}
```

- If the questions are all answered it returns:
```
{
    "status": "no more questions"
}
```


## Authors
- API and tests by Jaka Presecnik
- Starter code with frontend provided from Udacity [link](https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter)