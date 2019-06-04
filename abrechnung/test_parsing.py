#!/usr/bin/env python3
# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

import unittest
import utils as u

class TestAmountParsing(unittest.TestCase):
  def test_simple_dot(self):
    self.assertEqual(u.parse_amount("3.6"), 360)
    self.assertEqual(u.parse_amount("3.60"), 360)
    self.assertEqual(u.parse_amount("3."), 300)

  def test_simple_comma(self):
    self.assertEqual(u.parse_amount("3,6"), 360)
    self.assertEqual(u.parse_amount("3,60"), 360)
    self.assertEqual(u.parse_amount("3,"), 300)

  def test_without_delim(self):
    self.assertEqual(u.parse_amount("3"), 300)

  def test_error(self):
    with self.assertRaises(u.ConversionError):
      u.parse_amount("troll")

  def test_error_dot(self):
    with self.assertRaises(u.ConversionError):
      u.parse_amount("3.troll")

    with self.assertRaises(u.ConversionError):
      u.parse_amount("3.tr")

    with self.assertRaises(u.ConversionError):
      u.parse_amount("3.333")

  def test_error_comma(self):
    with self.assertRaises(u.ConversionError):
      u.parse_amount("3,troll")

    with self.assertRaises(u.ConversionError):
      u.parse_amount("3,tr")

    with self.assertRaises(u.ConversionError):
      u.parse_amount("3,333")

if __name__ == "__main__":
  unittest.main()
