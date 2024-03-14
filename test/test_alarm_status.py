import unittest
from src.alarm_status import AlarmStatus

class TestAlarmStatus(unittest.TestCase):

    def setUp(self):
        self.alarm_status_processor = AlarmStatus()

    def test_valid_input(self):
        context = "0f0000000600000000000000"
        expected_result = ['2,3', '', '', '']
        result = self.alarm_status_processor.hex_bit_alarm_status(context)
        self.assertEqual(result, expected_result)

    def test_invalid_input(self):
        context = "invalid_context_data"
        result = self.alarm_status_processor.hex_bit_alarm_status(context)
        self.assertIsNone(result)

    def test_empty_input(self):
        context = ""
        result = self.alarm_status_processor.hex_bit_alarm_status(context)
        self.assertIsNone(result)

    def test_short_input(self):
        context = "0f0000000600"
        result = self.alarm_status_processor.hex_bit_alarm_status(context)
        self.assertIsNone(result)

    def test_integer_input(self):
        context = 123456
        result = self.alarm_status_processor.hex_bit_alarm_status(context)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
