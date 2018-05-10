#!/usr/bin/env python3
# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

import unittest
import event as e
import transaction as t
import account as a
import group as g

def gen_test_group():
  """ some function for backwards compatibility (used in ipynb file)"""
  t = TestAccounting()
  t.setUp()
  t.test_group_balancing()
  return t.group

class TestAccounting(unittest.TestCase):
  def tearDown(self):
    """
    This is run after each and every test_* function
    """
    pass

  def setUp(self):
    """
    This is run before each and every test_* function
    """
    self.group = g.Group(0)
    
    # Add accounts
    self.group.add_account(a.Account("nicolas"))
    self.group.add_account(a.Account("max"))
    self.group.add_account(a.Account("sandrina"))
    self.group.add_account(a.Account("annika"))

  def test_group_balancing(self):
    """
    --------------------------------------------------------------------------
    This is the test function you want to execute!!!!
    --------------------------------------------------------------------------
    """
    events = [
      e.Event(30, "max", ["nicolas", "max", "sandrina"]),
      e.Event(20, "max", ["nicolas", "max", "sandrina"]),
      e.Event(50, "max", ["nicolas", "max", "sandrina", "annika"]),
      e.Event(30, "nicolas", ["nicolas", "max", "annika"]),
      e.Event(60.50, "nicolas", ["nicolas", "max", "sandrina"]),
    ]

    transactions = [
      t.Transaction(2.0, "nicolas", "max")
    ]

    # Add events
    for event in events:
      self.group.add_event(event)
      self.group.print_account_data()
      print()
      print(self.group.readable_account_data())
      self.assertTrue(self.group.check_balance())
      print()

    for transaction in transactions:
      self.group.do_transaction(transaction)
      self.group.print_account_data()
      print()
      print(self.group.readable_account_data())
      self.assertTrue(self.group.check_balance())
      print()

    # Calculate transactions needed to balance accounts
    self.group.calculate_balancing()

    return self.group

if __name__ == "__main__":
  unittest.main()
