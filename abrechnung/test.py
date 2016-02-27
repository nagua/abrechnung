#!/usr/bin/env python3
# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

import event as e
import account as a
import group as g

def gen_test_group():
  """
  -----------------------------------------------------------------------------------------
  This is the test function you want to execute!!!!
  -----------------------------------------------------------------------------------------
  """
  group = g.Group(0)
  
  # Add accounts
  group.add_account(a.Account("nicolas"))
  group.add_account(a.Account("max"))
  group.add_account(a.Account("sandrina"))
  group.add_account(a.Account("annika"))
  
  # Add events
  group.add_event(e.Event(30, "max", ["nicolas", "max", "sandrina"]))
  group.print_account_data()
  group.check_balance()
  print()

  group.add_event(e.Event(20, "max", ["nicolas", "max", "sandrina"]))
  group.print_account_data()
  group.check_balance()
  print()

  group.add_event(e.Event(50, "max", ["nicolas", "max", "sandrina", "annika"]))
  group.print_account_data()
  group.check_balance()
  print()

  group.add_event(e.Event(30, "nicolas", ["nicolas", "max", "annika"]))
  group.print_account_data()
  group.check_balance()
  print()

  group.add_event(e.Event(60.50, "nicolas", ["nicolas", "max", "sandrina"]))
  group.print_account_data()
  group.check_balance()
  print()

  # Calculate transactions needed to balance accounts
  group.calculate_balancing()

  return group

if __name__ == "__main__":
  gen_test_group()