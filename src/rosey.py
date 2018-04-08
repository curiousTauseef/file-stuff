#!/usr/bin/env python
import glob
import os
import sys
import time
import re
import shutil
from os.path import expanduser
home = expanduser("~")
rosey_dir = home + "/.rosey/"
rosey_config = rosey_dir + "config"
rosey_log = rosey_dir + "rosey.log"

class Rosey():

  def __init__(self, config):
    """Configs come one in a list of three member lists"""
    """glob-file-pattern-to-match, prefix to remove, directory-to-move-matched-files"""
    self.config = config

  def FileMoveToDoList(self):
    files = []
    todos = []
    configs = iter(self.config)
    for config in configs:
      files = self.findMatchingFiles(config[0])
      for f in files:
        todos +=  [
          [f, self.replacePatternWithNewPath(f, config[1], config[2])]
        ]

    return todos

  def replacePatternWithNewPath(self, file, remove_this, dest_path):
    t = time.localtime(os.path.getctime(file))
    timestamp = time.strftime("%Y-%m-%d", t) + "-"
    orig_name = os.path.basename(file)
    trimmed_name = orig_name.replace(remove_this, "")
    no_spaces_name = trimmed_name.replace(" ", "-")
    timestamped_name = timestamp + no_spaces_name
    new_name = re.sub("-+", "-", timestamped_name)
    new_path = dest_path + new_name
    return new_path

  def findMatchingFiles(self, glob_spec):
    all = glob.glob(glob_spec)
    return all


def check_config(config):
  findings = []
  regexes = [f[0] for f in config]
  if (regexes.sort() != list(set(regexes)).sort()):
    findings += "You have one or more duplicate patterns"
    return

  dest_dirs = [f[2] for f in config]
  for dest in dest_dirs:
    if (not os.path.isdir(dest)):
      findings += "Destination directory does not exist: '{0}'".format(dest)

  return findings

def cleanup_config(config):
  config_list = [line.rstrip().split(',') for line in config]
  trimmed_config = []
  for config_item in config_list:
    trimmed_config += [[f.lstrip().rstrip() for f in config_item]]

  return trimmed_config

def moveEm(todo, really_move = True):

  with open(rosey_log, "a") as myfile:
      for t in todo:
        message = "Moving: {0}\n    to: {1}\n".format(t[0], t[1])

        if really_move:
          try:
            shutil.move(t[0], t[1])
            message += "      : Move Successful"
          except Exception as e:
            message += "      : Move Fails {0}.".format(e)

          myfile.write(message + "\n");
        print message

def show_findings(findings):
  for f in findings:
    print f

def main(arg):

  if (not os.path.exists(rosey_config)):
    print "You need to create ~/.rosey/config"
    exit(1)

  with open(rosey_config) as f:
    config = f.readlines()

  clean_config = cleanup_config(config)
  findings = check_config(clean_config)
  if findings != []:
    show_findings(findings)
    exit(1)
  rosey = Rosey(clean_config)
  todo = rosey.FileMoveToDoList()
  if arg == "move":
    moveEm(todo)
  if arg == "show":
    moveEm(todo, False)

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print "usage: {0} [move, show] {1}".format(sys.argv[0], len(sys.argv))
    exit(0)
  main(sys.argv[1]) # Run the example

