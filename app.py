from flask import Flask, request, jsonify , make_response#to make HTTP requests and responses and to use data in json format
from flasksqlalchemy import SQLAlchemy #helps to create and manage the database
from os import environ #to access environment variables

app = Flask(__name__) #create an instance of the Flask class
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app) #create an instance of the SQLAlchemy class

class User(db.Model): #create a class that inherits from db.Model
    __tablename__ = 'users' #name of the table in the database
    
    id = db.Column(db.Integer, primary_key=True) #primary key of the table
    name = db.Column(db.String(50), nullable=False) #name of the user,
    email = db.Column(db.String(120), unique=True, nullable=False) #email of the user, must be unique and cannot be null
    
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }      
    
db.create_all() #create the tables in the database

#create a test route
@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'API is working!'}), 200)

#create a user
@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()  # Get the JSON data from the request
        new_user = User(name=data['name'], email=data['email'])  # Create a new User instance
        db.session.add(new_user)  # Add the new user to the session
        db.session.commit()  # Commit the session to save the user to the database
        return make_response(jsonify(new_user.json()), 201)  # Return the created user as JSON with a 201 status code
    
    except e:
        return make_response(jsonify({'error': str(e)}), 400)

#get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()  # Query all users from the database
        return make_response(jsonify([user.json() for user in users]), 200)  # Return the list of users as JSON with a 200 status code
    
    except e:
        return make_response(jsonify({'error': str(e)}), 400)

#get a user by id
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()  # Get the user by ID or return a 404 error if not found
        return make_response(jsonify(user.json()), 200)  # Return the user as JSON with a 200 status code
    
    except e:
        return make_response(jsonify({'error': str(e)}), 400)

#update a user
@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()  # Get the JSON data from the request
        user = User.query.filter_by(id=id).first()  # Get the user by ID or return a 404 error if not found
        
        user.name = data['name']  # Update the user's name
        user.email = data['email']  # Update the user's email
        db.session.commit()  # Commit the session to save the changes
        
        return make_response(jsonify(user.json()), 200)  # Return the updated user as JSON with a 200 status code
    
    except e:
        return make_response(jsonify({'error': str(e)}), 400)