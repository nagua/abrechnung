# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

import time
import utils

class Transaction:

  def __init__(self, amount_in_euro, source, destination):
    self.amount_in_cents = utils.parse_amount(amount_in_euro)
    self.source = source
    self.destination = destination
    self.date = time.localtime()

  def __repr__(self):
    transfer_text = "[Transaction] - Transfer: {amount} euro from: {from} to: {to}"
    return transfer_text.format(**{'amount': self.amount_in_cents/100, 'from': self.source, 'to': self.destination})
