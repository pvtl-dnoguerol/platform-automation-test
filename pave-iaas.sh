#!/bin/bash

find .
cp terraform-tfvars-s3/terraform-1.0.3.tfvars terraforming-aws/terraforming-pas/terraform.tfvars
cd terraforming-aws/terraforming-pas
echo "Performing terraform init"
terraform init -input=false
echo "Performing terraform apply"
terraform apply -input=false -auto-approve > ../../terraform-output/terraform.out