#!/usr/bin/python2

import os
import argparse
import tempfile
import re
import shutil

import sys

class RebaseIncludeRule:

    old_include_dir = None
    new_include_dir = None

    def __init__(self, old_include_dir, new_include_dir):
        self.old_include_dir = old_include_dir
        self.new_include_dir = new_include_dir

    def rebase(self, included_file):
        full_included_path = os.path.join(self.old_include_dir, included_file);
        return os.path.relpath(full_included_path, self.new_include_dir)


def rebase_include_line(file, included_file_path, rules):
    file_dir_path = os.path.dirname(file)
    for _, rule in rules.iteritems():
        if os.path.isfile(os.path.join(rule.old_include_dir, included_file_path)):
            return rule.rebase(included_file_path)
    sys.stdout.write("Include path '%s' cannot be resolved. Maybe included from a system dir, skipping it !\n" % included_file_path)


def rebase_includes_in_file(file, rules):
    new_handle, new_file_path = tempfile.mkstemp()
    new_file = os.fdopen(new_handle, 'w')
    with open(file) as f:
        sys.stdout.write("Processing file %s\n" % file)
        for line in f:
            stripped_line = line.strip()
            match_obj = re.match('#include "(.*)"', stripped_line)
            if match_obj == None: 
                new_file.write(line)
            else:
                try:
                    rebased_file_path = rebase_include_line(file, match_obj.group(1), rules)
                    rebased_line = '#include "%s"\n' % rebased_file_path
                    new_file.write(rebased_line)
                except:
                    new_file.write(line)

        new_file.close()
        shutil.copyfile(new_file_path, file)
        os.remove(new_file_path)


def rebase_includes_in_path(path, old_include_dirs, new_include_dir):
    rules = {}
    for old_include_dir in old_include_dirs:
        rules[old_include_dir] = RebaseIncludeRule(old_include_dir, new_include_dir)

    for root, dirs, files in os.walk(path):
        path = root.split('/')
        for file in files:
            rebase_includes_in_file(os.path.join(root, file), rules)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("new_include_dir", help="New dir used to rebase '#include's")
    parser.add_argument("old_include_dir", nargs='+', help="Old include dir to be rebased")
    args = parser.parse_args()
    old_include_dirs = args.old_include_dir
    rebase_rules = {}
    for old_include_dir in old_include_dirs:
        rebase_includes_in_path(old_include_dir, old_include_dirs, args.new_include_dir)


