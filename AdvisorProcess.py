#!/usr/bin/python3

######################################################################################################
# References:
# https://docs.python.org/3/library/xmlrpc.client.html#module-xmlrpc.client
# Dynamic function adding: https://stackoverflow.com/questions/494997/howto-xml-rpc-dynamic-function-registration-in-python
# Keyboard Interrupt: https://stackoverflow.com/questions/21120947/catching-keyboardinterrupt-in-python-during-program-shutdown
# Run infinite loop: https://codedump.io/share/4wmAPzixsCJz/1/how-to-run-the-python-program-forever
# Threading: https://www.tutorialspoint.com/python/python_multithreading.htm

# Networked chat: https://youtu.be/PkfwX6RjRaI
######################################################################################################

import xmlrpc.client
import random
# from threading import Thread
import time
import sys

try:
    # Initialize connection to server
    s = xmlrpc.client.ServerProxy('http://localhost:6000', allow_none=True)
except ConnectionRefusedError:
    # Handle connection exception
    print("Cannot establish connection to server...")
    print("[x] Start server process first, exiting advisor process...")
    # Exit program
    sys.exit(0)


def responses(msg):
    """Generate random response for each student request
       and add them into message queue"""
    try:
        result_list = []
        # Random decisions list
        random_list = ['yes', 'no', 'yes', 'no', 'yes', 'no', 'no']
        for temp in msg:
            # Select a decision in random
            random_string = random.sample(random_list, 1)
            print("=" * 40)
            print("\t Received messages")
            print(temp)
            print("=" * 40)
            # Append to temporary list
            result_list.append("NotificationProcess" + "," + temp + "," + random_string[0])
        #  Send message to server ==> Return temporary list
        return result_list
    except KeyboardInterrupt:
        # Handle keyboard interrupt exception
        print("[x] Interrupt received, exiting server...")
        sys.exit(0)
    except ConnectionRefusedError:
        # Handle connection exception
        print("Cannot establish connection to server...")
        print("[x] Start server process first, exiting advisor process...")
        # Exit program
        sys.exit(0)


def get_messages():
    """Read messages from message queue"""
    result_msg = []
    while True:
        try:
            # Call server function ==> Read messages from student
            result_msg = s.advisor_process()
            if len(result_msg) == 0:
                # Sleep when no messages in message queue
                print("[x] No messages to retrieve")
                # Sleep
                time.sleep(3)
            elif len(result_msg) != 0:
                # Generate random decisions
                response_result = responses(result_msg)
                # Send responses to server ==> Advisor decisions
                s.advisor_response(response_result)
        except KeyboardInterrupt:
            # Handle keyboard interrupt exception
            print("[x] Interrupt received, exiting server...")
            # Exit program
            sys.exit(0)
        except ConnectionRefusedError:
            # Handle connection exception
            print("Cannot establish connection to server...")
            print("[x] Start server process first, exiting advisor process...")
            # Exit program
            sys.exit(0)


if __name__ == '__main__':
    """Logical start of program
       Call various functions and handle exceptions"""
    try:
        # Call function
        get_messages()
    except KeyboardInterrupt:
        # Handle keyboard interrupt
        print("[x] Interrupt received, exiting server...")
        # Exit program
        sys.exit(0)