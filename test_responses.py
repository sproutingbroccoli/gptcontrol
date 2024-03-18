TEST_MORE_INFO_COUNTER = 0
TEST_MORE_INFO_MAX = 3


def prefab_response(command, mode):
    """
    :param command: The command received from the user.
    :param mode: The mode in which the method should operate. It can be either 'SINGLE_RESPONSE' or 'MORE_INFO'.
    :return: The response message based on the given command and mode.

    The `prefab_response` method generates response messages based on the given command and operating mode. It maintains
    a global counter for tracking the number of MORE_INFO responses.

    If the mode is 'SINGLE_RESPONSE', the method returns an event message with the sessionId and userMessage set
    accordingly.

    If the mode is 'MORE_INFO', the method increments the global counter by 1 and creates a more_info_message with the
    sessionId, userMessage, and the current value of the counter.
    If the  counter exceeds a certain maximum value (TEST_MORE_INFO_MAX), it resets to 0 and returns an event message
    instead.

    Note: The global variable `TEST_MORE_INFO_COUNTER` must be defined before calling this method.
    """
    global TEST_MORE_INFO_COUNTER

    event_message = {
        'action': 'EVENT',
        'sessionId': '12345',
        'userMessage': f'Successfully called! Command was {command}'
    }

    more_info_message = {
        'action': 'MORE_INFO',
        'sessionId': '12345',
        'userMessage': f'More info {TEST_MORE_INFO_COUNTER}. Command was {command}'
    }

    if mode == 'SINGLE_RESPONSE':
        return event_message

    if mode == 'MORE_INFO':
        TEST_MORE_INFO_COUNTER += 1
        if TEST_MORE_INFO_COUNTER >= TEST_MORE_INFO_MAX:
            TEST_MORE_INFO_COUNTER = 0
            return event_message

        return more_info_message
