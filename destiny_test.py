import destiny

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import SocketServer
import threading
import unittest
import urlparse

from data import items

class MockURLOpener(object):
  def __init__(self, url_response_map):
    self.url_response_map = url_response_map

  def open(self, request):
    url = request.get_full_url()
    return self.url_response_map[url]

class TestDestiny(unittest.TestCase):
  def test_make_api_request(self):
    uri = "/Manifest/InventoryItem/1274330687/"
    response = open('testdata/Manifest/InventoryItem/1274330687.json').read()
    url = destiny.API_ROOT + uri
    mock_url_opener = MockURLOpener({
      url: response,
    })
    destiny_api = destiny.DestinyAPI(url_opener=mock_url_opener)
    response = destiny_api.make_api_request(uri)
    item_data = response['data']['inventoryItem']
    self.assertEqual(1274330687, item_data['itemHash'])
    self.assertEqual('Gjallarhorn', item_data['itemName'])

  def test_fetch_item(self):
    uri = "/Manifest/InventoryItem/1274330687/"
    response = open('testdata/Manifest/InventoryItem/1274330687.json', 'r').read()
    mock_url_opener = MockURLOpener({
      destiny.API_ROOT + uri: response,
    })
    destiny_api = destiny.DestinyAPI(url_opener=mock_url_opener)

    # Both string and int item ids should work.
    item_ids = ["1274330687", 1274330687]
    for item_id in item_ids:
      item_data = destiny_api.fetch_item(item_id)
      self.assertEqual(1274330687, item_data['itemHash'])
      self.assertEqual('Gjallarhorn', item_data['itemName'])

  def test_search_item(self):
    uri = "/Explorer/Items/?count=1&direction=Descending&name=gjallarhorn&definitions=true&order=MinimumRequiredLevel&categories="
    response = open('testdata/Explorer/Items/?count=1&direction=Descending&name=gjallarhorn&definitions=true&order=MinimumRequiredLevel&categories=', 'r').read()
    mock_url_opener = MockURLOpener({
      destiny.API_ROOT + uri: response,
    })
    destiny_api = destiny.DestinyAPI(url_opener=mock_url_opener)
    items = destiny_api.search_item('gjallarhorn')
    self.assertEqual(1, len(items))
    item_data = items[0]
    self.assertEqual(1274330687, item_data['itemHash'])
    self.assertEqual('Gjallarhorn', item_data['itemName'])

  def test_search_item_with_max_results(self):
    uri = "/Explorer/Items/?count=2&direction=Descending&name=suros&definitions=true&order=MinimumRequiredLevel&categories="
    response = open('testdata/Explorer/Items/?count=2&direction=Descending&name=suros&definitions=true&order=MinimumRequiredLevel&categories=', 'r').read()
    mock_url_opener = MockURLOpener({
      destiny.API_ROOT + uri: response,
    })

    destiny_api = destiny.DestinyAPI(url_opener=mock_url_opener)
    items = destiny_api.search_item('suros', max_results=2)
    self.assertEqual(2, len(items))

  def test_search_item_with_category(self):
    weapons_uri = '/Explorer/Items/?count=5&direction=Descending&name=suros&definitions=true&order=MinimumRequiredLevel&categories=1'
    weapons_response = open('testdata/Explorer/Items/?count=5&direction=Descending&name=suros&definitions=true&order=MinimumRequiredLevel&categories=1', 'r').read()
    shaders_uri = "/Explorer/Items/?count=5&direction=Descending&name=suros&definitions=true&order=MinimumRequiredLevel&categories=41"
    shaders_response = open('testdata/Explorer/Items/?count=5&direction=Descending&name=suros&definitions=true&order=MinimumRequiredLevel&categories=41', 'r').read()
    mock_url_opener = MockURLOpener({
      destiny.API_ROOT + weapons_uri: weapons_response,
      destiny.API_ROOT + shaders_uri: shaders_response,
    })
    destiny_api = destiny.DestinyAPI(url_opener=mock_url_opener)
    weapons = destiny_api.search_item('suros', category=items.WEAPON,
                                  max_results=5)
    self.assertLess(2, len(weapons))
    shaders = destiny_api.search_item('suros', category=items.SHADERS,
                                  max_results=5)
    self.assertEqual(1, len(shaders))
    item_data = shaders[0]
    self.assertEqual(2561402282, item_data['itemHash'])
    self.assertEqual('SUROS Minimalist', item_data['itemName'])

  def test_get_item_attachment(self):
    uri = "/Manifest/InventoryItem/1274330687/"
    response = open('testdata/Manifest/InventoryItem/1274330687.json', 'r').read()
    mock_url_opener = MockURLOpener({
      destiny.API_ROOT + uri: response,
    })
    destiny_api = destiny.DestinyAPI(url_opener=mock_url_opener)
    item_data = destiny_api.fetch_item(1274330687)
    expected = {
      'color': '#ceae33',
      'text': 'Exotic Rocket Launcher',
      'title': 'Gjallarhorn',
      'title_link': 'http://db.destinytracker.com/items/1274330687/',
      'thumb_url': ('http://www.bungie.net/common/destiny_content/icons/'
                    'eb8377390504838c0190d8d56e70d28e.jpg'),
    }
    self.assertEqual(expected, destiny_api.get_item_attachment(item_data))

if __name__ == '__main__':
    unittest.main()
