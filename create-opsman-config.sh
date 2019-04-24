#!/bin/bash
apt-get update
apt-get install -y python3
python platform_automation_test/parse-terraform-output.py terraform-output/terraform.1.0.0.out > opsman-output/opsman-config-1.0.0.yml
find .