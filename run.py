from application import application
from flask_cors import CORS


cors = CORS(application)
application.run(port=9000, host="0.0.0.0", debug=True)