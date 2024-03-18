import unittest
import requests
from unittest.mock import patch
from home_assistant import (get_all_entities, get_all_sensors,
                            send_service_message, send_to_home_assistant)


class TestHomeAssistant(unittest.TestCase):
    def setUp(self):
        self.json_obj_event = {
            "action": "EVENT",
            "event": [
                {"type": "ON", "device": "light"},
                {"type": "OFF", "device": "light"}
            ]
        }

        self.json_noevent = {
            "action": "NOEVENT",
            "event": []
        }

        self.url = 'http://myhomeassistant_url.com'
        self.headers = {'content-type': 'application/json'}

    @patch('requests.get')
    def test_get_all_entities_success(self, mock_get):
        # Setup
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = [{'entity_1': 'value'}, {'entity_2': 'value'}]
        home_assistant_url = 'http://test-home-assistant.com/'
        headers = {'header_1': 'value'}

        # Exercise
        result = get_all_entities(home_assistant_url, headers)

        # Verify
        self.assertEqual(result, [{'entity_1': 'value'}, {'entity_2': 'value'}])
        mock_get.assert_called_once_with(f'{home_assistant_url}states', headers=headers)

    @patch('requests.get')
    def test_get_all_entities_failure(self, mock_get):
        # Setup
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        mock_response.json.return_value = []
        home_assistant_url = 'http://test-home-assistant.com/'
        headers = {'header_1': 'value'}

        # Exercise
        result = get_all_entities(home_assistant_url, headers)

        # Verify
        self.assertEqual(result, [])
        mock_get.assert_called_once_with(f'{home_assistant_url}states', headers=headers)

    def test_get_all_sensors(self):
        entities = [
            {'entity_id': 'sensor.temp', 'value': '20'},
            {'entity_id': 'sensor.humidity', 'value': '30'},
            {'entity_id': 'light.room', 'value': 'on'}
        ]
        expected_output = [
            {'entity_id': 'sensor.temp', 'value': '20'},
            {'entity_id': 'sensor.humidity', 'value': '30'}
        ]
        self.assertEqual(get_all_sensors(entities), expected_output)

    def test_get_all_sensors_with_no_sensors(self):
        entities = [
            {'entity_id': 'light.room', 'value': 'on'},
            {'entity_id': 'switch.living_room', 'value': 'off'}
        ]
        self.assertEqual(get_all_sensors(entities), [])

    def test_get_all_sensors_with_empty_list(self):
        entities = []
        self.assertEqual(get_all_sensors(entities), [])

    @patch('requests.post')
    @patch('logging.debug')
    def test_send_service_message_success(self, mock_debug, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        event = {"entityId": "light.living_room", "service": "turn_on", "data": {"brightness": 255}}
        home_assistant_url = "http://localhost:8123/api/"
        headers = {"Authorization": "Bearer YOUR_LONG_LIVED_ACCESS_TOKEN"}

        send_service_message(event, home_assistant_url, headers)

        mock_debug.assert_called_once()
        mock_post.assert_called_once()

    @patch('requests.post')
    @patch('logging.error')
    def test_send_service_message_failure(self, mock_error, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 404
        event = {"entityId": "light.living_room", "service": "turn_on", "data": {"brightness": 255}}
        home_assistant_url = "http://localhost:8123/api/"
        headers = {"Authorization": "Bearer YOUR_LONG_LIVED_ACCESS_TOKEN"}

        send_service_message(event, home_assistant_url, headers)

        mock_error.assert_called_once()
        mock_post.assert_called_once()

    @patch('home_assistant.send_service_message')
    def test_process_response_and_send_to_home_assistant_events(self, mock_send_service_message):
        send_to_home_assistant(self.json_obj_event, self.url, self.headers)
        mock_send_service_message.assert_called()

    @patch('home_assistant.send_service_message')
    def test_process_response_and_send_to_home_assistant_no_events(self, mock_send_service_message):
        send_to_home_assistant(self.json_noevent, self.url, self.headers)
        mock_send_service_message.assert_not_called()


if __name__ == '__main__':
    unittest.main()
