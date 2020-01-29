#!/bin/bash

virtualenv venv -p python3
echo "Virtualenv venv is created!"
source venv/bin/activate
echo "Virtualenv venv is up!"
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Creating MongoDB container for Docker..."
sudo docker run -d -p 27019:27019 --name mongodb mongo --bind_ip_all

