from flask import Blueprint
from models.user import User

bp_app = Blueprint('mod_user', __name__)

# user register
@bp_app.route('/user_register', methods=['POST'])
def regUser():
    data = User.UserRegister()
    return data


# getting all client users
@bp_app.route('/all_users', methods=['GET'])
def getAllClients():
    data = User.getClientUsers()
    return data

# user log in
@bp_app.route('/user_login', methods=['POST'])
def loginUser():
    data = User.userLogin()
    return data

# user update details
@bp_app.route('/user_update', methods=['POST'])
def updateUser():
    data = User.userUpdate()
    return data

# password update
@bp_app.route('/password_update', methods=['POST'])
def passUpdate():
    data = User.updatePass()
    return data

# user by userID
@bp_app.route('/user_by_id', methods=['POST'])
def userByID():
    data = User.getUserbyID()
    return data