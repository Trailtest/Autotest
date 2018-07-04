import serial
import time
import sys


def at_request(SERIALPORT, BAUDRATE):
    ser = serial.Serial(SERIALPORT, BAUDRATE, timeout=1)

    try:
        ser.open()
        print(ser.name + 'IS OPEN....')

    except Exception, e:
        print "error open serial port: " + str(e)
        exit()

    if ser.isOpen():

        try:

            data = 'AT+CSQ'
            ser.write(data.encode('ascii') + '\r\n')
            print("write data: ATI")
            time.sleep(2)

            while True:

                response = ser.readline()
                if 'CSQ: ' in response:
                    s = response.split('CSQ: ')
                    if len(s) > 1:
                        s2 = s[1].split('\r')[0]
                    if ',' in s2:
                        out_1 = s2.split(',')[0]
                        out_2 = s2.split(',')[1]

                    print(out_1 + '  hhhhh ' + out_2)
                    break
                time.sleep(2)
                print("read data: " + response)

            ser.close()

        except Exception, e:
            print "error communicating...: " + str(e)

    else:
        print "cannot open serial port "


if __name__ == '__main__':
    port = sys.argv[1]
    brate = int(sys.argv[2])

    at_request(port, brate)
