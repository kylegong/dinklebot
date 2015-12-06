from flask import request

def response(message, private=False):
  response = {"text": message}
  if private:
    response["response_type"] = "ephemeral"
  else:
    response["response_type"] = "in_channel"
  return response

def get_post_data(key):
  for line in request.data.splitlines():
    try:
      line_key, line_value = line.split('=')
      if line_key == key:
        return line_value
    except ValueError:
      continue

def get_text():
  return get_post_data('text')
