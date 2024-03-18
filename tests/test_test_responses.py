import unittest
from unittest.mock import patch

# assuming that test_responses is the module name
from test_responses import prefab_response


class TestPrefabResponse(unittest.TestCase):

    @patch('test_responses.TEST_MORE_INFO_COUNTER')
    @patch('test_responses.TEST_MORE_INFO_MAX')
    def test_single_response(self, mock_counter, mock_max):
        command = "test_command"
        mode = "SINGLE_RESPONSE"
        expected_result = {
            'action': 'EVENT',
            'sessionId': '12345',
            'userMessage': f'Successfully called! Command was {command}'
        }
        actual_result = prefab_response(command, mode)
        self.assertEqual(actual_result, expected_result)

    @patch('test_responses.TEST_MORE_INFO_COUNTER', 0)
    @patch('test_responses.TEST_MORE_INFO_MAX', 6)
    def test_more_info_response(self):
        command = "test_command2"
        mode = "MORE_INFO"
        expected_result = {
            'action': 'MORE_INFO',
            'sessionId': '12345',
            'userMessage': f'More info 0. Command was {command}'
        }
        actual_result = prefab_response(command, mode)
        self.assertEqual(actual_result, expected_result)

    @patch('test_responses.TEST_MORE_INFO_COUNTER', 7)
    @patch('test_responses.TEST_MORE_INFO_MAX', 6)
    def test_more_info_max_response(self):
        command = "test_command3"
        mode = "MORE_INFO"
        expected_result = {
            'action': 'EVENT',
            'sessionId': '12345',
            'userMessage': f'Successfully called! Command was {command}'
        }
        actual_result = prefab_response(command, mode)
        self.assertEqual(actual_result, expected_result)


if __name__ == '__main__':
    unittest.main()
