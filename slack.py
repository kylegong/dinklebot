def response(message, is_private=False):
  response = {"text": message}
  if is_private:
    response["response_type"] = "ephemeral"
  else:
    response["response_type"] = "in_channel"
  return response

def get_text(request):
  return request.params.get('text')
