#!/usr/bin/env bash

# Setup virtualenv, install packages necessary to run BibOS Admin.
# System requirements, installed packages etc. are checked 
# in a separate dependencies file. 

if [ -z $BIBOS_VIRTUAL_ENV ]
then

    if [ -z `which virtualenv` ]
    then
        apt-get update
        apt-get install -y python3-venv
    fi

    DIR=$(pwd)
    DIR=$(dirname "${DIR}")
    echo $DIR
    BIBOS_VIRTUAL_ENV=${DIR}/python-env
fi

if [ -e ${BIBOS_VIRTUAL_ENV}/bin/activate ]
then
    echo "virtual environment already installed" 1>&2
    exit
fi

rm -rf $BIBOS_VIRTUAL_ENV
python3 -m venv $BIBOS_VIRTUAL_ENV
source $BIBOS_VIRTUAL_ENV/bin/activate

DIR=$(dirname ${BASH_SOURCE[0]})
PYTHON_PACKAGES=$(cat "$DIR/PYTHON_DEPENDENCIES")

for  package in "${PYTHON_PACKAGES[@]}"
do
    pip3 install $package

    RETVAL=$?
    if [ $RETVAL -ne 0 ]; then
        echo "" 1>&2
        echo "ERROR: Unable to install Python package <$package>." 1>&2
        echo -n "Please check your network connection. " 1>&2
        echo "A remote server may be down - please retry later. " 1>&2
        echo "" 1>&2
        exit -1
    fi
done
