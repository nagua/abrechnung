# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

import time

class Transaction:

  def __init__(self, amount_in_euro, source, destination):
    str_amount_in_cents = amount_in_euro.replace('.', '').replace(',', '')
    self.amount_in_cents = int(str_amount_in_cents)
    self.source = source
    self.destination = destination
    self.date = time.localtime()

  def __repr__(self):
    transfer_text = "[Transaction] - Transfer: {amount} euro from: {from} to: {to}"
    return transfer_text.format(**{'amount': self.amount_in_cents/100, 'from': self.source, 'to': self.destination})
