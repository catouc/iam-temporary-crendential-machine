
from flask import Flask
from flask_restful import Api

from api import RoleAPI, RolesAPI

app = Flask(__name__)
api = Api(app)

api.add_resource(RoleAPI, "/role/<role_id>")
api.add_resource(RolesAPI, "/roles")

if __name__ == "__main__":
    app.run(debug=True)

