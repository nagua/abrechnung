# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

import time
import utils

class Event:
  """Class that represents an event"""

  def __init__(self, cost_in_euro, payer, participants):
    self.cost_in_cents = utils.parse_amount(cost_in_euro)
    self.payer = payer
    self.participants = participants
    self.balancing_operation = False
    self.date = time.localtime()
    self.remainder_person = ""

  def cost_per_person(self):
    """Calculate cost per person"""
    return self.cost_in_cents / len(self.participants)

  def add_remainder_person(self, remainder_person):
    self.remainder_person = remainder_person

  def __repr__(self):
    event_text = "[Event] - cost: {cost}, payer: {payer}, participants: {participants}, remainder person: {remainder_person}"
    return event_text.format(**{'cost': self.cost_in_cents, 'payer': self.payer, 'participants': self.participants, 'remainder_person': self.remainder_person})
