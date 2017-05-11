class BillingData:
  def __init__(self):
    self.version = 1
    self.groups = []

  def update(self):
    if self.version == 0:
      print("Update to version 1")
      for key, group in self.groups.items():
        setattr(group, 'transactions', [])
        for event in group.events:
          setattr(event, 'remainder_person', '')
      self.version = 1
