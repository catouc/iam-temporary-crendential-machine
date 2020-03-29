# Temporary IAM credential manager

A very small proof of concept for a service that will create temporary IAM roles and policies to lessen the need to give people permanent access to their AWS environments.

# How to use

The main interaction is currently done through a small flask API. It very simply exposes the REST model for a role object through the two endpoints:

* role/<role-id>
* roles

I'm to lazy to write a swagger doc or anything like that so here's the fields that are expected:

* Requester <str> 
* Principal <obj>
  * Type <str> (Either `AWS`, `Service` or `Federated` ... `Canonical` technically works but would not apply to anything)
  * Name <str> (String of either the full ARN for the `AWS` or the service url for `Service`)
* EndTime <str> (datetime string conform to https://tools.ietf.org/html/rfc3339#section-5.6 so YYYY-MM-DDTHH:MM:SS)
* PermissionDocument <obj> (a json string of the permission doc your role needs to have)

Here is an example curl request:

```
curl -XPOST localhost:5000/roles -d '{"EndTime": "2020-03-16T21:34:30", "Principal": {"Type": "Service", "Name": "trustedadvisor.amazonaws.com"},"PermissionDocument": {"Version": "2012-10-17","Statement": [{"Effect": "Allow","NotAction": ["iam:*"], "Resource": "*"}]}, "Requester": "phil"}'
```
