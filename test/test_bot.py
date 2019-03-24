import unittest
from test.entity.bot import Bot


class TestBot(unittest.TestCase):

    def test_ping(self):
        bot = Bot()
        res = bot.command('ping')
        self.assertEqual(res, 'PONG')

    def test_1_plus_1(self):
        bot = Bot()
        self.assertEqual(2, int(bot.command('eval 1+1')))


if __name__ == '__main__':
    unittest.main()
