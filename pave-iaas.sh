#!/bin/bash

find .
cp terraform-tfvars-s3/terraform-1.0.3.tfvars terraforming-aws/terraforming-pas/terraform.tfvars
cd terraforming-aws/terraforming-pas

#touch ../../terraform-output/terraform.1.0.0.out

#date >>  ../../terraform-output/terraform.1.0.0.out
echo "Performing terraform init"
terraform init -input=false
echo "Performing terraform apply"
terraform apply -input=false -auto-approve -state=../../terraform-output/terraform.1.0.0.out