import json
import sys

print "---"
print "opsman-configuration:"
print "  aws:"

with open(sys.argv[1]) as json_file:
	data = json.load(json_file)
	for module in data['modules']:
		if len(module['path']) == 1 and module['path'][0] == 'root':
			print "    access_key_id: " + data['modules'][0]['outputs']['ops_manager_iam_user_access_key']['value']
			print "    secret_access_key: " + data['modules'][0]['outputs']['ops_manager_iam_user_secret_key']['value']
			print "    region: " + data['modules'][0]['outputs']['region']['value']	
			print "    vpc_subnet_id: " + data['modules'][0]['outputs']['infrastructure_subnet_ids']['value'][0]		
			ip = data['modules'][0]['outputs']['infrastructure_subnet_cidrs']['value'][0].split('.')
			print "    private_ip: " + ip[0] + '.' + ip[1] + '.' + ip[2] + '.2'
		if len(module['path']) == 2 and module['path'][1] == 'ops_manager':
			print "    security_group_id: " + module['outputs']['security_group_id']['value']
			print "    key_pair_name: " + module['outputs']['ssh_public_key_name']['value']
			print "    iam_instance_profile_name: " + module['outputs']['ops_manager_iam_instance_profile_name']['value']
			print "    public_ip: " + module['outputs']['public_ip']['value']
	print "    instance_type: m5.large"
	print "    boot_disk_size: 200"
	