class MockURLOpener(object):
  def __init__(self):
    self.responses = {}

  def add_response(self, url, response):
    self.responses[url] = response

  def open(self, request):
    url = request.get_full_url()
    try:
      return self.responses[url]
    except KeyError:
      error_msg = 'Unexpected URL\nRequested:\n%s\nExpected:\n' % url
      for expected_url in self.responses.keys():
        error_msg += '%s\n' % expected_url
      raise Exception(error_msg)
