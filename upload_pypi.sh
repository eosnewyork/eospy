#!/bin/bash

if [ "$1" == "" ]; then
    echo Need to pass a version number.
    exit 1
fi

export BUILD_VERSION=$1

# setup
python setup.py sdist
# test upload
twine upload dist/*${BUILD_VERSION}*