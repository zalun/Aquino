# This is just an example of a daemon which could run to constantly get
# data from serial and send it to the API

# TODO: find a way to test serial - would be good to simulate all sensors

import serial
import time
import json

PORT = '/dev/ttyACM0'
# how often to send data to the server (seconds)
SEND_THRESHOLD = 5

# this should be received from the server
SERVER_START_TIME = time.time()
collected_data = []

# these 2 should be provided by configuration
username = "user"
password = "pass"


def send_data(send_time, server_time):
    prepared_data = []
    for i in range(1, len(collected_data)):
        data = collected_data.pop(0)
        data['time'] = server_time + data['seconds']
        del data['seconds']
        prepared_data.append(data)

    data = {"username": username,
            "token": token,
            "data": prepared_data}

    # send data to the server
    # in response receive server's time
    print data
    new_send_time = time.time()
    new_server_time = time.time()
    return new_send_time, new_server_time


def collect_data(data, send_time, server_time):
    seconds = int(time.time() - send_time)
    data['seconds'] = seconds
    collected_data.append(data)
    if seconds >= SEND_THRESHOLD:
        send_time, server_time = send_data(send_time, server_time)
    return send_time, server_time


def receiving(ser, server_time):
    buffer = ''
    first = True
    send_time = time.time()

    # this should work like a daemon so it would be possible to start/stop/status
    while True:
        if '\n' in buffer:
            # skip if a line already in buffer
            print "line skipped"
            pass
        else:
            # this will block until one more char or timeout
            buffer += ser.read(1)
        # get remaining buffered chars
        buffer += ser.read(ser.inWaiting())
        if '\n' in buffer:
            # do not perform any action on the first read as it is probably
            # broken, by occasion we've got defintely at least 2 lines
            # in buffer
            if first:
                first = False
                continue

            lines = buffer.split('\n')
            last_received = lines[-2]
            try:
                data = json.loads(last_received)
            except Exception, err:
                pass
            else:
                send_time, server_time = collect_data(data, send_time, server_time)
            #If the Arduino sends lots of empty lines, you'll lose the
            #last filled line, so you could make the above statement conditional
            #like so: if lines[-2]: last_received = lines[-2]
            buffer = lines[-1]


# create a serial connection
connection = serial.Serial(PORT, 9600, timeout=1)
# start receiving data
receiving(connection, SERVER_START_TIME)
# close connection on stop receiving data
connection.close()

