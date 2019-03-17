import unittest
from .entity.bot import Bot


class TestBot(unittest.TestCase):

    def test_ping(self):
        bot = Bot('@marx')
        res = bot.command('ping')
        self.assertEqual(res, 'PONG')


if __name__ == '__main__':
    unittest.main()
