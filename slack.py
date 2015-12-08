import json
import urllib2

import secrets

def response(text, extra_args=None):
  response = {
    "response_type": "in_channel"
  }
  if text:
    response['text'] = text
  if extra_args:
    response.update(extra_args)
  return response

def get_request_text(request):
  return request.params.get('text')

def send_message(text, extra_args=None):
  payload = response(text, extra_args=None)
  urllib2.urlopen(secrets.SLACK_INCOMING_WEBHOOK, json.dumps(payload))
