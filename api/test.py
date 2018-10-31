# Run this file to start the Flask API server
# e.g. "python test.py" in command line

# To test requests with this API, use Postman
# We will also need to host this somewhere

# Useful URLs:
# http://flask.pocoo.org/docs/0.12/quickstart/
# https://www.flaskapi.org/

from flask import request
from flask_api import FlaskAPI
# You need database_helper.py in the same directory
from database_helper import DatabaseHelper

app = FlaskAPI(__name__)

@app.route('/api/register', methods=['POST'])
def register():
  try:
    email = request.data.get("email")
    password = request.data.get("password")
    firstname = request.data.get("firstname")
    lastname = request.data.get("lastname")
    helper = DatabaseHelper()
    return helper.register(email, password, firstname, lastname)
  except Exception as e:
    return "API Error\n" + e.message

@app.route('/api/login', methods=['POST'])
def login():
  try:
    email = request.data.get("email")
    password = request.data.get("password")
    helper = DatabaseHelper()
    return helper.login(email, password)
  except Exception as e:
    return "API Error\n" + e.message

@app.route('/api/user', methods=['GET'])
def list_users():
  try:
    access_token = request.args.get('accessToken')
    helper = DatabaseHelper()
    return helper.list_users(access_token)
  except Exception as e:
    return "API Error\n" + e.message

@app.route('/api/project', methods=['POST'])
def create_project():
  try:
    owner_id = request.data.get("owner_id")
    name = request.data.get("name")
    description = request.data.get("description")
    due_date = request.data.get("due_date")
    helper = DatabaseHelper()
    return helper.create_project(owner_id, name, description, due_date)
  except Exception as e:
    return "API Error\n" + e.message

@app.route('/api/project/<int:id>', methods=['GET'])
def get_project(id):
  try:
    access_token = request.args.get('accessToken')
    helper = DatabaseHelper()
    return helper.get_project(id, access_token)
  except Exception as e:
    return "API Error\n" + e.message

@app.route('/api/project/<int:id>', methods=['DELETE'])
def delete_project(id):
  try:
    access_token = request.args.get('accessToken')
    helper = DatabaseHelper()
    return helper.delete_project(id, access_token)
  except Exception as e:
    return "API Error\n" + e.message

if __name__ == "__main__":
    app.run(debug=True)
