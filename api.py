from flask import request
from flask_restful import Resource

access_list = {}

class Access(Resource):

    def get(self, access_id):
        return access_list[access_id]

    def delete(self, access_id):
        del access_list[access_id]
        return '', 204


class AccessList(Resource):

    def get(self):
        return access_list

    def post(self):
        json_data = request.get_json(force=True)
        access_id = generate_acccess_id()
        access = {
            "scope": json_data["scope"],
            "principal": json_data["principal"],
            "timeout": json_data["timeout"]
        }
        access_list[access_id] = access
        return access, 201


def generate_acccess_id():
    return len(access_list)
