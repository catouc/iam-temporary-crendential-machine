from role import Role
from policy import Policy


class RoleManager:
    def __init__(self, role_manager_id, requester, principal, permission_doc, end_time):
        print(f"Initialised role manager {role_manager_id}")
        self.id = role_manager_id
        self.requester = requester
        self.principal = principal
        self.permission_doc = permission_doc
        self.end_time = end_time
        self.role, self.policy = self.create_role()

    def create_role(self):
        print(f"Creating role {self.id}")
        role = Role(self.id, self.requester, self.principal, self.end_time)
        policy = Policy(self.id, self.permission_doc, self.requester)
        role.attach_role_policy(policy.arn)
        return role, policy

    def delete_role(self):
        print(f"Deleting role {self.id}")
        # self.role.detach_role_policy(self.policy.arn)
        self.role.delete()
        self.policy.delete()
