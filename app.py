from urllib import request

from flask import Flask, request, jsonify, Response, make_response
from database import db
from models.user import User
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id: int) -> User:
    """
    Load user by ID from the database.
    Args:
        user_id (int): User ID
    Returns:
        User: User object
    """
    return User.query.get(user_id)


@app.route('/login/', methods=['POST'])
def login() -> Response:
    """
    Login route for the user to authenticate.
    Returns:
        Response: Message with the status of the authentication
            """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return make_response(jsonify({'message': 'User authenticated successfully'}))
    return make_response(jsonify({'message': 'Invalid credentials'}), 400)


@app.route('/logout', methods=['GET'])
@login_required
def logout() -> Response:
    """
    Logout route for the user to de-authenticate.
    Returns:
        Response: Message with the status of the de-authentication
    """
    logout_user()
    return make_response(jsonify({'message': 'User logged out successfully'}))


@app.route('/user', methods=['POST'])
def create_user():
    """
    Create a new user.
    Returns:
        Response: Message with the status of the user creation
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({'message': 'User created successfully'}))
    return make_response(jsonify({'message': 'Invalid data'}), 400)

if __name__ == '__main__':
    app.run(debug=True)
