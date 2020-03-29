```
curl -XPOST localhost:5000/roles -d '{"EndTime": "2020-03-16T21:34:30", "Principal": {"Type": "Service", "Name": "trustedadvisor.amazonaws.com"},"PermissionDocument": {"Version": "2012-10-17","Statement": [{"Effect": "Allow","NotAction": ["iam:*"], "Resource": "*"}]}, "Requester": "phil"}'
```
