import uuid
from flask import jsonify, request
from dbhelper import Database as DB
from random import randint
import hashlib
from datetime import datetime


class User:
    def __init__(self):
        print("******user model********")

    # registering a user
    @staticmethod
    def UserRegister():
        try:
            _json = request.json
            _username = _json['username']
            _email = _json['email']
            _role = _json["role"]
            _password = _json['password']
            _dateTime = datetime.now()
            _userID = str(uuid.uuid4())
            # checking if user exists
            check_user_exists = user_client_existing(_email, _username)
            if len(check_user_exists) > 0:
                response = make_response(403, "user already exists", "null")
                return response

            # hashing password
            hashed_password = hashlib.sha256(str(_password).encode('utf-8')).hexdigest()

            # generating an user_client otp
            generated_otp = randint(1000, 9999)

            user_dict = {"user_id": _userID, "username": _username, "email": _email, "role": _role, "password": hashed_password, "created_at": _dateTime}
            add_data = DB().insert('healthcare.user', **user_dict)

            print(":: insert data ::", add_data)

            # making response
            response = make_response(100, "user registered successfully", user_dict)
            return response

        except Exception as e:
            print(str(e))
            response = make_response(403, "failed to register user", "null")
            return response

    # get all users
    def getClientUsers():
        try:
            sql = "SELECT * FROM healthcare.user"
            data = DB().select(sql)
            if len(data) <= 0:
                response = make_response(403, "No registered client yet", "null")
            response = make_response(100, "success", data)
            return response

        except Exception as e:
            print(e)
            response = make_response(403, "failed to pull all users", "null")
            return response

    # user login
    def userLogin():
        try:
            _json = request.json
            _email = _json['email']
            _password = _json['password']

            # hashing password
            hashed_password = hashlib.sha256(str(_password).encode('utf-8')).hexdigest()

            # checking user
            check_user = user_client_login_existing(_email, str(hashed_password))
            
            if len(check_user) <= 0:
                response = make_response(403, "User doesn't exist", "null")
                return response


            response = make_response(100, "success", check_user[0])
            return response

        except Exception as e:
            print(e)
            response = make_response(403, "failed to logIn user", "null")
            return response

    # user update password
    def updatePass():
        try:
            _json = request.json
            _userId = _json['user_id']
            _oldPass = _json['old_pass']
            _newPass = _json['new_pass']
            _confirmPass = _json['confirm_pass']

            # hasing old password
            hashed_oldPassword = hashlib.sha256(str(_oldPass).encode('utf-8')).hexdigest()
            # checking user existing
            check_user = check_user_password(_userId, hashed_oldPassword)
            if len(check_user) <= 0:
                response = make_response(403, "user doesn't exist", "null")
                return response

            # checking if new pass equals to confirm pass
            if (_newPass != _confirmPass):
                response = make_response(403, "password mismatch", "null")
                return response

            # checking if new pass equals to old pass
            if (_oldPass == _newPass):
                response = make_response(403, "new password is similar to the old one", "null")
                return response

            # checking new password length
            if len(_newPass) <= 5:
                response = make_response(403, "new password is too short", "null")
                return response

            # hashing new password
            hashed_newPassword = hashlib.sha256(str(_newPass).encode('utf-8')).hexdigest()

            updated_dict = {"password": hashed_newPassword}

            DB().Update('healthcare.user', "id  =  '" + str(_userId) + "'", **updated_dict)

            response = make_response(100, "password updated successfully", check_user[0])
            return response

        except Exception as e:
            print(e)
            response = make_response(403, "failed to update password", "null")
            return response

    # user by userID
    def getUserbyID():
        try:
            _json = request.json
            _userID = _json['user_id']

            # checking if userID is valid
            check_userExist = checking_user_by_id(_userID)
            if len(check_userExist) <= 0:
                response = make_response(403, "Invalid User!")
                return response

            response = make_response(100, "success", check_userExist[0])
            return response

        except Exception as e:
            print(e)
            response = make_response(403, "failed to retrieve user", "null")
            return response



def make_response(status, message, data):
    data = jsonify({"status": status, "message": message, "data": data})
    return data

# check user existing function
def user_client_existing(user_email, username):
    sql = "SELECT * FROM healthcare.user WHERE email = '" + user_email + "' OR username = '" + username + "' "
    data = DB().select(sql)
    return data

#  check user client for login session
def user_client_login_existing(user_email, user_password):
    sql = "SELECT * FROM healthcare.user WHERE email = '" + user_email + "' AND password = '" + user_password + "' "
    data = DB().select(sql)
    return data

# check user by user id
def checking_user_by_id(userID):
    sql = "SELECT * FROM healthcare.user WHERE id = '" + str(userID) + "' "
    data = DB().select(sql)
    return data

# checking user password
def check_user_password(userID, userPass):
    sql = "SELECT * FROM healthcare.user WHERE id = '" + str(userID) + "' AND password = '" + str(userPass) + "' "
    data = DB().select(sql)
    return data

# customized response for userID
def checking_Cuser_by_id(userID):
    sql = "SELECT * FROM healthcare.user WHERE id = '" + str(userID) + "' "
    data = DB().select(sql)
    response = {
        "email": data[0]['email'],
        "username": data[0]['username'],
    }
    return response