# Backend - Full Stack Trivia API 

## Setup for Backend:

### 1. Python 3.7
Follow instructions to install verion 3.7 [python docs](https://docs.python.org/3.7/using/unix.html#getting-and-installing-the-latest-version-of-python)


### 2. **Virtual Enviornment** 
We recommend working within a virtual environment whenever using Python for projects. 

Enter this commands in terminal to install and start Virtual Enviroment:
One of the dependencies doesn't work on python version 3.8 and above, so make sure you use 3.7.
```
py -3.7 -m venv venv
venv\Scripts\activate 
```
**or**
```
python3.7 -m venv venv
source venv\Scripts\activate 
```

This keeps your dependencies for each project separate and organaized. More detailed instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


### 3. **PIP Dependencies**
Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and run:
```
pip install -r requirements.txt
```
**or**
```
pip3 install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


### 4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```
psql -U <USERNAME> trivia < trivia.psql
```

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Set virtual enviroment variables:
```
set FLASK_APP=src/app.py
set FLASK_ENV=development
set DB_USER=<YOUR DATABASE USERNAME>
set DB_PASSWORD=<PASSWORD FOR YOUR DATABASE USER>
```
**or**
```
$env:FLASK_APP = "src/app.py"
$env:FLASK_ENV = "development"
$env:DB_USER = "<YOUR DATABASE USERNAME>"
$env:DB_PASSWORD = "<PASSWORD FOR YOUR DATABASE USER>"
```
**or**
export FLASK_APP=src/app.py
export FLASK_ENV=development
export DB_USER=<YOUR DATABASE USERNAME>
export DB_PASSWORD=<PASSWORD FOR YOUR DATABASE USER>

To run the server, execute:
```
flask run --reload
```
If it doesn't work with this command, try:
```
python -m flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Testing
To run the tests, run
```
dropdb -U <USERNAME> trivia_test
createdb -U <USERNAME> trivia_test
psql -U <USERNAME> trivia_test < trivia.psql
python test_flaskr.py
```
Make sure you set enviroment variables as described in 'Running the server'! 
Also write commands in bash as if you do it in windows terminal they may fail.