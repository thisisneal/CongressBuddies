#!/bin/bash
if [ ${#@} -eq 1 ]; then
    echo http://www.govtrack.us/data/photos/$1.jpeg
else
    echo "Usage: ./getPhotos.sh [idnumber]"
fi
