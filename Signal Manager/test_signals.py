import queue
import threading
import time

class Singleton(type):
    __instance = None
    __instances = {}

def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
        cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances[cls]

class Signal_Manager(metaclass=Singleton):
    sig_map = {}
    asynq = queue.Queue()

    def __init__(self):
        t = threading.Thread(target=self.__listen)
        t.daemon = True
        t.start()

    def __listen(self):
        while True:
            if self.asynq.empty():
                time.sleep(3) # Time lapse for async queued signal check
                continue

            signal, args, kwargs = self.asynq.get()
            self.emit(signal, *args, **kwargs)

    def connect(self, signal, slot):
        '''
        Connect signal with slot to receive message
        '''
        if signal not in self.sig_map.keys():
            self.sig_map[signal] = []
        self.sig_map[signal].append(slot)

    def disconnect(self, signal, slot):
        '''
        Disconnect signal message
        '''
        if signal in self.sig_map.keys():
            if slot in self.sig_map[signal]:
                self.sig_map[signal].remove(slot)

    def emit(self, signal, *args, **kwargs):
        '''
        Synchronous emission
        '''
        if signal in self.sig_map.keys():
            for s in self.sig_map[signal]:
                try:
                    s(*args, **kwargs)
                except Exception as e:
                    print(e)

    def amit(self, signal, *args, **kwargs):
        '''
        Asyncrhonous emission. Immediately return. No context hang.
        '''
        self.asynq.put([signal, args, kwargs])

    def nmit(self, signal, *args, **kwargs):
        '''
        N thread asynchronus emission. Immediately return. No context hang.
        '''
        t = threading.Thread(target=lambda: self.emit(signal, *args, **kwargs))
        t.daemon = True
        t.start()

sigmgr = Signal_Manager()

def slot_sig1():
    print('Hello 01')

def slot_sig2(**kwargs):
    print(kwargs)

def slot_sig3(*args, **kwargs):
    print(args)
    print(kwargs)
    time.sleep(1)

if __name__ == '__main__':
    # two sync signals call
    sigmgr.connect('Signal_01', slot_sig1)
    sigmgr.emit('Signal_01')

    sigmgr.connect('Signal_02', slot_sig2)
    sigmgr.emit('Signal_02', data='Hello 02')

    # one thread async > time delay 1 sec by each call
    sigmgr.connect('Signal_03', slot_sig3)
    sigmgr.amit('Signal_03', (1, 2, 3, 4,), data='Hello 03')
    sigmgr.amit('Signal_03', (1, 2, 3, 4,), data='Hello 04')
    sigmgr.amit('Signal_03', (1, 2, 3, 4,), data='Hello 05')
    print('aync emit !')

    # n thread async > output right away all call
    sigmgr.nmit('Signal_03', (1, 2, 3, 4,), data='Hello 06')
    sigmgr.nmit('Signal_03', (1, 2, 3, 4,), data='Hello 07')
    sigmgr.nmit('Signal_03', (1, 2, 3, 4,), data='Hello 08')
    print('n thread aync emit !')
    time.sleep(10)
    exit(0)