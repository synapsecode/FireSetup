# #!/usr/bin/env bash
# This Variable contains the directory that this bash file is stored in
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# Link to the firesetup python script
SCRIPT_PATH=$SCRIPT_DIR/firesetup.py
# Get the current directory from where script gets invoked
CURDIR=$(pwd)
# Run the python script ($* just forwards the other arguements that have been passed)
python3 $SCRIPT_PATH $SCRIPT_DIR $CURDIR $*


# python3 $SCRIPT_PATH $SCRIPT_DIR "/Volumes/ExternalSSD/Programming/Flutter/xc" $*