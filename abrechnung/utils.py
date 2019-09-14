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


def amount_to_string(amount):
  amount = int(amount)
  negative = amount < 0
  if negative:
    amount *= -1

  fractional_part = amount % 100
  integer_part = (amount - fractional_part) // 100

  ret = "{}.{:02d}".format(integer_part, fractional_part)
  if negative:
    ret = "-" + ret

  return ret


def parse_amount(s):
  try:
    return try_parse_with_delim(s, '.')
  except ValueError:
    pass

  try:
    return try_parse_with_delim(s, ',')
  except ValueError:
    pass

  try:
    return int(s) * 100
  except ValueError:
    pass

  raise ConversionError("Could not convert {} to an amount.".format(s))


def try_parse_with_delim(s, d):
  if d in s:
    ps = s.split(d)
    if len(ps) == 2:
      if len(ps[1]) == 2:
        return int(ps[0]) * 100 + int(ps[1]) * 1
      elif len(ps[1]) == 1:
        return int(ps[0]) * 100 + int(ps[1]) * 10
      elif len(ps[1]) == 0:
        return int(ps[0]) * 100
  raise ValueError

class ConversionError(Exception):
  pass
