#!/usr/bin/env python2.7
"""Use this to run dinklebot from the commandline.

Returns the full slack response as JSON.

Examples:
python dinklebot.py hi
python dinklebot.py item gj
"""

import json
import sys

import commands

if __name__ == "__main__":
  command_text = ' '.join(sys.argv[1:])
  command_runner = commands.CommandRunner()
  slack_response = command_runner.run(command_text)
  print json.dumps(slack_response, indent=2)
