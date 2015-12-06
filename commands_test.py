#!/usr/bin/env python2.7

import sys

import commands

if __name__ == "__main__":
  command_text = ' '.join(sys.argv[1:])
  print commands.run(command_text)
