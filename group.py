import random, copy, time

class Group:
  """
  This class represents a group that shares money.
  And has events to where money was spend and
  distributes the cost to the participants.
  """
  def __init__(self):
    self.accounts = []
    self.events = []
    self.group_id = 0

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
        
  def __repr__(self):
    """Print all account details of this group"""
    ret = ""
    account_data = "[print_account_data] - Name: {name} \t| Balance: {balance} \n"
    ret += "[print_account_data] - Account details: \n"
    for acc in self.accounts:
      ret += account_data.format(**{'name': acc.name, 'balance': acc.balance})
    return ret

  def print_account_data(self):
  	print(str(self))

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