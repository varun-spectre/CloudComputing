#!/bin/bash
cd /home/ubuntu/Cloud_computing_546

# Pull the latest changes from your git repository
GIT_TOKEN=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
git config --global credential.helper store
git config --global user.email "smunagan@asu.edu"
git config --global user.name "sivamunaganuru"
git stash
git pull

# Restart your classify.py service
sudo systemctl restart classify.service

# [Unit]
# Description=Git pull on startup
# After=network.target

# [Service]
# Type=simple
# User=ubuntu
# WorkingDirectory=/home/ubuntu
# ExecStart=/home/ubuntu/Cloud_computing_546/project_1/app-tier/git-pull.sh

# [Install]
# WantedBy=multi-user.target
