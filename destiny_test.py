import destiny

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import SocketServer
import threading
import unittest
import urlparse

from data import items

class TestJSONServerHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    filepath = self.path.lstrip('/')
    if filepath.endswith('/'):
      filepath += 'index.html'
    with open(filepath, 'r') as f:
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      self.wfile.write(f.read())

  def log_request(self, code=None, size=None):
    return

class TestDestiny(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.hostname = 'localhost'
    cls.port = 18290
    cls.server = HTTPServer((cls.hostname, cls.port), TestJSONServerHandler)
    threading.Thread(target=cls.server.serve_forever).start()

  @classmethod
  def tearDownClass(cls):
    cls.server.shutdown()

  def setUp(self):
    api_root = 'http://%s:%s/testdata' % (self.__class__.hostname,
                                          self.__class__.port)
    self.destiny = destiny.DestinyAPI(api_root=api_root)

  def test_make_api_request(self):
    uri = "/Manifest/InventoryItem/1274330687/"
    response = self.destiny.make_api_request(uri)
    item_data = response['data']['inventoryItem']
    self.assertEqual(1274330687, item_data['itemHash'])
    self.assertEqual('Gjallarhorn', item_data['itemName'])

  def test_fetch_item(self):
    # Both string and int item ids should work.
    item_ids = ["1274330687", 1274330687]
    for item_id in item_ids:
      item_data = self.destiny.fetch_item(item_id)
      self.assertEqual(1274330687, item_data['itemHash'])
      self.assertEqual('Gjallarhorn', item_data['itemName'])

  def test_search_item(self):
    items = self.destiny.search_item('gjallarhorn')
    self.assertEqual(1, len(items))
    item_data = items[0]
    self.assertEqual(1274330687, item_data['itemHash'])
    self.assertEqual('Gjallarhorn', item_data['itemName'])

  def test_search_item_with_max_results(self):
    items = self.destiny.search_item('suros', max_results=2)
    self.assertEqual(2, len(items))

  def test_search_item_with_category(self):
    weapons = self.destiny.search_item('suros', category=items.WEAPON,
                                  max_results=5)
    self.assertLess(2, len(weapons))
    shaders = self.destiny.search_item('suros', category=items.SHADERS,
                                  max_results=5)
    self.assertEqual(1, len(shaders))
    item_data = shaders[0]
    self.assertEqual(2561402282, item_data['itemHash'])
    self.assertEqual('SUROS Minimalist', item_data['itemName'])

  def test_get_item_attachment(self):
    item_data = self.destiny.fetch_item(1274330687)
    expected = {
      'color': '#ceae33',
      'text': 'Exotic Rocket Launcher',
      'title': 'Gjallarhorn',
      'title_link': 'http://db.destinytracker.com/items/1274330687/',
      'thumb_url': ('http://www.bungie.net/common/destiny_content/icons/'
                    'eb8377390504838c0190d8d56e70d28e.jpg'),
    }
    self.assertEqual(expected, self.destiny.get_item_attachment(item_data))

if __name__ == '__main__':
    unittest.main()
