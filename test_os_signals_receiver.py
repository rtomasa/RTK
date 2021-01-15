import signal
import os
import time
import subprocess
import setproctitle

'''
Run the receiver in background first, then run the sender to send signal.
Do note that setproctitle module is also required for this test.
'''

''' Program receiver '''

def set_process_name(name):
    setproctitle.setproctitle(name)

def receive_os_signal(signalNumber, frame):
    print('Received signal:', signalNumber)

if __name__ == '__main__':
    signal.signal(signal.SIGUSR1, receive_os_signal)
    set_process_name('test_process')
    time.sleep(10)