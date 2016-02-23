import time

class Event:
  """Class that represents an event"""

  def __init__(self, cost_in_euro, payer, participants):
    self.cost_in_cents = int(cost_in_euro * 100)
    self.payer = payer
    self.participants = participants
    self.date = time.localtime()

  def cost_per_person(self):
    """Calculate cost per person"""
    return self.cost_in_cents / len(self.participants)