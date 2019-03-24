from slackclient import SlackClient
import time
import os

WAIT_TIME = 1


class Bot(object):
    # Bot User OAuth Access Token
    SLACK_BOT_TOKEN = 'xoxp-56358677287-56354407024-565676558451-55d220a3b3082b4fe07fc473821b81bc'
    TEST_BOT_NAME = os.getenv('TEST_BOT_NAME', '@marx')
    TEST_GROUP = '#test_bots'
    TIMEOUT = 10*60

    def __init__(self, bot_name=TEST_BOT_NAME):
        print('SLACK_BOT_TOKEN', self.SLACK_BOT_TOKEN)
        print()
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
        assert res['ok'], res
        messages = None
        init_time = time.time()
        while True:
            time.sleep(WAIT_TIME)
            answer = self.sc.api_call('conversations.history', channel=res['channel'], oldest=res['ts'])
            print(answer)
            assert answer['ok']
            messages = answer['messages']
            if messages:
                return messages[0]['text']
            if time.time() - init_time > self.TIMEOUT:
                raise TimeoutError()
