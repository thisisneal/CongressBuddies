CongressBuddies
===============

Downloading Vote Data
---------------------
Command to download 2013 vote records from govtrack:
rsync -avz --delete --delete-excluded --exclude *.xml govtrack.us::govtrackdata/congress/113/votes .

Dependencies
------------
PyYAML : http://pyyaml.org/
- sudo python setup.py install

Tornado :
- pip install tornado

How to Run
----------
- python WebUI.py
- Open http://localhost:8888

Description
-----------
See who likes who in congress!
