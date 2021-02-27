import globals

class B:
    def __init__(self):
        pass

    def print(self):
        print('B', globals.g1)
        print('B', globals.g2)