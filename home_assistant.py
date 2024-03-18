import logging

import requests


def get_all_entities(home_assistant_url, headers):
    """
    Get all entities in Home Assistant.

    :param home_assistant_url: The URL of the Home Assistant instance.
    :param headers: The headers to include in the request.
    :return: A list of entities in Home Assistant. Each entity is represented as a dictionary.
    """
    response = requests.get(f'{home_assistant_url}states', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []


def get_all_sensors(entities):
    """
    Get all sensors from the given list of entities.

    :param entities: A list of entities.
    :type entities: list

    :return: A list of sensors.
    :rtype: list
    """
    return [entity for entity in entities if entity['entity_id'].startswith('sensor.')]


def send_service_message(event, home_assistant_url, headers):
    """
    Sends a service message to Home Assistant.

    :param event: The event data containing the entity ID, service, and data.
    :type event: dict
    :param home_assistant_url: The base URL of the Home Assistant instance.
    :type home_assistant_url: str
    :param headers: The headers for the HTTP request.
    :type headers: dict
    :return: None.
    :rtype: None
    """
    service_domain, _ = event["entityId"].split(".", 1)
    entity_id = event["entityId"]
    service_data = event.get("data", {})

    # Construct the payload
    payload = {
        "entity_id": entity_id,
        **service_data
    }

    # Construct the URL for the service call
    url = f"{home_assistant_url}services/{service_domain}/{event['service']}"

    # Make the POST request
    response = requests.post(url, json=payload, headers=headers)

    # Check the response
    if response.status_code == 200:
        logging.debug(f"Successfully called {event['service']} on {entity_id}.")
    else:
        logging.error(
            f"Failed to call service for {event}. Status code: {response.status_code}, response: {response.text}")


def send_to_home_assistant(json_object, home_assistant_url, headers):
    """
    Process the given JSON object and send events to Home Assistant.

    :param json_object: The JSON object containing events to be sent.
    :param home_assistant_url: The URL of the Home Assistant instance.
    :param headers: The headers to be included in the request to Home Assistant.
    :return: None
    """
    # Check if the action is to send events
    if json_object.get("action") == "EVENT":
        # Iterate over each event in the event array
        for event in json_object.get("event", []):
            # Call the send_service_message method for each event
            send_service_message(event, home_assistant_url, headers)
