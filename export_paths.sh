#!/bin/sh
# This script will export the pythonpath. Please source this file before starting the application.

export PYTHONPATH=$PYTHONPATH:$(pwd)/src
export CONFROOT=$(pwd)/etc
echo $PYTHONPATH
echo $CONFROOT
