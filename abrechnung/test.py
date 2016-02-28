#!/usr/bin/env python3
# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

import unittest
import event as e
import account as a
import group as g

def gen_test_group():
  """ some function for backwards compatibility """
  t = TestAccounting()
  t.run()
  return t.group

class TestAccounting(unittest.TestCase):
  def tearDown(self):
    pass

  def setUp(self):
    group = g.Group(0)
    
    # Add accounts
    group.add_account(a.Account("nicolas"))
    group.add_account(a.Account("max"))
    group.add_account(a.Account("sandrina"))
    group.add_account(a.Account("annika"))

    self.group = group

  def test_group_balancing(self):
    """
    --------------------------------------------------------------------------
    This is the test function you want to execute!!!!
    --------------------------------------------------------------------------
    """
    group = self.group
    
    events = [
      e.Event(30, "max", ["nicolas", "max", "sandrina"]),
      e.Event(20, "max", ["nicolas", "max", "sandrina"]),
      e.Event(50, "max", ["nicolas", "max", "sandrina", "annika"]),
      e.Event(30, "nicolas", ["nicolas", "max", "annika"]),
      e.Event(60.50, "nicolas", ["nicolas", "max", "sandrina"]),
    ]

    # Add events
    for event in events:
      group.add_event(event)
      group.print_account_data()
      self.assertTrue(group.check_balance())
      print()

    # Calculate transactions needed to balance accounts
    group.calculate_balancing()

    return group

if __name__ == "__main__":
  unittest.main()
