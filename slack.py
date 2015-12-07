def response(text, extra_args=None):
  response = {'text': text}
  if extra_args:
    response.update(extra_args)
  return response

def get_request_text(request):
  return request.params.get('text')
