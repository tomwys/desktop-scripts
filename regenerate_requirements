#!/bin/bash -e

BASE_REQUIREMENTS="$1"
BASE_REQUIREMENTS="${BASE_REQUIREMENTS:-base_requirements.txt}"

if [ ! -f "$BASE_REQUIREMENTS" ] ; then
    echo $BASE_REQUIREMENTS file not found!
    exit 1
fi

OUTPUT_DIRECTORY=$(dirname "$BASE_REQUIREMENTS")
OUTPUT_FILE="$OUTPUT_DIRECTORY/requirements.txt"
VENV_DIR=$(mktemp -d -u)

virtualenv -p /usr/bin/python2.7 "$VENV_DIR"
"$VENV_DIR"/bin/pip install -r "$BASE_REQUIREMENTS"
"$VENV_DIR"/bin/pip freeze >"$OUTPUT_FILE"
rm -r "$VENV_DIR"
echo $OUTPUT_FILE regenerated.
