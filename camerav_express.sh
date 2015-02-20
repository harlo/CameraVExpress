#! /bin/bash

MIME_TYPE=$(file $1)
echo $MIME_TYPE | grep "data"

if ([ $? -eq 0 ]); then
	python camerav_express.py "$MIME_TYPE" $1
	if ([ $? -eq 0 ]); then
		echo "SUCCESS!  Data exported to $1.json"
	fi
fi