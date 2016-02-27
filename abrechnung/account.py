# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

class Account:
  """
  Class that represents the account of a person

  Attributes:
  	- name
  	- balance
  """

  def __init__(self, name):
    self.name = name
    self.balance = 0

  def __repr__(self):
    account_data = "[account_data] - Name: {name} \t\t| Balance: {balance} \n"
    return account_data.format(**{'name': self.name, 'balance': self.balance / 100})
