# Online Advising Simulation using RPC and Message Queues

>**Note: This project is submitted as part of class projects for CSE 5306 at University of Texas Arlington**

>**This code should not be used for the course CSE 5306 offered at University of Texas Arlington**

### Requirements:

* Python 3.6.2 or later
* xmlrpc library(Already present in python default libraries)

### Download links:

* [Python v3.6.2](https://www.python.org/downloads/)

### Features:
* Can resume sending messages when server crashes(Message queue is persistent).

### Setup:
The project is designed to run in python 3. I recommend to check the library requirements before running the project in later or before versions.

#### Components:

1. MessageQueuingServer.py
2. StudentProcess.py
3. AdvisorProcess.py
4. NotificationProcess.py

#### Default connection parameters:

##### RPC server:

> Server IP: localhost

> Server port number: 6000

##### RPC client: 

> Client IP: localhost

> Client port number: 6000

**The values can be changed in the code as shown below**
 
```
Server:

with SimpleXMLRPCServer((<IP>, <Port>), requestHandler=RequestHandler, allow_none=True) as server:

Client:

xmlrpc.client.ServerProxy('http://<IP>.:<Port>', allow_none=True)
```

### Project execution:

1. Run **MessageQueuingServer** using the command: `python MessageQueuingServer.py`

>After executing, the process will wait for messages from other processes and will run in an infinite loop.


2. Run **StudentProcess** using the command: python StudentProcess.py

After executing, the process runs in an infinite loop and asks user for input in repeat.

```
Sample input:

Enter your name: <name>
Enter subject to request clearance: <subject code>
```

If the message is received by server, a status message, *Message received* will be displayed. Then the program will prompt user to display his next input.

3. Run **AdvisorProcess.py** using the command: `python AdvisorProcess.py`

After executing, the process runs in an infinite loop. 


4. Run **NotificationProcess.py** using the command: `python NotificationProcess.py`

After executing, the process runs in an infinite loop and requests server for advisor responses. 


### Limitations:

* The server and clients are designed to run locally. Modifications might be required to run in remote environment.

### Additional information:

For more information refer the project wiki.
