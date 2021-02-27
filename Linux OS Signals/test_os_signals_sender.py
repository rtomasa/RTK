import signal
import os
import time
import subprocess

'''
Run the receiver in background first, then run the sender to send signal.
'''

''' Program sender '''

def get_process_name_pid():
    try:
        process_name_pid = int(subprocess.check_output(["pidof","-s",'test_process']))
        print("Process name found with PID " + str(process_name_pid))
        return process_name_pid
    except:
        print("Error: process not found!")

def send_signal():
    os.kill(get_process_name_pid(), signal.SIGUSR1)
    print("Sending signal SIGUSR1 (10)")

if __name__ == '__main__':
    send_signal()