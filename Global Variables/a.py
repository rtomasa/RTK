import globals

class A:
    def __init__(self):
        pass

    def print(self):
        print('A', globals.g1)
        print('A', globals.g2)

    def change(self):
        globals.g2 = 'bye'