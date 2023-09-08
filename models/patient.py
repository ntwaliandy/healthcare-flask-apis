import uuid
from flask import jsonify, request
from dbhelper import Database as DB
from random import randint
from datetime import datetime




class Patient:
    def __init__(self):
        print("::::::::: patient instance :::::::")


    def create_patient_profile():
        try:
            _json = request.json
            _patientID = str(uuid.uuid4())
            _userID = _json['user_id']
            _fullName = _json['full_name']
            _dateOfBirth = _json['date_of_birth']
            _phoneNumber = _json['phone_number']
            _location = _json['location']

            # check if user exists
            check_user = check_user_existing(_userID)
            if len(check_user) <= 0:
                response = make_response(403, "user doesn't exist", "null")
                return response

            # check if patient exists
            check_patient = check_patient_existing(_userID)
            if len(check_patient) > 0:
                response = make_response(403, "patient already exists", "null")
                return response

            patient_dict = {"user_id": _userID, "patient_id": _patientID, "full_name": _fullName, "date_of_birth": _dateOfBirth, "phone_number": _phoneNumber, "location": _location}
            
            add_data = DB().insert('healthcare.patient', **patient_dict)

            response = make_response(100, "success", patient_dict)
            return response

        except Exception as e:
            print(str(e))
            response = make_response(403, "failed to create profile", "null")
            return response


    def edit_profile():
        try:
            _json = request.json
            _userID = _json['user_id']
            _fullName = _json['full_name']
            _dateOfBirth = _json['date_of_birth']
            _phoneNumber = _json['phone_number']
            _location = _json['location']

            # check if user exists
            check_user = check_user_existing(_userID)
            if len(check_user) <= 0:
                response = make_response(403, "user doesn't exist", "null")
                return response

            # check if patient exists
            check_patient = check_patient_existing(_userID)
            if len(check_patient) <= 0:
                response = make_response(403, "patient doesn't exists", "null")
                return response

            patient_dict = {"full_name": _fullName, "date_of_birth": _dateOfBirth, "phone_number": _phoneNumber, "location": _location}

            update_data = DB().Update('healthcare.patient', "user_id  =  '" + str(_userID) + "'", **patient_dict)

            response = make_response(100, "success", check_patient[0])
            return response

        except Exception as e:
            print(str(e))
            response = make_response(403, "failed to update patient", "null")
            return response







def make_response(status, message, data):
    data = jsonify({"status": status, "message": message, "data": data})
    return data


# check user existing function
def check_user_existing(userID):
    sql = "SELECT * FROM healthcare.user WHERE user_id = '" + str(userID) + "' AND role = 'patient'"
    data = DB().select(sql)
    return data


# check patient existing function
def check_patient_existing(userID):
    sql = "SELECT * FROM healthcare.patient WHERE user_id = '" + str(userID) + "'"
    data = DB().select(sql)
    return data