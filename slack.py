def response(message, private=False):
  response = {"text": message}
  if private:
    response["response_type"] = "ephemeral"
  else:
    response["response_type"] = "in_channel"
  return response

def get_text(request):
  return request.params.get('text')
