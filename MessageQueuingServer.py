#!/usr/bin/python3

######################################################################################################
# References:
# https://docs.python.org/3/library/xmlrpc.server.html#module-xmlrpc.server
######################################################################################################

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import sys

message_queue = []

# *** Restore previous messages start ***
print("Restoring backup...")
try:
    f1 = open("MessageQueueBackup.txt", 'r')
    for line in f1:
        # Add messages to message queue
        message_queue.append(line.strip('\n'))
except FileNotFoundError:
    # Handle file reader exception
    f1.close()
    print("Exception caught")
finally:
    # Close pointer
    f1.close()
print("Restoring backup successful")
# *** Restore previous messages end ***


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Creates server instance
with SimpleXMLRPCServer(("localhost", 6000),
                        requestHandler=RequestHandler, allow_none=True) as server:
    try:
        # Ready to add functions for RPC calls
        server.register_introspection_functions()

        def student_process(msg):
            """Add responses from student process into message queue"""
            # Append to queue
            message_queue.append(msg)
            print("=" * 60)
            # Print queue
            print("\t Current Queue status")
            print("{},{},{},{},{}".format("Destination Process", "Process ID", "Student Name", "Course", "Status(op)"))
            print("=" * 60)
            for temp1 in message_queue:
                print(temp1)
            print("=" * 60)
            # Send status to student process
            return "Message Received"

        # Register function with RPC instance
        server.register_function(student_process, 'student_process')

        def advisor_process():
            """Returns messages from student process and remove processed messages from message queue"""
            advisor_send = []
            for temp1 in message_queue:
                split_temp = temp1.split(",")
                if split_temp[0] == 'AdvisorProcess':
                    # Add to temporary list
                    advisor_send.append(split_temp[1] + "," + split_temp[2] + "," + split_temp[3])
                    # Remove sent messages from queue
                    message_queue.remove(temp1)

            return advisor_send

        # Register function for RPC calls
        server.register_function(advisor_process, 'advisor_process')

        def advisor_response(msg):
            """Add results of advisor to message queue"""
            for temp in msg:
                message_queue.append(temp)
                # Print latest queue
                print("=" * 60)
                print("\t Current Queue status")
                print("{},{},{},{},{}".format("Destination Process", "Process ID", "Student Name", "Course", "Status"))
                print("=" * 60)
                for temp2 in message_queue:
                    print(temp2)
                print("=" * 60)
        # Register function for RPC calls
        server.register_function(advisor_response, 'advisor_response')

        def notification_process():
            """Return notification responses from message queue"""
            notification_send = []
            for temp1 in message_queue:
                split_temp = temp1.split(",")
                if split_temp[0] == 'NotificationProcess':
                    # Add results to temporary list
                    notification_send.append(split_temp[1] + "," + split_temp[2] + "," + split_temp[3] + "," + split_temp[4])
                    # Print queue
                    print("=" * 60)
                    print("\t Current Queue status")
                    print("{},{},{},{},{}".format("Destination Process", "Process ID", "Student Name", "Course", "Status"))
                    print("=" * 60)
                    for temp2 in message_queue:
                        print(temp2)
                    print("=" * 60)
                    # Remove processed messages from queue
                    message_queue.remove(temp1)
            # Return list to notification process
            return notification_send

        # Register function for RPC calls
        server.register_function(notification_process, 'notification_process')

        # Run the server's main loop infinite times
        server.serve_forever()
    except KeyboardInterrupt:
        # Handle keyboard interrupt exception
        print("[x] Interrupt received, exiting server...")
        # *** Backup queue start ***
        print("Backup in progress...")
        f = open("MessageQueueBackup.txt", 'w')
        for temp in message_queue:
            f.write(temp + '\n')
        f.close()
        print("Backup successful")
        # *** Backup queue end ***
        # Exit program
        sys.exit(0)
    except:
        # Handle random exceptions
        print("[x] Killing process, exiting server...")
        sys.exit(0)
