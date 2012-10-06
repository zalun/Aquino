# read data from mocked serial

import unittest
import serial
import json
import time
from mock import Mock
import pc
from random import random

PORT = 1


class Serial(serial.Serial):
    responses = None
    sleep = False
    sleep_random = None

    def __init__(port, *args, **kwargs):
        try:
            super(Serial, self).__init__(port, *args, **kwargs)
        except Exception:
            pass

    def read(self, *args, **kwargs):
        if self.sleep:
            if self.sleep_random:
                sleep = self.sleep * random()
            else:
                sleep = self.sleep
            time.sleep(sleep)
        if args and args[0] == 1:
            return "\n"

        if self.responses:
            return self.responses.pop(0)

    def inWaiting(self):
        return 4



OLD_READ = Serial.read

serial.Serial = Serial

# 1 fiinshed but not stated properly line
# 2 not filled lines
# 5 full lines
COMMON_RESPONSE = ['": "x"}\n', '{"a": "b', '{"a": "b"}\n', '{"c": "d"}\n', '{"e": "f"}\n',
                '{"g', '{"g": "h"}\n', '{"i": "j"}\n']


class testMeasurement(unittest.TestCase):

    def setUp(self):
        self.s = serial.Serial(PORT, timeout=1)
        self.collect_data = pc.Aquino.collect_data
        self.send_collected_data = pc.Aquino.send_collected_data

    def tearDown(self):
        serial.Serial.read = OLD_READ
        pc.Aquino.collect_data = self.collect_data
        pc.Aquino.send_collected_data = self.send_collected_data
        serial.Serial.sleep = False
        serial.Serial.sleep_random = None

    def test_read(self):
        """Test readline method"""
        serial.Serial.responses = COMMON_RESPONSE[:]
        self.assertEqual(self.s.read(), COMMON_RESPONSE[0]);

    def test_collect_data_count(self):
        serial.Serial.responses = COMMON_RESPONSE[:]
        pc.Aquino.collect_data = Mock()
        a = pc.Aquino('a', 'b')
        a.listen(max_count=4)
        self.assertEqual(pc.Aquino.collect_data.call_count, 4)
        # 0 is omited as first == True
        self.assertEqual(
                pc.Aquino.collect_data.call_args_list[0][0][0],
                json.loads(COMMON_RESPONSE[2]))

    def test_send_data_called(self):
        serial.Serial.responses = COMMON_RESPONSE[:]
        serial.Serial.sleep = 0.8
        serial.Serial.sleep_random = True
        pc.Aquino.send_collected_data = Mock()
        a = pc.Aquino('a', 'b', threshold=1)
        a.listen(max_count=2)
        self.assertTrue(pc.Aquino.send_collected_data.called)
