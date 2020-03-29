import boto3


SESSION = boto3.Session()
IAM = SESSION.resource("iam")
CLIENT = SESSION.client("iam")


class Role:
    def __init__(self, role_id, requester, principal, end_time):
        self.id = role_id
        self.requester = requester
        self.principal = principal
        self.end_time = end_time
        self.create()

    def create(self):
        resp = CLIENT.create_role(
            RoleName=self.id,
            AssumeRolePolicyDocument=generate_assume_role_doc(self.principal),
            Description=f"Requested by {self.requester}",
            Tags=[
                {"Key": "Name", "Value": self.id},
                {"Key": "Requester", "Value": self.requester},
                {"Key": "EndTime", "Value": self.end_time},
            ],
        )
        return resp

    def delete(self):
        role = IAM.Role(self.id)
        for pol in role.attached_policies.all():
            pol.detach_role(RoleName=role.name)
        resp = role.delete()
        return resp

    def attach_role_policy(self, policy_arn):
        role = IAM.Role(self.id)
        resp = role.attach_policy(PolicyArn=policy_arn)
        return resp


def generate_assume_role_doc(principal):
    pol = """{
       "Version": "2012-10-17",
       "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "%s": "%s"
            },
            "Action": "sts:AssumeRole"
        }
       ]
    }
    """ % (
        principal["Type"],
        principal["Name"],
    )
    return pol
