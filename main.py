#!/usr/bin/env python

import json
import webapp2

import commands
import slack

class CommandHandler(webapp2.RequestHandler):
  def post(self):
    full_command_text = slack.get_text(self.request)
    slack_response = slack.response(commands.run(full_command_text))
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(slack_response))

app = webapp2.WSGIApplication([
    ('/v1/', CommandHandler)
], debug=True)
