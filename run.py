from application import application
from flask_cors import CORS
from controllers.user import bp_app as user_mod
from controllers.doctor import bp_app as doctor_mod
from controllers.patient import bp_app as patient_mod

application.register_blueprint(user_mod, url_prefix="/user")
application.register_blueprint(doctor_mod, url_prefix="/doctor")
application.register_blueprint(patient_mod, url_prefix="/patient")

cors = CORS(application)
application.run(port=9000, host="0.0.0.0", debug=True)