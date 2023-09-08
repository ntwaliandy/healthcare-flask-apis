import uuid
from flask import jsonify, request
from dbhelper import Database as DB
from random import randint
from datetime import datetime




class Doctor:
    def __init__(self):
        print("::::::::: doctor instance :::::::")


    def create_doctor_profile():
        try:
            _json = request.json
            _doctorID = str(uuid.uuid4())
            _userID = _json['user_id']
            _fullName = _json['full_name']
            _dateOfBirth = _json['date_of_birth']
            _phoneNumber = _json['phone_number']
            _location = _json['location']

            # check if doctor exists
            check_user = check_user_existing(_userID)
            if len(check_user) <= 0:
                response = make_response(403, "user doesn't exist", "null")
                return response

            check_doctor = check_doctor_existing(_userID)
            if len(check_doctor) > 0:
                response = make_response(403, "doctor already exists", "null")
                return response

            doctor_dict = {"user_id": _userID, "doctor_id": _doctorID, "full_name": _fullName, "date_of_birth": _dateOfBirth, "phone_number": _phoneNumber, "location": _location}
            
            add_data = DB().insert('healthcare.doctor', **doctor_dict)

            response = make_response(100, "success", doctor_dict)
            return response

        except Exception as e:
            print(str(e))
            response = make_response(403, "failed to create profile", "null")
            return response






def make_response(status, message, data):
    data = jsonify({"status": status, "message": message, "data": data})
    return data


# check user existing function
def check_user_existing(userID):
    sql = "SELECT * FROM healthcare.user WHERE user_id = '" + str(userID) + "' AND role = 'doctor'"
    data = DB().select(sql)
    return data


# check user existing function
def check_doctor_existing(userID):
    sql = "SELECT * FROM healthcare.doctor WHERE user_id = '" + str(userID) + "'"
    data = DB().select(sql)
    return data