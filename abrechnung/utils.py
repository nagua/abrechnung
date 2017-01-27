# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

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

class FuzzyDict:
  def __init__(self, items=[]):
    self.data = dict(items)
    self.threshold = 5

  def __setitem__(self, key, value):
    self.data[key] = value

  def __getitem__(self, key):
    dist, match = min((levenshtein(key, match), match) for match in self.data)
    if dist<self.threshold:
      return self.data[match]
    else:
      raise KeyError(key + " does not match any value")

  def __contains__(self, key):
    try:
      v = self[key]
      return True
    except KeyError:
      return False

class NormalizingDict:
  def __init__(self, items=[]):
    self.data = {}
    for k,v in items:
      self[k] = v

  def __setitem__(self, key, value):
    self.data[self.normalize(key)] = value

  def __getitem__(self, key):
    return self.data[self.normalize(key)]

  def __contains__(self, key):
    return self.normalize(key) in self.data

  def normalize(self, key):
    return key.lower()
