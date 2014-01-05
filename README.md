CongressBuddies
===============

Description
-----------
See who likes who in congress!

Search for any US Representative or Senator, and CongressBuddies will display the 5 "most similar" congress members based on voting record as well as their respective states.

Downloading Vote Data
---------------------
Command to download 2013 vote records from govtrack:
    rsync -avz --delete --delete-excluded --exclude *.xml govtrack.us::govtrackdata/congress/113/votes .

Dependencies
------------
PyYAML
Tornado
    ./install.sh 

How to Run
----------
    python MakeAdjacencyMat.py
    python WebUI.py
Open http://localhost:8080
