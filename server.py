from flask_app.controllers import login_and_registration
from flask_app.controllers import cars_new
from flask_app.controllers import cars_view
from flask_app.controllers import cars_edit
from flask_app.controllers import purchases

from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)
