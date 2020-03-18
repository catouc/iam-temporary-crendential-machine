import boto3


SESSION = boto3.Session()
IAM = SESSION.resource("iam")
CLIENT = SESSION.client("iam")


class Role:
    def __init__(self, role_id, requester, end_time):
        self.id = role_id
        self.requester = requester
        self.end_time = end_time
        self.create()

    def create(self):
        resp = CLIENT.create_role(
            RoleName=self.id,
            AssumeRolePolicyDocument=generate_assume_role_doc(self.requester),
            Description=f"Requested by {self.requester}",
            Tags=[
                {"Key": "Name", "Value": self.id},
                {"Key": "Requester", "Value": self.requester},
                {"Key": "EndTime", "Value": self.end_time},
            ],
        )
        return resp

    def delete(self):
        # This won't handle the detaching of policies at the moment
        role = IAM.Role(self.id)
        resp = role.delete()
        return resp

    def attach_role_policy(self, policy_arn):
        role = IAM.Role(self.id)
        resp = role.attach_policy(PolicyArn=policy_arn)
        return resp

    def detach_role_policy(self, policy_arn):
        role = IAM.Role(self.id)
        resp = role.detach_policy(PolicyArn=policy_arn)
        return resp


def generate_assume_role_doc(requester):
    pol = """{
       "Version": "2012-10-17",
       "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
       ]
    }
    """
    return pol
