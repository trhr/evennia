#!/bin/bash
export FOLDER=/tmp/deploy/

if [ -d $FOLDER ]
then
 rm -rf $FOLDER
fi

mkdir -p $FOLDER
