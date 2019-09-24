## Environment setup:
We use python3 for this project.

You can choose to use virtual environment or use anaconda to manage your environments. 
Then at root directory (``/PostDisasterSol``), run:
``pip3 install -e .``

## Database init:
(The sqplite3 database will be stored in var/. If it is currently in your directory, you can manually delete it or simply leave it there.)  
Run ``python3 var/init_db.py``  
Then you can run ``python3 var/insert.py`` to add some examples into the database.

## To run the web app: 
At root directory (``/PostDisasterSol``), run:

$ export FLASK_APP=PDPlatform  

$ export PDPlatform_SETTINGS=config.py  

To test on local lost:
$ export FLASK_DEBUG=True  

$ flask run --host localhost --port 8000  

To test on IBM cloud service
$ export FLASK_DEBUG=False

$ flask run --host 0.0.0.0 --port 8000  
