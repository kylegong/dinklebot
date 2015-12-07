def response(text, extra_args=None):
  response = {'text': text}
  response.update(extra_args)
  return response

def get_request_text(request):
  return request.params.get('text')
