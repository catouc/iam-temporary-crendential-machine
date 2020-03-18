from role import Role
from policy import Policy


class RoleManager:
    def __init__(self, role_manager_id, requester, permission_doc, end_time):
        self.id = role_manager_id
        self.requester = requester
        self.permission_doc = permission_doc
        self.end_time = end_time
        self.role, self.policy = self.create_role()

    def create_role(self):
        role = Role(self.id, self.requester, self.end_time)
        policy = Policy(self.id, self.permission_doc, self.requester)
        role.attach_role_policy(policy.arn)
        return role, policy

    def delete_role(self):
        self.role.detach_role_policy(self.policy.arn)
        self.policy.delete()
        self.role.delete()
