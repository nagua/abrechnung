# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

class Transaction:

  def __init__(self, amount, from_user, to_user):
    self.amount_in_cents = amount
    self.from_user = from_user
    self.to_user = to_user

  def __repr__(self):
    transfer_text = "[transaction] - Transfer: {amount} euro from: {from} to: {to}"
    return transfer_text.format(**{'amount': self.amount_in_cents/100, 'from': self.from_user, 'to': self.to_user})