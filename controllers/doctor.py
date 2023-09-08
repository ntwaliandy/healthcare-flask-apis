from flask import Blueprint
from models.doctor import Doctor

bp_app = Blueprint('mod_doctor', __name__)

# create profile
@bp_app.route('/create_profile', methods=['POST'])
def createProfile():
    data = Doctor.create_doctor_profile()
    return data