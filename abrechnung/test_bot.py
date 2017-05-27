import unittest
from unittest.mock import Mock
from abrechnungsbot import AbrechnungsBot
from billingdata import BillingData
from group import Group

class TestAbrechnungsBot(unittest.TestCase):
    def setUp(self):
        self.groupid = 123
        self.billingdata = BillingData()

        self.botcfg = {"private_chat":self.groupid, "token":"Pa$$w0rd", "backup_file":None}
        self.bot = AbrechnungsBot(self.botcfg, self.billingdata)

        self.update_mock = Mock()
        self.update_mock.message.chat_id = self.groupid

        self.bot_mock = Mock()

        self.bot.start(Mock(), self.update_mock)

    def _group(self):
        return self.billingdata.groups[self.groupid]
    
    def test_add_acc(self):
        self.bot.add_account(self.bot_mock, self.update_mock, ["Ich"])

        self.assertEqual("Ich", self._group().accounts[0].name)
        
    def test_add_evt(self):
        self.bot.add_event(self.bot_mock, self.update_mock, [100, "Du", "Ich"])

        self.assertTrue(self.bot_mock.sendMessage.called)
        self.assertTrue(self.bot_mock.sendMessage.called_with(
            chat_id=self.groupid, 
            text="Event was added"
        ))
        

if __name__=='__main__':
    unittest.main()
