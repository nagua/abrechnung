#!/usr/bin/env python3
# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

from event import *
from account import *
from group import *

def levenshtein(s1, s2):
  """
  Calculates the levenshtein distance.
  Taken from: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
  """
  if len(s1) < len(s2):
    return levenshtein(s2, s1)

  # len(s1) >= len(s2)
  if len(s2) == 0:
    return len(s1)

  previous_row = range(len(s2) + 1)
  for i, c1 in enumerate(s1):
    current_row = [i + 1]
    for j, c2 in enumerate(s2):
      insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
      deletions = current_row[j] + 1       # than s2
      substitutions = previous_row[j] + (c1 != c2)
      current_row.append(min(insertions, deletions, substitutions))
    previous_row = current_row
 
  return previous_row[-1]

def gen_test_group():
  """
  -----------------------------------------------------------------------------------------
  This is the test function you want to execute!!!!
  -----------------------------------------------------------------------------------------
  """
  group = Group()
  
  # Add accounts
  group.add_account(Account("nicolas", 123))
  group.add_account(Account("max", 123))
  group.add_account(Account("sandrina", 123))
  group.add_account(Account("annika", 123))
  
  # Add events
  group.add_event(Event(30, "max", ["nicolas", "max", "sandrina"]))
  group.print_account_data()
  group.check_balance()
  print()

  group.add_event(Event(20, "max", ["nicolas", "max", "sandrina"]))
  group.print_account_data()
  group.check_balance()
  print()

  group.add_event(Event(50, "max", ["nicolas", "max", "sandrina", "annika"]))
  group.print_account_data()
  group.check_balance()
  print()

  group.add_event(Event(30, "nicolas", ["nicolas", "max", "annika"]))
  group.print_account_data()
  group.check_balance()
  print()

  group.add_event(Event(60.50, "nicolas", ["nicolas", "max", "sandrina"]))
  group.print_account_data()
  group.check_balance()
  print()

  # Calculate transactions needed to balance accounts
  group.calculate_balancing()

  return group

if __name__ == "__main__":
  gen_test_group()