import json
import logging
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

def in_channel(response):
  response["response_type"] = "in_channel"
  return response

def ephemeral(response):
  response["response_type"] = "ephemeral"
  return response

def get_request_text(request):
  return request.params.get('text')

def get_response_url(request):
  return request.params.get('response_url')

def send_message(message_dict, webhook=secrets.SLACK_INCOMING_WEBHOOK):
  payload = json.dumps(message_dict)
  try:
    urllib2.urlopen(webhook, payload)
  except urllib2.HTTPError:
    logging.warning('Error sending message to %s with payload:\n%s',
                    webhook, payload)
