from openai import OpenAI

# In-memory storage for conversation histories
conversations = {}


def generate_response_with_history(session_id, user_command, entities, sensors, system_prompt, open_ai_key):
    """
    :param session_id: The ID of the conversation session.
    :param user_command: The command issued by the user.
    :param entities: The list of entities.
    :param sensors: The list of sensors.
    :param system_prompt: The prompt for the system.
    :param open_ai_key: The API key for OpenAI.
    :return: The generated response.

    Generate a response with conversation history.

    This method generates a response using OpenAI's chat completions API,
    taking into account the conversation history. The response is based on
    the user's command, the entities and sensors provided, and the system prompt.

    The method follows these steps:
    1. Retrieve the conversation history for the session ID.
    2. Simplify the entities and sensors information for the prompt.
    3. Construct the prompt by combining the history, user's command,
       and information about sensors and entities.
    4. Create a messages list containing the system prompt and the constructed prompt.
    5. Use the OpenAI client to make a chat completions API call.
    6. Update the conversation history with the user's command and AI's response.
    7. Return the AI's response.

    """
    history = conversations.get(session_id, "")

    # Simplify the entities and sensors information for the prompt
    sensor_details = ', '.join([f"{sensor['entity_id']}: {sensor['state']}" for sensor in sensors])
    entity_details = ', '.join([
        f"{entity['entity_id']} (group: {entity['attributes'].get('group_name')}): {entity['state']}"
        for entity in entities
        if not entity['entity_id'].startswith('sensor.') and not entity['attributes'].get('is_hue_group')])

    prompt = (f"{history}\n\n"
              f"User issued the command: '{user_command}'.\n\n"
              f"The system has the following sensors: {sensor_details}. Other entities: {entity_details}.")

    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]

    client = OpenAI(api_key=open_ai_key)
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        temperature=0.5,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["User issued the command:", "AI:"]
    )

    updated_history =\
        f"{history}User issued the command: '{user_command}'.\nAI: {response.choices[0].message.content}\n"
    conversations[session_id] = updated_history  # Update the conversation history

    return response.choices[0].message.content
