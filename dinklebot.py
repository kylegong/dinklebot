#!/usr/bin/env python2.7
'''
Use this to run dinklebot from the commandline.

Examples:
python dinklebot.py hi
python dinklebot.py item gj
'''

import sys

import commands

if __name__ == "__main__":
  command_text = ' '.join(sys.argv[1:])
  command, extra = commands.parse(command_text)
  if command.is_private:
    print '(Private)'
  print command(extra)
