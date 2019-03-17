import os
import time
import re
from slackclient import SlackClient
from lenin.action import ALL as COMMAND

is_good_env = os.getenv('LENIN_PROJECT', None)
if is_good_env is None:
    raise EnvironmentError('Please define environment variables:\n\tLENIN_PROJECT\n\tBOT_ACCESS_TOKEN\n'
                           '\tBOT_USER_ACCESS_TOKEN')
print("value BOT_ACCESS_TOKEN={}".format(os.environ['BOT_ACCESS_TOKEN']))
print("value BOT_USER_ACCESS_TOKEN={}".format(os.environ['BOT_USER_ACCESS_TOKEN']))

# instantiate Slack client
slack_client = SlackClient(os.environ.get('BOT_USER_ACCESS_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starter_bot_id = None

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
MENTION_REGEX = '^<@([WU][0-9A-Z]+)>\s*(.*)'


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message":  #  and "subtype" not in event
            user_ids, message = parse_direct_mention(event["text"])
            if len(user_ids) == 0 or starter_bot_id in user_ids:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention,
        returns None
    """
    user_ids = []
    matches = re.search(MENTION_REGEX, message_text)
    while matches:
        user_id, message_text = matches.groups()
        user_ids.append(user_id)
        matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains
    # the remaining message
    return user_ids, message_text.strip()


def handle_command(cmd, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(list(COMMAND.keys()))

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    worlds = cmd.split()
    action = str(worlds[0]).lower()
    if worlds and action in COMMAND:
        response = COMMAND[action](worlds[1:])

    if response:
        # Sends the response back to the channel
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starter_bot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
