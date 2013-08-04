#!/bin/bash
if [ ${#@} -eq 1 ]; then
    ID=$1
    if [[ 300001 -le $ID && $ID -le 412585 ]]; then 
        wget http://www.govtrack.us/data/photos/${ID}.jpeg -O ${ID}.jpeg
    else
        echo "Not in range"
    fi
else
    echo "Usage: ./getPhotos.sh [idnumber]"
fi
