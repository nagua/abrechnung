# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

import time

class Event:
  """Class that represents an event"""

  def __init__(self, cost_in_euro, payer, participants):
    self.cost_in_cents = int(float(cost_in_euro) * 100)
    self.payer = payer
    self.participants = participants
    self.balancing_operation = False
    self.date = time.localtime()
    self.remainder = ""

  def cost_per_person(self):
    """Calculate cost per person"""
    return self.cost_in_cents / len(self.participants)

  def add_remainder(self, remainder):
    self.remainder = remainder

  def __repr__(self):
  	event_text = "[add_event] - cost: {cost}, payer: {payer}, participants: {participants}"
  	return event_text.format(**{'cost': self.cost_in_cents, 'payer': self.payer, 'participants': self.participants})
