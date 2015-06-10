#!/usr/bin/env bash

JSON_PATH=$HOME/.ipython/kernels/odpscmd
if [ ! -e $JSON_PATH/kernel.json ];
then
    mkdir -p $JSON_PATH
    cp kernel.json $JSON_PATH/
fi

export PYTHONPATH=`pwd`
ipython notebook
