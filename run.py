from application import application
from flask_cors import CORS
from controllers.user import bp_app as user_mod

application.register_blueprint(user_mod, url_prefix="/user")

cors = CORS(application)
application.run(port=9000, host="0.0.0.0", debug=True)