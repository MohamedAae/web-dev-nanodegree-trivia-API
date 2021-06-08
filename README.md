# Full Stack API Final Project

**Udacitrivia** is  a trivia, where users can add, answer, and view questions and answers. I've worked to develop an API on the backend to fulfill the data requirements, which includes:

1) **Display questions** - both all questions and by category.
2) **Delete questions.**
3) **Add questions** and require that they include the question and answer text.
4) **Search for questions** based on a text query string.
5) **Play the quiz game**, randomizing either all questions or within a specific category.

The project adheres to the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/) and follows *common best practices* including, using clear function and variables names.

## Getting Started
___
### **Techincal Stack**
The projects needs **`Python3`**, **`pip`**, **`node`**, **`npm`**, and **`PostgreSQL`** to run.

### *Backend Dependencies /*
The project requires Python >= **3.7**, it is recommended to set up a virtual environment for your project, this [guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) will help you set it up.

&mdash; **Key Dependencies**
- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQLite database.
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) handles cross-origin requests from our frontend server.

&mdash; **Running the server**

From within the `backend` directory first, ensure you are working using your created virtual environment.
To run the server, execute:
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
<br>

### *Database Setup /*
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
<br>

### *Frontend Dependencies /*
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

&mdash; **Installing dependencies**

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```
&mdash; **Running Your Frontend in Dev Mode**

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## API Reference
___
## *End Points* &mdash;

### **`GET` /categories**
`Behavior:`
- Retrieve & return a list of all categories.
- Returns each category name and id.

`Sample Request:`
```
curl http://localhost:5000/categories
```
`Response:`
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


### **`GET` /questions**
`Behavior:`
- Retrieve & return a list of all questions paginated into groups of 10 questions per page.
- Return a list of categories, questions, and the number of total questions.
- Questions list contains the id, question, category, answer, and difficulty.

`Sample Request:`
```
curl http://localhost:5000/questions
```
`Response:`
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
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```


### **`POST` /questions**
`Behavior:`
- It either creates a new question or returns search results.
- **If no search term is sent:**
    - The endpoint will create a new question.
    - Then the endpoint returns paginated questions with the newly added question.

`Sample Request:`
```
curl -X POST http://localhost:5000/questions -H "Content-Type: application/json" -d '{ "question": "how many states in usa", "answer": "50", "difficulty": 2, "category": "3" }'
```
`Response:`
```
{
  "created": 28,
  "questions": [
    ...
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
    ...
  ],
  "success": true,
  "total_questions": 21
}
```
- **If the request contains search term:**
    - It returns search results

`Sample Request:`
```
curl -X POST http://localhost:5000/questions -H "Content-Type: application/json" -d '{"searchTerm": "usa"}'
```
`Response:`
```
{
  "current_category": null,
  "questions": [
    {
      "answer": "50",
      "category": 3,
      "difficulty": 2,
      "id": 28,
      "question": "how many states in usa"
    }
  ],
  "success": true,
  "total_questions": 22
}
```


### **`DELETE` /questions/\<int:question_id>**
`Behavior:`
- Deletes question by id.
- Returns message of the deleted question id.

`Sample Request:`
```
curl -X DELETE http://localhost:5000/questions/20
```
`Response:`
```
{
  "deleted": 20,
  "success": true
}
```


### **`GET` /categories/\<int:cat_id>/questions**
`Behavior:`
- Get questions only for the given category id.
- Returns paginated questions.

`Sample Request:`
```
curl http://localhost:5000/categories/3/questions
```
`Response:`
```
{
  "current_category": "Geography",
  "questions": [
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
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Michigan",
      "category": 3,
      "difficulty": 3,
      "id": 27,
      "question": "Which US state contains an area known as the Upper Penninsula?"
    },
    {
      "answer": "50",
      "category": 3,
      "difficulty": 2,
      "id": 28,
      "question": "how many states in usa"
    }
  ],
  "success": true,
  "total_questions": 5
}
```
### **`POST` /quizzes**
`Behavior:`
- Allows users to start a new quiz game.
- Returns a series of questions for the selected category.
- If all questions are answered, the game ends.

`Sample Request:`
```
curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "Art", "id": "2"}}'
```
`Response:`
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

## *Error Handling* &mdash;
| `Code` | `Description`      |
| ------ | ------------------ |
| 400    | Bad Request        |
| 404    | Resource Not Found |
| 422    | Unprocessable      |

`Sample Response:`
- `400`
```
{
    'success': False,
    'error': 400,
    'message': 'Bad Request'
}
```
- `404`
```
{
    'success': False,
    'error': 404,
    'message': 'Resource Not Found'
}
```
- `422`
```
{
    'success': False,
    'error': 422,
    'message': 'Unprocessable'
}
```
