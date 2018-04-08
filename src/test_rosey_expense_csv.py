from rosey_expense_csv import *

import unittest
import mock
from mock import MagicMock

# Example input filenames
# 2017-09-16-Sioux-1-ref-$5.99.pdf
# 2017-09-16-code-sthlm-train-sat--$35.xx.pdf
# 2017-09-18-CoDe-CPH-SHTLM-UA-$4,306.26.pdf
# 2017-09-18-Sioux-1-breakfast-$7.91.pdf
# 2017-09-18-Sioux-1-breakfast--$5.21.pdf
# 2017-09-18-Sioux-1-food-$16.58.pdf
# 2017-09-18-Sioux-1-train-$80.xx.pdf
# 2017-09-18-apple-computer-W531462903--$3,366.00-.pdf
# 2017-09-20-date-annual-meeting-hotel--$552.44.pdf

class RoseyExpenseCsvTest(unittest.TestCase):

  def test_nominal_case(self):
    filename = '2017-09-16-Sioux-1-ref-$5.99.pdf'
    expected_csv = '2017-09-16, Sioux-1, "ref", 5.99, OK, "2017-09-16-Sioux-1-ref-$5.99.pdf"'
    self.assertEqual(expected_csv, rosy_file_to_cvs(filename))

  def test_commas_removed_from_numbers(self):
    filename = '2017-09-16-Sioux-1-ref,beer-$5,555.99.pdf'
    expected_csv = '2017-09-16, Sioux-1, "ref,beer", 5555.99, OK, "2017-09-16-Sioux-1-ref,beer-$5,555.99.pdf"'
    self.assertEqual(expected_csv, rosy_file_to_cvs(filename))

  def test_hyphens_removed_from_purchase_name(self):
    filename = '2017-09-16-Sioux-1-desert-ice-cream-$5,555.99.pdf'
    expected_csv = '2017-09-16, Sioux-1, "desert ice cream", 5555.99, OK, "2017-09-16-Sioux-1-desert-ice-cream-$5,555.99.pdf"'
    self.assertEqual(expected_csv, rosy_file_to_cvs(filename))

  def test_multiple_hyphens_treated_as_one(self):
    filename = '2017-09-16--Sioux-1----desert-ice-cream--$5,555.99.pdf'
    expected_csv = '2017-09-16, Sioux-1, "desert ice cream", 5555.99, OK, "2017-09-16--Sioux-1----desert-ice-cream--$5,555.99.pdf"'
    self.assertEqual(expected_csv, rosy_file_to_cvs(filename))

  def test_receipt_date_needs_attention(self):
    filename = '2017-09-16-date-AOTB-2017-Lunch-mon-$11.22.pdf'
    expected_csv = '2017-09-16, AOTB-2017, "Lunch mon", 11.22, Date needs attention, "2017-09-16-date-AOTB-2017-Lunch-mon-$11.22.pdf"'
    self.assertEqual(expected_csv, rosy_file_to_cvs(filename))

  def test_receipt_date_in_what_needs_attention(self):
    filename = '2017-09-16-AOTB-2017-date-Lunch-mon-$11.22.pdf'
    expected_csv = '2017-09-16, AOTB-2017, "Lunch mon", 11.22, Date needs attention, "2017-09-16-AOTB-2017-date-Lunch-mon-$11.22.pdf"'
    self.assertEqual(expected_csv, rosy_file_to_cvs(filename))

  def test_amount_needs_attention(self):
    filename = '2017-09-16-WEB-12-Dinner-$42.xx.pdf'
    expected_csv = '2017-09-16, WEB-12, "Dinner", 42.xx, Amount needs attention, "2017-09-16-WEB-12-Dinner-$42.xx.pdf"'
    self.assertEqual(expected_csv, rosy_file_to_cvs(filename))

  def test_date_and_amount_need_attention(self):
    filename = '2017-09-16-date-WEB-12-Dinner-$42.xx.pdf'
    expected_csv = '2017-09-16, WEB-12, "Dinner", 42.xx, Date and Amount need attention, "' + filename + '"'
    self.assertEqual(expected_csv, rosy_file_to_cvs(filename))

  def test_amount_needs_attention_when_two_dollar_signs(self):
    filename = '2017-09-16-WEB-12-Dinner-$42.42-$12.42.pdf'
    expected_csv = '2017-09-16, WEB-12, "Dinner $42.42", 12.42, $$ needs attention, "' + filename + '"'
    self.assertEqual(expected_csv, rosy_file_to_cvs(filename))

  def test_split_needs_attention(self):
    filename = '2017-09-16-WEB-12-split-dinner-$12.42.pdf'
    expected_csv = '2017-09-16, WEB-12, "split dinner", 12.42, Split needs attention, "' + filename + '"'
    self.assertEqual(expected_csv, rosy_file_to_cvs(filename))

  def test_cash_needs_attention(self):
    filename = '2017-09-16-WEB-12-dinner-$12.42-cash.pdf'
    expected_csv = '2017-09-16, WEB-12, "dinner", 12.42-cash, Cash needs attention, "' + filename + '"'
    self.assertEqual(expected_csv, rosy_file_to_cvs(filename))

  def test_generally_needs_attention(self):
    filename = '2017-09-16-WEB-12.pdf'
    expected_csv = 'No date, No expense group, "No expense", No amount, Generally needs attention, "' + filename + '"'
    self.assertEqual(expected_csv, rosy_file_to_cvs(filename))

  def test_select_pdfs_case_insensitive(self):
    filenames = [
        '2017-09-16-WEB-12-dinner-$23.99.pdf',
        '2017-09-16-Business-Meeting-dinner-$93.99.pdf',
        '2017-09-16-Web-12-Lunch-$23.99.pdf']

    expected_filename = ["2017-09-16-WEB-12-dinner-$23.99.pdf","2017-09-16-Web-12-Lunch-$23.99.pdf"]
    self.assertEqual(expected_filename, find_matching_files(filenames, "web-12"))

def test_select_pdfs_case_insensitive(self):
    filenames = [
        '2017-09-16-WEB-12-dinner-$23.99.pdf',
        '2017-09-16-Web-12-Lunch-$23.99.pdf']

    expected_csv = ['2017-09-16, WEB-12, "dinner", 23.99, OK, "2017-09-16-WEB-12-dinner-$23.99.pdf"',
                   '2017-09-16, Web-12, "Lunch", 23.99, OK, "2017-09-16-Web-12-Lunch-$23.99.pdf"']
    self.assertEqual(expected_csv, rosey_produce_report_lines(filenames))

