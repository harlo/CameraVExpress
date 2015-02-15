#! /bin/bash

MEDIA_TYPE="None"
MIME_TYPE=$(file $1)
echo $MIME_TYPE | grep "JPEG image data"

if ([ $? -eq 0 ]); then
	MEDIA_TYPE="image"
fi

python camerav_express.py $MEDIA_TYPE $1 $2