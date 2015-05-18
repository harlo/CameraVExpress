#! /bin/bash
THIS_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

python $THIS_DIR/camerav_express.py "$(file $1)" $2
if ([ $? -eq 0 ]); then
	echo "SUCCESS!"
fi
