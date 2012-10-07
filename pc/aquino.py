# This is just an example of a daemon which could run to constantly get
# data from serial and send it to the API

# TODO: find a way to test serial - would be good to simulate all sensors

import serial
import sys
import time
import json

PORT = '/dev/ttyACM0'
BAUDS = 9600
# how often to send data to the server (seconds)
SEND_THRESHOLD = 300  # 5 min


class Aquino:

    collected_data = []
    should_listen = True

    def __init__(self, consumer_key, consumer_secret,
            serial_port=PORT, bauds=BAUDS,
            threshold=SEND_THRESHOLD,
            protocol='https://', domain='', port=443):
        """
        Prepare connection to server, read server time, initiate serial
        connection to Arduino
        param:    key
        param:    secret
        param:    port
        param:    threshold   How often to send data to the server
        """
        self.threshold = threshold
        self.s = serial.Serial(serial_port, bauds, timeout=1)
        # store server time
        self.server_time = self.get_server_time()
        # set the time when data was send
        self.send_time = time.time()
        # save the key and scret for now
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def get_server_time(self):
        return time.time()

    def collect_data(self, data):
        seconds = int(time.time() - self.send_time)
        data['seconds'] = seconds
        self.collected_data.append(data)
        if seconds >= self.threshold:
            self.send_collected_data()

    def send_collected_data(self):
        prepared_data = []
        for i in range(1, len(self.collected_data)):
            data = self.collected_data.pop(0)
            data['time'] = self.server_time + data['seconds']
            del data['seconds']
            prepared_data.append(data)

        data = {"consumer_key": self.consumer_key,
                "consumer_secret": self.consumer_secret,
                "data": prepared_data}

        # send data to the server
        # in response receive server's time
        print data
        self.send_time = time.time()
        self.server_time = self.get_server_time()

    def listen(self, max_count=None):
        buffer = ''
        first = True
        counter = 0;

        # this should work like a daemon so it would be possible to start/stop/status
        while self.should_listen:
            if '\n' in buffer:
                # skip if a line already in buffer
                pass
            else:
                # this will block until one more char or timeout
                buffer += self.s.read(1)
            # get remaining buffered chars
            buffer += self.s.read(self.s.inWaiting())
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
                    # Collectd data
                    self.collect_data(data)
                    # discontinue if counter > max_count
                    if max_count:
                        counter += 1
                        if counter >= max_count:
                            self.should_listen = False
                            self.send_collected_data()
                # If the Arduino sends lots of empty lines, you'll lose the
                # last filled line, so you could make the above statement conditional
                # like so: if lines[-2]: last_received = lines[-2]
                buffer = lines[-1]

        sys.stdout.write("\nListening finished\n\n")
