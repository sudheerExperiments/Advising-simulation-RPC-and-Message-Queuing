import xmlrpc.client
import sys

# Initialize connection to server
s = xmlrpc.client.ServerProxy('http://localhost:6000', allow_none=True)
# Process ID
user_id = 0


def read_input():
    """Used to take input name, course details from user on command prompt"""
    try:
        # Use global ID
        global user_id
        user_id += 1
        # Read input
        name = input("Enter your name:")
        sub = input("Enter subject to request clearance:")
        # Send input to server
        return "AdvisorProcess" + "," + str(user_id) + "," + name + "," + sub
    except KeyboardInterrupt:
        # Handle keyboard interrupt exception
        print("\n[x] Interrupt received, exiting server...")
        # Exit program
        sys.exit(0)


if __name__ == '__main__':
    """Logical start of program
       Call various functions and handle exceptions"""
    while True:
        try:
            # Call server function
            result = s.student_process(read_input())
            # Print status
            print("Status:{}".format(result))
        except KeyboardInterrupt:
            # Handle keyboard interrupt exception
            print("\n[x] Interrupt received, exiting server...")
            # Exit program
            sys.exit(0)