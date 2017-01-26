# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

class Transaction:

  def __init__(self, amount, source, destination):
    self.amount_in_cents = amount
    self.source = source
    self.destination = destination
    self.date = time.localtime()

  def __repr__(self):
    transfer_text = "[transaction] - Transfer: {amount} euro from: {from} to: {to}"
    return transfer_text.format(**{'amount': self.amount_in_cents/100, 'from': self.source, 'to': self.destination})