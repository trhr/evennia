#!/bin/bash
cd /home/ec2-user/evennia/
pip3 install --upgrade -r requirements.txt
echo "The Evennia AfterInstall deployment lifecycle event successfully completed." > /tmp/deploy/after-install.txt


