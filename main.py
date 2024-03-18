import json
import logging
import os

from flask import Flask, request, jsonify, Response
import uuid

from home_assistant import send_to_home_assistant, get_all_entities, get_all_sensors
from open_ai import generate_response_with_history
from test_responses import prefab_response

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Configuration
MODE = 'LIVE'  # MORE_INFO, SINGLE_RESPONSE, LIVE
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
HOME_ASSISTANT_TOKEN = os.getenv('HOME_ASSISTANT_TOKEN')
HOME_ASSISTANT_URL = os.getenv('HOME_ASSISTANT_URL')
headers = {
    'Authorization': f'Bearer {HOME_ASSISTANT_TOKEN}',
    'content-type': 'application/json',
}

with open('./system_prompt.txt', 'r') as file:
    SYSTEM_PROMPT = file.read()


@app.route('/command', methods=['POST'])
def process_command():
    try:
        data = request.json
        logging.debug(f'Message received: {json.dumps(data)}')
        user_command = data.get('command')
        session_id = data.get('sessionId') or str(uuid.uuid4())

        if not user_command:
            return jsonify({"error": "No command provided"}), 400

        if MODE != 'LIVE':
            return prefab_response(user_command, MODE)

        entities = get_all_entities(HOME_ASSISTANT_URL, headers)
        sensors = get_all_sensors(entities)

        response = (
            generate_response_with_history(session_id, user_command, entities, sensors, SYSTEM_PROMPT, OPENAI_API_KEY))
        logging.debug(response)
        chatgpt_response = json.loads(response)
        # send_to_home_assistant(chatgpt_response, HOME_ASSISTANT_URL, headers)

        chatgpt_response["sessionId"] = session_id

        return chatgpt_response
    except Exception as e:
        logging.error(f'Error processing: {e}')
        return Response("An unexpected error has occurred. Please try again later.", status=500)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
