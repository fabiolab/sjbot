#!/bin/bash
source .env
source p3.7/bin/activate
pip install -r requirements.txt
nohup python -u ./sjbot_main.py > sjbot.log & 
