import json
import uuid
import time

from datetime import datetime
from threading import Thread

from flask import request
from flask_restful import Resource

from role_manager import RoleManager

roles = []


class RoleAPI(Resource):
    def get(self, role_id):
        return roles[role_id]


class RolesAPI(Resource):
    def get(self):
        return roles

    def post(self):
        json_data = request.get_json(force=True)
        role_id = generate_acccess_id()
        role = {
            "id": role_id,
            "end_time": json_data["EndTime"],
            "requester": json_data["Requester"],
            "principal": json_data["Principal"],
            "permission_document": json.dumps(json_data["PermissionDocument"]),
        }
        thread = Thread(
            target=manage_role,
            args=[
                role["id"],
                role["end_time"],
                role["requester"],
                role["principal"],
                role["permission_document"],
            ],
        )
        thread.daemon = True
        thread.start()
        roles.append(role)
        return role, 201


def generate_acccess_id():
    return str(uuid.uuid4())


def manage_role(role_id, end_time, requester, principal, permission_doc):
    r = RoleManager(role_id, requester, principal, permission_doc, end_time)
    date_format = "%Y-%m-%dT%H:%M:%S"
    end_time = datetime.strptime(end_time, date_format)
    wait_time = end_time - datetime.utcnow()
    time.sleep(wait_time.total_seconds())
    r.delete_role()
