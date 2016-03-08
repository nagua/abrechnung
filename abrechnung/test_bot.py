import unittest
from unittest.mock import Mock
from abrechnungsbot import AbrechnungsBot

class TestAbrechnungsBot(unittest.TestCase):
    def setUp(self):
        self.groupid = 123
        self.groups = {}
        self.botcfg = {"private_chat":self.groupid, "token":"Pa$$w0rd"}
        self.bot = AbrechnungsBot(self.botcfg, self.groups)

        self.update_mock = Mock()
        self.update_mock.message.chat_id = self.groupid

        self.bot_mock = Mock()

        self.bot.start(Mock(), self.update_mock)
        self.group = self.groups[self.groupid]
    
    def test_add_acc(self):
        self.bot.add_account(self.bot_mock, self.update_mock, ["Ich"])

        self.assertEqual("Ich", self.group.accounts[0].name)
        
    def test_add_evt(self):
        self.bot.add_event(self.bot_mock, self.update_mock, [100, "Du", "Ich"])

        self.assertTrue(self.bot_mock.sendMessage.called)
        self.assertTrue(self.bot_mock.sendMessage.called_with(
            chat_id=self.groupid, 
            text="Event was added"
        ))
        

if __name__=='__main__':
    unittest.main()
