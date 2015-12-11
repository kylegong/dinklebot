#!/usr/bin/env python

import json
import logging
import webapp2

import commands
import slack

class CommandHandler(webapp2.RequestHandler):
  def post(self):
    logging.info('request params: %s', self.request.params)
    full_command_text = slack.get_request_text(self.request)
    slack_response = commands.run(full_command_text)
    response_url = slack.get_response_url(self.request)
    slack.send_message(slack_response, webhook=response_url)

class DailyHandler(webapp2.RequestHandler):
  def get(self):
    slack_response = commands.daily(None)
    slack.send_message(slack_response)
    return self.response.write(slack_response)

app = webapp2.WSGIApplication([
    ('/v1/', CommandHandler),
    ('/v1/cron/daily/', DailyHandler),
], debug=True)
