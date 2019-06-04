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

def parse_amount(s):
  parse = try_parse_with_delim(s, '.')
  if parse:
    return parse
  parse = try_parse_with_delim(s, '.')
  if parse:
    return parse
  return int(s)

def try_parse_with_delim(s, d):
  if d in s:
    ps = s.split(d)
    if len(ps) == 2 and len(ps[1]) <= 2:
      return int(ps[0]) * 100 + int(ps[1])
    else:
      raise ConversionError("Could not convert {} to an amount.".format(s))
  return None

class ConversionError(Exception):
  pass
