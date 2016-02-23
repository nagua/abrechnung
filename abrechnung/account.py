class Account:
  """Class that represents the account of a person"""

  def __init__(self, name, account_id):
    self.name = name
    self.balance = 0
    self.account_id = account_id