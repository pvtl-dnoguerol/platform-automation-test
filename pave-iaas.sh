#!/bin/bash

find .
cp terraform-tfvars-s3/terraform-1.0.0.tfvars terraforming-aws/terraforming-pas/terraform.tfvars
cd terraforming-aws/terraforming-pas
terraform init -input=false
terraform apply -input=false