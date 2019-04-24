import json
import subprocess

# TODO: turn into command-line parameters
envname = "dan"
region = "eu-central-1"

print "Deleting load balancers"
j = json.loads(subprocess.check_output(["aws", "elbv2", "describe-load-balancers", "--region", region]))
for lb in j["LoadBalancers"]:
	if lb["LoadBalancerName"] == envname + "-ssh-lb" or lb["LoadBalancerName"] == envname + "-tcp-lb" or lb["LoadBalancerName"] == envname + "-web-lb":
		subprocess.call(['aws', 'elbv2', 'delete-load-balancer', '--load-balancer-arn', lb["LoadBalancerArn"], "--region", region])

print "Deleting load balancer target groups"
j = json.loads(subprocess.check_output(["aws", "elbv2", "describe-target-groups", "--region", region]))
for tg in j["TargetGroups"]:
	if tg["TargetGroupName"] == envname + "-ssh-tg" or tg["TargetGroupName"].startswith(envname + "-tcp-tg-") or tg["TargetGroupName"].startswith(envname + "-web-tg-"):
		subprocess.call(['aws', 'elbv2', 'delete-target-group', '--target-group-arn', tg["TargetGroupArn"], "--region", region])

print "Deleting nat gateways"
j = json.loads(subprocess.check_output(["aws", "ec2", "describe-nat-gateways", "--filter", "Name=tag:Environment,Values=" + envname, "--region", region]))
for nat in j["NatGateways"]:
	if nat["State"] != "deleted":
		for nataddr in nat["NatGatewayAddresses"]:
			subprocess.call(['aws', 'ec2', 'release-address', '--allocation-id', nataddr["AllocationId"], "--region", region])
		subprocess.call(['aws', 'ec2', 'delete-nat-gateway', '--nat-gateway-id', nat["NatGatewayId"], "--region", region])

print "Deleting addresses"
j = json.loads(subprocess.check_output(["aws", "ec2", "describe-addresses", "--filters", "Name=tag:Environment,Values=" + envname, "--region", region]))
for addr in j["Addresses"]:
	if "AssociationId" in addr:
		subprocess.call(['aws', 'ec2', 'disassociate-address', '--association-id', addr["AssociationId"], "--region", region])
	subprocess.call(['aws', 'ec2', 'release-address', '--allocation-id', addr["AllocationId"], "--region", region])

print "Deleting internet gateways"
j = json.loads(subprocess.check_output(["aws", "ec2", "describe-internet-gateways", "--filters", "Name=tag:Environment,Values=" + envname, "--region", region]))
for subnet in j["InternetGateways"]:
	for attachment in subnet["Attachments"]:
		subprocess.call(['aws', 'ec2', 'detach-internet-gateway', '--internet-gateway-id', subnet["InternetGatewayId"], "--vpc-id", attachment["VpcId"], "--region", region])
	subprocess.call(['aws', 'ec2', 'delete-internet-gateway', '--internet-gateway-id', subnet["InternetGatewayId"], "--region", region])

print "Deleting security groups"
j = json.loads(subprocess.check_output(["aws", "ec2", "describe-security-groups", "--filters", "Name=tag:Environment,Values=" + envname, "--region", region]))
for subnet in j["SecurityGroups"]:
	subprocess.call(['aws', 'ec2', 'delete-security-group', '--group-id', subnet["GroupId"], "--region", region])

print "Deleting key pairs"
j = json.loads(subprocess.check_output(["aws", "ec2", "describe-key-pairs", "--region", region]))
for keypair in j["KeyPairs"]:
	if keypair["KeyName"] == envname + "-ops-manager-key":
		subprocess.call(['aws', 'ec2', 'delete-key-pair', '--key-name', keypair["KeyName"], "--region", region])
j = json.loads(subprocess.check_output(["aws", "kms", "list-aliases", "--region", region]))
for keypair in j["Aliases"]:
	if keypair["AliasName"] == "alias/" + envname:
		subprocess.call(['aws', 'kms', 'delete-alias', '--alias-name', keypair["AliasName"], "--region", region])

print "Deleting IAM users"
j = json.loads(subprocess.check_output(["aws", "iam", "list-users", "--region", region]))
for user in j["Users"]:
	if user["UserName"] == envname + "_om_user":
		j2 = json.loads(subprocess.check_output(["aws", "iam", "list-attached-user-policies", "--user-name", user["UserName"],"--region", region]))
		for policy in j2["AttachedPolicies"]:
			subprocess.call(['aws', 'iam', 'detach-user-policy', '--user-name', user["UserName"], "--policy-arn", policy["PolicyArn"], "--region", region])
		j2 = json.loads(subprocess.check_output(["aws", "iam", "list-access-keys", "--user-name", user["UserName"], "--region", region]))
		if "AccessKeyMetadata" in j2:
			for metadata in j2["AccessKeyMetadata"]:
				subprocess.call(['aws', 'iam', 'delete-access-key', "--user-name", user["UserName"], "--access-key-id", metadata["AccessKeyId"], "--region", region])
		subprocess.call(['aws', 'iam', 'delete-user', '--user-name', user["UserName"], "--region", region])

print "Deleting IAM roles"
j = json.loads(subprocess.check_output(["aws", "iam", "list-roles", "--region", region]))
for role in j["Roles"]:
	if role["RoleName"] == envname + "_om_role" or role["RoleName"] == envname + "_pas_bucket_access":
		j2 = json.loads(subprocess.check_output(["aws", "iam", "list-attached-role-policies", "--role-name", role["RoleName"],"--region", region]))
		for policy in j2["AttachedPolicies"]:
			subprocess.call(['aws', 'iam', 'detach-role-policy', '--role-name', role["RoleName"], "--policy-arn", policy["PolicyArn"], "--region", region])
		j2 = json.loads(subprocess.check_output(["aws", "iam", "list-instance-profiles-for-role", "--role-name", role["RoleName"],"--region", region]))
		for ip in j2["InstanceProfiles"]:
			subprocess.call(['aws', 'iam', 'remove-role-from-instance-profile', '--role-name', role["RoleName"], "--instance-profile-name", ip["InstanceProfileName"], "--region", region])
		j2 = json.loads(subprocess.check_output(["aws", "iam", "list-role-policies", "--role-name", role["RoleName"],"--region", region]))
		for policy in j2["PolicyNames"]:
			subprocess.call(['aws', 'iam', 'delete-role-policy', '--role-name', role["RoleName"], "--policy-name", policy, "--region", region])
		subprocess.call(['aws', 'iam', 'delete-role', '--role-name', role["RoleName"], "--region", region])

print "Deleting IAM instance profiles"
j = json.loads(subprocess.check_output(["aws", "iam", "list-instance-profiles", "--region", region]))
for ip in j["InstanceProfiles"]:
	if ip["InstanceProfileName"] == envname + "_ops_manager" or ip["InstanceProfileName"] == envname + "_pas_bucket_access":
		subprocess.call(['aws', 'iam', 'delete-instance-profile', '--instance-profile-name', ip["InstanceProfileName"], "--region", region])

print "Deleting IAM policies"
j = json.loads(subprocess.check_output(["aws", "iam", "list-policies", "--region", region]))
for policy in j["Policies"]:
	if policy["PolicyName"] == envname + "_ert" or policy["PolicyName"] == envname + "_ops_manager_role" or policy["PolicyName"] == envname + "_ops_manager_user":
		subprocess.call(['aws', 'iam', 'delete-policy', '--policy-arn', policy["Arn"], "--region", region])

print "Deleting VPCs"
j = json.loads(subprocess.check_output(["aws", "ec2", "describe-vpcs", "--filters", "Name=tag:Environment,Values=" + envname, "--region", region]))
for subnet in j["Vpcs"]:
	j2 = json.loads(subprocess.check_output(["aws", "ec2", "describe-subnets", "--filters", "Name=vpc-id,Values=" + subnet["VpcId"], "--region", region]))
	for subnet in j2["Subnets"]:
		subprocess.call(['aws', 'ec2', 'delete-subnet', '--subnet-id', subnet["SubnetId"], "--region", region])
	j2 = json.loads(subprocess.check_output(["aws", "ec2", "describe-route-tables", "--filters", "Name=vpc-id,Values=" + subnet["VpcId"], "--region", region]))
	for rt in j2["RouteTables"]:
		subprocess.call(['aws', 'ec2', 'delete-route-table', '--route-table-id', rt["RouteTableId"], "--region", region])
	subprocess.call(['aws', 'ec2', 'delete-vpc', '--vpc-id', subnet["VpcId"], "--region", region])
