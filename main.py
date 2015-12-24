#!/usr/bin/env python

import json
import logging
import webapp2

import commands
import models
import slack

class CommandHandler(webapp2.RequestHandler):
  def post(self):
    logging.info('request params: %s', self.request.params)
    full_command_text = slack.get_request_text(self.request)
    command_runner = commands.CommandRunner(request=self.request)
    slack_response = command_runner.run(full_command_text)
    response_url = slack.get_response_url(self.request)
    slack.send_message(slack_response, webhook=response_url)

class SpoilerHandler(webapp2.RequestHandler):
  def get(self, key):
    spoiler = models.Spoiler.lookup(key)
    if not spoiler:
      return self.abort(404)
    return self.response.write(spoiler.message)

class DailyHandler(webapp2.RequestHandler):
  def get(self):
    command_runner = commands.CommandRunner()
    slack_response = command_runner.daily(None)
    slack.send_message(slack_response)
    return self.response.write(slack_response)

app = webapp2.WSGIApplication([
    ('/v1/', CommandHandler),
    webapp2.Route('/spoiler/<key>/', handler=SpoilerHandler,
                  name='spoiler'),
    ('/v1/cron/daily/', DailyHandler),
], debug=True)
