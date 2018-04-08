from rosey import *

import unittest
import mock
from mock import MagicMock

file1_glob  = "/path/receipts/bus *.pdf"
file1_remove = "bus "
file1_dest = "/business/current-receipts/"
file2_glob  = "/path/receipts/per *.pdf"
file2_remove = "per "
file2_dest = "/personal/current-receipts/"
config1 = [
      [file1_glob, file1_remove, file1_dest]
      ]
config2 = [
      [file1_glob, file1_remove, file1_dest],
      [file2_glob, file2_remove, file2_dest]
       ]

mockGlob = MagicMock()
mockTime = MagicMock()

@mock.patch('glob.glob', mockGlob)
@mock.patch('os.path.getctime', mockTime)
class RoseyTest(unittest.TestCase):

  def setUp(self):
    mockGlob.reset_mock()
    mockTime.reset_mock()
    self.addCleanup(self.unpatch)

  def unpatch(self):
    mockGlob.stop()
    mockTime.stop()

  def test_clean_up_config_file(self):
    lines = [
      "/orig/path/bus *.pdf , bus, /dest/path/business-receipts/",
      "/orig/path/per *.pdf, per , /dest/path/personal-receipts/",
      "/orig/path/tax *.pdf, tax, /dest/path/tax-docs/" ,
      "/orig/path/med *.pdf , med  , /dest/path/med-docs/"
    ]
    clean_config = cleanup_config(lines)
    expected = [
      ['/orig/path/bus *.pdf', 'bus', '/dest/path/business-receipts/'],
      ['/orig/path/per *.pdf', 'per', '/dest/path/personal-receipts/'],
      ['/orig/path/tax *.pdf', 'tax', '/dest/path/tax-docs/'],
      ['/orig/path/med *.pdf', 'med', '/dest/path/med-docs/']
    ]
    self.assertEqual(expected, clean_config)

  def test_no_config_file(self):
    pass
  
  def test_duplicate_config_pattern_fails(self):
    pass
  
  def test_unique_config_patterns_succeed(self):
    pass
  
  def test_no_matches_no_action(self):
    mockGlob.side_effect = [[]]
    rosey = Rosey(config1)
    files = rosey.FileMoveToDoList()
    assert [] == files
    mockGlob.assert_called_with(file1_glob)

  def test_replacePatternWithNewPath(self):
    rosey = Rosey(config1)
    file1 = "/path/receipts/bus CoDe hotel $120.99.pdf"
    mockTime.return_value = 1505597108.0
    mockGlob.side_effect = [[file1]]
    newpath = rosey.replacePatternWithNewPath(file1, "bus ", "/new/path/")
    self.assertEqual("/new/path/2017-09-16-CoDe-hotel-$120.99.pdf", newpath)


  def test_finder_finds_one(self):
    file1 = "bus CoDe.pdf"
    mockTime.return_value = 1505597108.0
    expected = [
          [file1, file1_dest + "2017-09-16-CoDe.pdf"],
        ]
    mockGlob.side_effect = [[file1]]

    rosey = Rosey(config1)
    todo = rosey.FileMoveToDoList()
    self.assertEqual(expected, todo)
    mockGlob.assert_called_with(file1_glob)

  def test_finder_finds_two_for_one_diectory(self):
    file1 = "bus CoDe 1.pdf"
    file2 = "bus CoDe 2.pdf"
    mockTime.return_value = 1505597108.0
    expected = [
          [file1, file1_dest + "2017-09-16-CoDe-1.pdf"],
          [file2, file1_dest + "2017-09-16-CoDe-2.pdf"]
        ]
    mockGlob.side_effect = [[file1, file2]]

    rosey = Rosey(config1)
    todo = rosey.FileMoveToDoList()
    self.assertEqual(expected, todo)
    mockGlob.assert_called_with(file1_glob)

  def test_finder_finds_two_files_from_two_diectories(self):
    file1 = "bus CoDe 1.pdf"
    file2 = "per CoDe 2.pdf"
    mockGlob.side_effect = [[file1],[file2]]
    mockTime.return_value = 1505597108.0

    rosey = Rosey(config2)
    todo = rosey.FileMoveToDoList()

    expected = [
          [file1, file1_dest + "2017-09-16-CoDe-1.pdf"],
          [file2, file2_dest + "2017-09-16-CoDe-2.pdf"]
        ]

    self.assertEqual(expected, todo)
    # mockGlob.assert_called_with(file1_glob)

  def test_mutiple_spaces_become_one(self):
    file1 = "bus CoDe 1  Dinner   $34.56.pdf"
    mockGlob.side_effect = [[file1]]
    mockTime.return_value = 1505597108.0

    rosey = Rosey(config1)
    todo = rosey.FileMoveToDoList()

    expected = [
          [file1, file1_dest + "2017-09-16-CoDe-1-Dinner-$34.56.pdf"]
        ]

    self.assertEqual(expected, todo)
    # mockGlob.assert_called_with(file1_glob)






  # def test_finder_finds_one_matching_file_with_one_config_line(self):
  #   files = ["/path/receipts/bus CoDe hotel $120.99.pdf"]
  #   mockGlob.side_effect = [files]
  #   finder = FileFinder(config1)
  #   self.assertEqual(files, finder.find())

  # def test_finder_finds_two_matching_files_with_two_config_line(self):
  #   file1 = "/path/receipts/bus CoDe hotel $120.99.pdf"
  #   file2 = "/path/receipts/per FLA hotel $320.99.pdf"
  #   return_values = [
  #         [file1],
  #         [file2]
  #       ]
  #   expected_files = [file1, file2]
  #   mockGlob.side_effect = return_values
  #   finder = FileFinder(config2)
  #   self.assertEqual(expected_files, finder.find())
  #   self.assertEqual(2, mockGlob.call_count)
  #   # mockGlob.assert_called_with([file1_regex, file2_regex])




# cwd = os.getcwd()
# glob.glob("/Users/james/Dropbox/receipts/bus*.pdf")


