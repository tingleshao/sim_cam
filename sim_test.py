# This is the test for the simulation program
import main as main


def test(test_number):
# Test 0: 1 Layer, 2x2, 1024 x 768
# Trivial strategy 1
if test_number == 0:
    main.run()

# Test 1: 2 Layers
# Trivial strategy 1
elif test_number == 1:
    main.run()

# Test 2: 1 Layer
# Trivial stategy 2
elif test_number == 2:
    main.run()

# Test 3: 2 Layers
# Trivial strategy 2
elif test_number == 3:
    main.run()

if __name__ == '__main__':
    test_number = int(argv[1])
    test(test_number)
