import serial
import time
def getValue(previous):
    service = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
    time.sleep(2)
    test = str(service.read(25))
    test = test[2: len(test)-1]
    for ind in range(0, (20-len(test))):
        test = "a" + test
    test = findIterations(test)
    while (test == 'none' and len(test) < 6):
        print('loop')
        test = str(service.read(25))
        test = test[2: len(test)-1]
        for ind in range(0, (25-len(test))):
            test = "a" + test
        test = findIterations(test)
    connect = test
    if (len(test) == 5):
        connect = connect[0:3] + connect[4:5]
    if (len(test) == 6):
        connect = connect[0:3] + connect[5:6]
    connect = float(connect)
    return connect
def findIterations(word):
    first = word.find('12345')
    if (first == -1 or first > 9):
        return 'none'
    word = word[first+5:]
    second = word.find('12345')
    word = word[:second]
    return word