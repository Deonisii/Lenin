from slackclient import SlackClient
import time
from torch.logger import log


class Bot(object):
    # Bot User OAuth Access Token
    SLACK_BOT_TOKEN = 'xoxp-2177870734-383569581717-562428176902-3568c10bc4778439cba9ed9efde75e39'
    TEST_GROUP = '#torch_test_group'
    TIMEOUT = 5

    def __init__(self):
        self.sc = SlackClient(self.SLACK_BOT_TOKEN)

    def command(self, command_text: str) -> str:
        assert command_text
        log(log.DEBUG, 'Hubot send: %s', command_text)
        res = self.sc.api_call(
            "chat.postMessage",
            channel=self.TEST_GROUP,
            text="@hubot {}".format(command_text),
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
        log(log.DEBUG, 'Hubot recv: %s', result_text)
        return result_text

    def info(self, symbol: str) -> dict:
        assert symbol
        res = self.command('info {}'.format(symbol))
        lines = res[res.index('```') + 3:].rstrip('`')
        res = dict()
        for line in lines.split('\n'):
            fields = line.split()
            if len(fields) == 3:
                res[fields[0]] = fields[2]
        return res
