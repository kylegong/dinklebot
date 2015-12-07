#!/usr/bin/env python2.7
"""Use this to run dinklebot from the commandline.

The --slack flag can be used to show the full slack response as JSON.

Examples:
python dinklebot.py --slack hi
python dinklebot.py item gj
"""

import argparse
import json
import sys

import commands


parser = argparse.ArgumentParser('Runs a dinklebot command.')
parser.add_argument('--slack', action="store_true",
                    help=('If True, show full slack response. '
                          'Otherwise just show the text. '
                          'If there is no text, will show slack response.'))

if __name__ == "__main__":
  args, command = parser.parse_known_args()
  command_text = ' '.join(command)
  slack_response = commands.run(command_text)
  if args.slack or not slack_response.has_key('text'):
    print json.dumps(slack_response, indent=2)
  else:
    print slack_response['text']
