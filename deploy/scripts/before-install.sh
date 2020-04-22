#!/bin/bash
export FOLDER=/tmp/deploy/
export EVENNIA_DIR=/home/ec2-user/evennia/

if [ -d $FOLDER ]
then
 rm -rf $FOLDER
fi

mkdir -p $FOLDER

service evennia stop

if [ -d $FOLDER ]
then
  rm -rf $FOLDER
fi

mkdir -p $EVENNIA_DIR
