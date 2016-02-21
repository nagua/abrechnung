# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
import time, random, copy

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


class Group:
  accounts = []
  events = []
  group_id = 0

  def __init__(self):
    accounts = []
    events = []
    group_id = 0

  def add_account(self, account):
    """Add an account to the group"""
    self.accounts.append(account)

  def add_event(self, event):
    """Add an event to this group and calculate the new balance"""
    self.events.append(event)

    # Only use whole payments and randomly put the remainder onto a account
    remainder = event.cost_in_cents % len(event.participants)
    cost_per_person = ( event.cost_in_cents - remainder) / len(event.participants)
    
    event_text = "[add_event] - cost: {cost}, payer: {payer}, participants: {participants}"
    add_event_text = "[add_event] - cost_per_person: {cost_per_person}, remainder: {remainder}"
    print(event_text.format(**{'cost': event.cost_in_cents, 'payer': event.payer, 'participants': event.participants}))
    print(add_event_text.format(**{'cost_per_person': cost_per_person, 'remainder': remainder}))

    
    # The payer gets all credits to his account
    for acc in self.accounts:
      if acc.name == event.payer:
        acc.balance += event.cost_in_cents

    # All participants get the cost_per_person to his account
    for participant in event.participants:
      found = False
      for acc in self.accounts:
        #Use edit-distance here
        if acc.name == participant:
          found = True
          acc.balance -= cost_per_person
          break
      if not found:
        # We should throw an exception here
        print("[add_event] - Person not found: " + participant)

    # Randomly add remainder costs to a participant
    if remainder != 0:
      rand_person = random.choice(event.participants)
      print("[add_event] - Extra remainder goes to: " +  rand_person)
      for acc in self.accounts:
        if rand_person == acc.name:
          acc.balance -= remainder
        
  def print_account_data(self):
    """Print all account details of this group"""
    account_data = "[print_account_data] - Name: {name} \t| Balance: {balance}"
    print("[print_account_data] - Account details: ")
    for acc in self.accounts:
      print(account_data.format(**{'name': acc.name, 'balance': acc.balance}))

  def check_balance(self):
    """Check if all accounts adds up to zero"""
    result = 0
    for acc in self.accounts:
      result += acc.balance

    print("[check_balance] - " + str(result == 0))
    return result == 0

  def calculate_balancing(self):
    """Calculate the transactions needed to balance all accounts"""
    positive_accounts=[]
    negative_accounts=[]

    # Sort accounts into positive and negative ones and make a copy of them
    for acc in self.accounts:
      if acc.balance < 0:
        negative_accounts.append(copy.copy(acc))
      else:
        positive_accounts.append(copy.copy(acc))

    transfer_text = "[calculate_balancing] - Transfer: {amount} from: {from} to: {to}"
    
    # For every negative account find a positive one to that the tansaction has to go to.
    for neg in negative_accounts:
      for pos in positive_accounts:
        if neg.balance == 0:
          break

        if pos.balance != 0:
          if pos.balance >= -neg.balance:
            #There is enough credit on the pos so neg has to transfer all to him
            print(transfer_text.format(**{'amount': -neg.balance, 'from': neg.name, 'to': pos.name}))
            pos.balance += neg.balance
            neg.balance = 0
          else:
            #There is not enough credit on pos so neg has to transfer a part to him
            print(transfer_text.format(**{'amount': pos.balance, 'from': neg.name, 'to': pos.name}))
            neg.balance += pos.balance
            pos.balance = 0

  def do_balancing(self):
    """Calculate the transactions and reset the account balance"""
    self.calculate_balancing()

    # Poor mans balancing ;)
    # The transactions have to be done from the actual humans
    for acc in self.accounts:
      acc.balance = 0


class Account:
  """Class that represents the account of a person"""
  
  balance = 0
  name = ""
  account_id = 0

  def __init__(self, name, account_id):
    self.name = name
    self.account_id = account_id

class Event:
  """Class that represents an event"""
  
  cost_in_cent = 0
  payer = ""
  participants = []

  def __init__(self, cost_in_euro, payer, participants):
    self.cost_in_cents = int(cost_in_euro * 100)
    self.payer = payer
    self.participants = participants
    self.date = time.localtime()

  def cost_per_person(self):
    """Calculate cost per person"""
    return self.cost_in_cents / len(self.participants)
