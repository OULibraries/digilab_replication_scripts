#!/bin/bash

MYFILE=$1
MYPATH=$2
SYNCDEST=$3

mkdir -p "${SYNCDEST}/${MYPATH}" && cp --no-clobber "${MYPATH}/${MYFILE}" "${SYNCDEST}/${MYPATH}/${MYFILE}"
