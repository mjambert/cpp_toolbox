#!/usr/bin/python2

import unittest

from rebase_includes import RebaseIncludeRule


class RebaseIncludeRuleTest(unittest.TestCase):

	def test_rebase_on_deeper_include_dir(self):
		rule = RebaseIncludeRule(old_include_dir = "dir1", new_include_dir = "dir1/dir2")
		self.assertEqual("../file.h", rule.rebase("file.h"))

	def test_rebase_on_far_deeper_include_dir(self):
		rule = RebaseIncludeRule(old_include_dir = "dir1", new_include_dir = "dir1/dir2/dir3/dir4")
		self.assertEqual("../../../file.h", rule.rebase("file.h"))

	def test_rebase_on_upper_include_dir(self):
		rule = RebaseIncludeRule(old_include_dir = "dir1/dir2", new_include_dir = "dir1")
		self.assertEqual("dir2/file.h", rule.rebase("file.h"))

	def test_rebase_on_far_upper_include_dir(self):
		rule = RebaseIncludeRule(old_include_dir = "dir1/dir2/dir3/dir4", new_include_dir = "dir1")
		self.assertEqual("dir2/dir3/dir4/file.h", rule.rebase("file.h"))

	def test_rebase_on_unrelated_include_dir(self):
		rule = RebaseIncludeRule(old_include_dir = "dir1/dir2/dir3", new_include_dir = "dir4")
		self.assertEqual("../dir1/dir2/dir3/file.h", rule.rebase("file.h"))


if __name__ == '__main__':
	unittest.main()

