# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
import time, random, copy

def levenshtein(s1, s2):
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
  group = Group()
  group.add_account(Account("nicolas", 123))
  group.add_account(Account("max", 123))
  group.add_account(Account("sandrina", 123))

  group.add_event(Event(30, "max", ["nicolas", "max", "sandrina"]))
  print("Check balance: " + group.check_balance() )
  group.calculate_balance()

  return group


class Group:
  accounts = []
  events = []

  def add_account(self, account):
    """Add an account to the group"""
    self.accounts.append(account)

  def add_event(self, event):
    """Add an event to this group and calculate the new balance"""
    self.events.append(event)
    
    #Only use whole payments and randomly put the remainder onto a account
    remainder = event.cost % len(event.participants)
    cost_per_person = ( event.cost - remainder) / len(event.participants)

    for acc in self.accounts:
      if acc.name == event.payer:
        acc.balance += event.cost

    for participant in event.participants:
      found = False
      for acc in self.accounts:
        #Use edit-distance here
        if acc.name == participant:
          found = True
          acc.balance -= cost_per_person
          break
      if not found:
        print("Person not found: " + participant)

    #Randomly add remainder costs to a participant
    rand_person = random.choice(event.participants)
    for acc in self.accounts:
      if rand_person == acc.name:
        acc.balance -= remainder

  def check_balance(self):
    """Check if all accounts adds up to zero"""
    result = 0
    for acc in self.accounts:
      result += acc.balance

    return result == 0

  def calculate_balancing(self):
    positive_accounts=[]
    negative_accounts=[]

    #Sort accounts into positive and negative ones
    for acc in self.accounts:
      if acc.balance < 0:
        negative_accounts.append(copy.copy(acc))
      else:
        positive_accounts.append(copy.copy(acc))

    transfer_text = "Transfer: {amount} from: {from} to: {to}"
    #For every negative account find a positive one to that the tansaction has to go to.

    for neg in negative_accounts:
      for pos in positive_accounts:
        if neg.balance == 0:
          break

        if pos.balance != 0:
          if pos.balance >= -neg.balance:
            #There is enough credit on the pos so neg has to transfer all to him
            print(transfer_text.format(**{'amount': -neg.balance, 'from': neg.name, 'to': pos.name}))
            pos.balance += neg.balance
          else:
            #There is not enough credit on pos so neg has to transfer a part to him
            print(transfer_text.format(**{}))
            


class Account:
  """Class that represents the account of a person"""
  group=0
  balance=0
  name=""

  def __init__(self, name, group):
    self.name = name
    self.group = group


class Event:
  """Class that represents an event"""
  cost=0
  payer=""
  participants=[]

  def __init__(self, cost, payer, participants):
    self.cost = cost
    self.payer = payer
    self.participants = participants
    self.date = time.localtime()

  def costPerPerson(self):
    """Calculate cost per person"""
    return self.cost / len(self.persons)


