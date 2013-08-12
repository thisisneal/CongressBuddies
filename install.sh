#!/bin/bash
#OS=$(uname -a)

#if echo $OS | grep -i "ubuntu" >> /dev/null ; then
#    echo "Is Ubuntu"
#fi

git pull
rsync -avz --delete --delete-excluded --exclude *.xml govtrack.us::govtrackdata/congress/113/votes .
sudo pip install pyyaml
sudo pip install tornado

