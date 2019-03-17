from slackclient import SlackClient
import time
import os


class Bot(object):
    # Bot User OAuth Access Token
    SLACK_BOT_TOKEN = os.getenv('BOT_USER_ACCESS_TOKEN', None)
    TEST_BOT_NAME = os.getenv('TEST_BOT_NAME', '@marx')
    TEST_GROUP = '#test_bots'
    TIMEOUT = 5

    def __init__(self, bot_name=TEST_BOT_NAME):
        self.sc = SlackClient(self.SLACK_BOT_TOKEN)
        self.bot_name = bot_name

    def command(self, command_text: str) -> str:
        assert command_text
        res = self.sc.api_call(
            "chat.postMessage",
            channel=self.TEST_GROUP,
            text="{bot_name} {command_text}".format(bot_name=self.bot_name, command_text=command_text),
            link_names=True
        )
        assert res['ok']
        messages = None
        init_time = time.time()
        while not messages:
            # time.sleep(1)
            answer = self.sc.api_call('conversations.history', channel=res['channel'], oldest=res['ts'])
            assert answer['ok']
            messages = answer['messages']
            if time.time() - init_time > self.TIMEOUT:
                raise TimeoutError()

        result_text = messages[0]['text']
        return result_text
