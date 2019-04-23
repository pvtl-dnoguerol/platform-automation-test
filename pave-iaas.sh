#!/bin/bash

find .
cp terraform-tfvars-s3/terraform-1.0.1.tfvars terraforming-aws/terraforming-pas/terraform.tfvars
cd terraforming-aws/terraforming-pas
echo "Performing terraform init\n"
terraform init -input=false
echo "Performing terraform apply\n"
terraform apply -input=false -auto-approve > ../../build-output/terraform.out