from flask import Blueprint
from models.patient import Patient

bp_app = Blueprint('mod_patient', __name__)

# create profile
@bp_app.route('/create_profile', methods=['POST'])
def createProfile():
    data = Patient.create_patient_profile()
    return data


# edit profile
@bp_app.route('/edit_profile', methods=['PUT'])
def editProfile():
    data = Patient.edit_profile()
    return data