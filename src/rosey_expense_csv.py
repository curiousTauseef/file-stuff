#!/usr/bin/env python
import re
import os
import sys
import glob
import fnmatch
from PyPDF2 import PdfFileMerger

good_date_regex = "^20[0-9]{2}-[0-9]{2}-[0-9]{2}" #YYYY-MM-DD
bad_date_regex = "^20[0-9]{2}-[0-9]{2}-[0-9]{2}-date" #YYYY-MM-DD-date
expense_group_regex = "[a-zA-Z]+-[a-zA-Z0-9]+" # Something-SomeThingNumber
good_date_pattern = re.compile("(" + good_date_regex + ")-(" + expense_group_regex + ")-(.*)-\$(.*)\.pdf")
bad_date_pattern = re.compile("(" + bad_date_regex + ")-(" + expense_group_regex + ")-(.*)-\$(.*)\.pdf")

class RoseyExpenseCsv():

  def __init__(self, files, match_string):
    self.files = files
    self.matching = find_matching_files(files, match_string)
    self.csv_lines = rosey_produce_report_lines(self.matching)

  def matching_files(self):
    return self.matching

  def report_lines(self):
    return self.csv_lines

  def cvs_from(self, filename):
    return rosy_file_to_cvs(filename)


def rosy_file_to_cvs(filename):
  date = "No date"
  expense_group = "No expense group"
  what = "No expense"
  amount = "No amount"
  problems = []

  adjusted_filename = filename.replace('--', '-')
  if adjusted_filename.find("-date") >= 0:
    adjusted_filename = adjusted_filename.replace("date-", "")
    problems += ["Date"]

  m = good_date_pattern.match(adjusted_filename)
  if not m:
    problems += ["Generally"]
  else:
    date = m.group(1)

  if m:
    expense_group = m.group(2)
    what = m.group(3).replace('-', ' ').lstrip()
    amount = m.group(4).replace(',', '')

  if amount.find("x") >= 0:
    problems += ["Amount"]

  # problems += check(amount, "x", "Amount")

  if what.find("$") >= 0:
    problems += ["$$"]
 
  if adjusted_filename.find("split") >= 0:
    problems += ["Split"]
 
  if adjusted_filename.find("cash") >= 0:
    problems += ["Cash"]
 
  message = make_message_from(problems)

  return '{0}, {1}, "{2}", {3}, {4}, "{5}"'.format(date, expense_group, what, amount, message, filename)

def check(value, containing, problem_name):
  if value.find(containing) >= 0:
    return [problem_name]
  else:
    return None


def make_message_from(problems):
  if len(problems) == 0:
    message = "OK"
  elif len(problems) == 1:
    message = problems[0] + " needs attention"
  else:
    message = problems[0] + " and " + problems[1] + " need attention"
  return message

def find_matching_files(files, match):
  matches = []
  select_pdf_files = ".*" + match + ".*\.pdf"
  pattern = re.compile(select_pdf_files.upper())
  for f in files:
    if pattern.match(f.upper()):
      matches += [f]
  return matches


def rosey_produce_report_lines(files):
  csv_lines = []
  for f in files:
    csv_lines += [rosy_file_to_cvs(f)]
  return csv_lines

def merge_receipts(path, pdf_files, output_filename):
  merger = PdfFileMerger()

  for pdf in pdf_files:
      merger.append(path + pdf)

  merger.write(output_filename)


def main(path, match):
  all_files = os.listdir(path)
  rosey_expense_csv = RoseyExpenseCsv(all_files, match)
  receipt_pdfs = rosey_expense_csv.matching_files()
  lines = rosey_expense_csv.report_lines()
  merge_receipts(path, receipt_pdfs, match + "-receipts.pdf")
  output = open(match + "-expenses.csv", "w") 
  output.write("Date, purpose, expense, amount, status, receipt file\n")

  for l in lines:
    output.write(l + "\n")
  output.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
      print "Usage: {0} path match-string {1}".format(sys.argv[0], len(sys.argv))
      exit(0)
    main(sys.argv[1], sys.argv[2])



