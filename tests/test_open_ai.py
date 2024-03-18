import unittest
from unittest.mock import MagicMock, patch
from open_ai import generate_response_with_history


class TestGenerateResponseWithHistory(unittest.TestCase):
    @patch("open_ai.OpenAI")
    def test_generate_response_with_history(self, mock_openai):
        # Mock response class
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "AI Response"
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        # Sample input
        session_id = "Session1"
        user_command = "Turn on the light"
        entities = [{
            'entity_id': 'light.living_room',
            'attributes': {'group_name': 'Living Room'},
            'state': 'off'
        }]
        sensors = [{
            'entity_id': 'sensor.living_room_temperature',
            'state': '24°C'
        }]
        system_prompt = "System Prompt"
        open_ai_key = "key"

        response = generate_response_with_history(session_id, user_command, entities, sensors, system_prompt,
                                                  open_ai_key)

        # Check the response
        self.assertEqual(response, "AI Response")

        # Check if the OpenAI API was called with the correct arguments
        mock_openai.return_value.chat.completions.create.assert_called_with(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": (
                    f"\n\nUser issued the command: '{user_command}'."
                    "\n\nThe system has the following sensors: sensor.living_room_temperature: 24°C."
                    " Other entities: light.living_room (group: Living Room): off.")
                 }],
            temperature=0.5,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["User issued the command:", "AI:"]
        )


if __name__ == "__main__":
    unittest.main()
