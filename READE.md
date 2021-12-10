# Server-Tapper

Server-Tapper was designed to create network traffic to servers I own around the world for a study.
The code will automate a defined range attempts to push and pull a file a random amount of times with a random amount of time between the actions.
The code is designed to work on a Raspbery Pi that can run throughout a long period of time.
# To install all dependencies needed:

$ pip install -r requirements.txt

# Code Options

-a  -add        adds a server to the database

-c  -check      checks to see if a connection can be made to server

-d  -delete     deletes a server to the database 

-h  -help       brings up help screen

-i  -iterations change ranges and iterations

-l  -pull       will only pull files to your servers

-lf -pullf      change file you will be pulling

-om -messages   exports message table in database to a filename you define to txt file

-ol -logs       export logs table in database to a filename you define to a csv

-r  -run        runs entire code to push and pull files

-s  -push       will only push files to your servers

-sf -pushf      change file you want to push

-u  -update     updates a server in the database

# py_Files

server_tap.py is the main Python file which all other files will run through. 

## push.py and pull.py

### The push and pull Python files will first identify each server in the database. It will then do the following for each server at the same time:

Identify the Min and Max for the respective type and iterations

Identify a random number of iterations using the Min and Max to set the range

Create a dataframe to identify if the attempt was succesful or not

Do the following till there are no more iterations left:

-pick a random amount of time within the range of the database's Ranges table

-push or pull file defined in the database's File table

-log activity to Logs and Messages table

-wait for the random amount of time defined to start up again
    
# To execute both push and pull at the same time run

$ python3 server_tap.py -r

$ python3 server_tap.py -run

# To execute just push run

$ python3 server_tap.py -s

$ python3 server_tap.py -push

# To execute just pull run

$ python3 server_tap.py -l

$ python3 server_tap.py -pull

## connect.py

Every .py file uses the connect.py to connect to the server_tap database.

# Database Structure

## Box_Info Table

The Box_info table hold the information needed to SCP files to and from your servers.

User        - username of the server

IP          - IP address of the server

Private_Key - the location of where the private key is located, place in Keys directory to clean storage

Port        - SSH port locatoin

By default this table will be empty

## Interacting With Box_Info Table

### To add a new server run 

$ python3 server_tap.py -a

$ python3 server_tap.py -add

### To edit information in the server run

$ python3 server_tap.py -u

$ python3 server_tap.py -update

### To delete a server run

$ python3 server_tap.py -d

$ python3 server_tap.py -delete

### To check the status of a server run

$ python3 server_tap.py -c

$ python3 server_tap.py -check

## Ranges Table

The Ranges table holds the information that determines the minimum and maximum values to Push, Pull, and Iterations. This information will be used to randomize how many times files will be pushed and pulled as well as how many iterations there will be.

By default the Min values are 10 and the max values are 20.

### To change the values run

$ python3 server_tap.py -i

$ python3 server_tap.py -iterations

The code will not let you place a min greater or equal than the max and a max less than or equal to a min.

## Files Table

The Files table is where you store the file name you would like to push to and grab from your servers. 

By default the Push file will be requirements.txt and the pull file will be test.txt.

### To change the file to push run

$ python3 server_tap.py -sf _path/to/file_

$ python3 server_tap.py -pushf _path/to/file_

### To change the file to pull run

$ python3 server_tap.py -lf _path/to/file_

$ python3 server_tap.py -pullf _path/to/file_

## Logs Table

The Logs table hold information regarding every push and pull, what date/time the action occured, and if that action was successful or not.

### To covert the Logs table to a csv run

$ python3 server_tap.py -ol _path/to/file_

$ python3 server_tap.py -logs _path/to/file_

## Messages Table

The Messages table holds every message printed in the terminal

### To covert the Messages table to a txt run

$ python3 server_tap.py -om _path/to/file_

$ python3 server_tap.py -messages _path/to/file_