#!/bin/bash

# Update system packages
sudo yum update -y

# Install Git
sudo yum install git -y

# Install Python3 and pip
sudo yum install python3-pip -y

# Add MongoDB repository
sudo tee /etc/yum.repos.d/mongodb-org-4.4.repo <<EOL
[mongodb-org-4.4]
name = MongoDB Repository
baseurl = https://repo.mongodb.org/yum/amazon/2/mongodb-org/4.4/x86_64/
gpgcheck=1
enabled=1
gpgkey = https://www.mongodb.org/static/pgp/server-4.4.asc
EOL

# Install MongoDB dependencies
sudo yum install mongodb-mongosh-shared-openssl3 -y
sudo yum install mongodb-org -y

# Start MongoDB
sudo systemctl start mongod --now

# Clone the repository to /home/ec2-user
sudo -u ec2-user git clone https://github.com/ashwin200026/Cloud_Project /home/ec2-user/Cloud_Project

# Change to the repository directory
cd /home/ec2-user/Cloud_Project

# Install Python dependencies
sudo pip install -r requirements.txt

# Change ownership to root user
sudo chown root /home/ec2-user/Cloud_Project/ -R

# Run the Python script
sudo python3 test.py

