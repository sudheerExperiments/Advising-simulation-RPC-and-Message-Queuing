import xmlrpc.client
import time
import sys

try:
    # Initialize connection to server
    s = xmlrpc.client.ServerProxy('http://localhost:6000', allow_none=True)
except ConnectionRefusedError:
    # Handle connection exceptions
    print("Cannot establish connection to server...")
    print("[x] Start server process first, exiting notification process...")
    # Exit program
    sys.exit(0)


def read_messages():
    """Read messages from message queue and display response on command prompt"""
    print("In notification process")
    result_msg = []
    while True:
        try:
            # Call server and get messages from message queue
            result_msg = s.notification_process()
            if len(result_msg) == 0:
                # Sleep when message queue is empty
                print("[x] No messages to retrieve")
                # Sleep
                time.sleep(7)
            elif len(result_msg) != 0:
                # Display output when result is not empty
                for temp in result_msg:
                    # Print each message
                    split_temp = temp.split(',')
                    print("=" * 40)
                    print("\t Decision")
                    print("=" * 40)
                    print("Student name: {}".format(split_temp[1]))
                    print("Course clearance request: {}".format(split_temp[2]))
                    print("Status: {}".format(split_temp[3]))
                    print("=" * 40)
        except KeyboardInterrupt:
            # Handle keyboard interrupt exception
            print("[x] Interrupt received, exiting notification process...")
            # Exit program
            sys.exit(0)
        except ConnectionRefusedError:
            # Handle connection exception
            print("Cannot establish connection to server...")
            print("[x] Start server process first, exiting notification process...")
            # Exit program
            sys.exit(0)


if __name__ == '__main__':
    """Logical start of program
       Call various functions and handle exceptions"""
    try:
        # Function call
        read_messages()
    except KeyboardInterrupt:
        # Handle keyboard interrupt exception
        print("[x] Interrupt received, exiting notification process...")
        # Exit program
        sys.exit(0)