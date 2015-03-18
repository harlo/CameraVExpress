#! /bin/bash
THIS_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
MIME_TYPE=$(file $1)
echo $MIME_TYPE | grep "data"

if ([ $? -eq 0 ]); then
	python $THIS_DIR/camerav_express.py "$MIME_TYPE" $1
	if ([ $? -eq 0 ]); then
		echo "SUCCESS!"
	fi
fi