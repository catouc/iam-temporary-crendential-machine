import boto3

SESSION = boto3.Session()
IAM = SESSION.resource("iam")
CLIENT = SESSION.client("iam")


class Policy:
    def __init__(self, pol_id, permission_document, requester):
        self.id = pol_id
        self.permission_document = permission_document
        self.requester = requester
        pol = self.create()
        self.arn = pol["Policy"]["Arn"]

    def create(self):
        resp = CLIENT.create_policy(
            PolicyName=self.id,
            PolicyDocument=self.permission_document,
            Description=f"Requested by {self.requester}",
        )
        return resp

    def delete(self):
        policy = IAM.Policy(self.arn)
        for role in policy.attached_roles.all():
            policy.detach_role(RoleName=role.name)
        resp = policy.delete()
        return resp
