#!/bin/bash

find .
cd terraforming-aws/terraforming-pas
cp ../../terraform-tfvars-s3/terraform.tfvars .
terraform init -input=false
terraform apply -input=false