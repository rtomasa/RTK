from a import A
from b import B

def main():
    a = A()
    b = B()
    print('Test 1')
    a.print()
    b.print()
    print('Test 2')
    a.change()
    a.print()
    b.print()

if __name__ == '__main__':
    main()