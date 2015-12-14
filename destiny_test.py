import destiny

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import SocketServer
import threading
import unittest
import urlparse

from data import items

class MockURLOpener(object):
  def __init__(self, api_root=destiny.API_ROOT):
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

class TestDestiny(unittest.TestCase):
  def test_make_api_request(self):
    mock_url_opener = MockURLOpener()
    destiny_api = destiny.DestinyAPI(url_opener=mock_url_opener)
    path = "/Manifest/InventoryItem/1274330687/"
    url = destiny_api.build_url(path)
    response = open('testdata/Manifest/InventoryItem/1274330687.json').read()
    mock_url_opener.add_response(url, response)

    api_response = destiny_api.make_api_request(path)
    item_data = api_response['data']['inventoryItem']
    self.assertEqual(1274330687, item_data['itemHash'])
    self.assertEqual('Gjallarhorn', item_data['itemName'])

  def test_fetch_item(self):
    mock_url_opener = MockURLOpener()
    destiny_api = destiny.DestinyAPI(url_opener=mock_url_opener)
    path = "/Manifest/InventoryItem/1274330687/"
    url = destiny_api.build_url(path)
    response = open('testdata/Manifest/InventoryItem/1274330687.json').read()
    mock_url_opener.add_response(url, response)

    # Both string and int item ids should work.
    item_ids = ["1274330687", 1274330687]
    for item_id in item_ids:
      item_data = destiny_api.fetch_item(item_id)
      self.assertEqual(1274330687, item_data['itemHash'])
      self.assertEqual('Gjallarhorn', item_data['itemName'])

  def test_search_item(self):
    mock_url_opener = MockURLOpener()
    destiny_api = destiny.DestinyAPI(url_opener=mock_url_opener)
    path = "/Explorer/Items/"
    params = {
      'count': 1,
      'direction': 'Descending',
      'name': 'gjallarhorn',
      'definitions': 'true',
      'order': 'MinimumRequiredLevel',
      'categories': '',
    }
    url = destiny_api.build_url(path, params)
    response = open('testdata/Explorer/Items/gjallarhorn.json', 'r').read()
    mock_url_opener.add_response(url, response)

    results = destiny_api.search_item('gjallarhorn')
    self.assertEqual(1, len(results))
    item_data = results[0]
    self.assertEqual(1274330687, item_data['itemHash'])
    self.assertEqual('Gjallarhorn', item_data['itemName'])

  def test_search_item_with_max_results(self):
    mock_url_opener = MockURLOpener()
    destiny_api = destiny.DestinyAPI(url_opener=mock_url_opener)
    path = "/Explorer/Items/"
    params = {
      'count': 2,
      'direction': 'Descending',
      'name': 'suros',
      'definitions': 'true',
      'order': 'MinimumRequiredLevel',
      'categories': '',
    }
    url = destiny_api.build_url(path, params)
    response = open(
        'testdata/Explorer/Items/suros_max_results.json', 'r').read()
    mock_url_opener.add_response(url, response)

    destiny_api = destiny.DestinyAPI(url_opener=mock_url_opener)
    items = destiny_api.search_item('suros', max_results=2)
    self.assertEqual(2, len(items))

  def test_search_item_with_category(self):
    mock_url_opener = MockURLOpener()
    destiny_api = destiny.DestinyAPI(url_opener=mock_url_opener)
    path = "/Explorer/Items/"
    weapons_params = {
      'count': 5,
      'direction': 'Descending',
      'name': 'suros',
      'definitions': 'true',
      'order': 'MinimumRequiredLevel',
      'categories': items.WEAPON,
    }
    weapons_url = destiny_api.build_url(path, weapons_params)
    weapons_response = open(
        'testdata/Explorer/Items/suros_weapons.json', 'r').read()
    mock_url_opener.add_response(weapons_url, weapons_response)
    shaders_params = {
      'count': 5,
      'direction': 'Descending',
      'name': 'suros',
      'definitions': 'true',
      'order': 'MinimumRequiredLevel',
      'categories': items.SHADERS,
    }
    shaders_url = destiny_api.build_url(path, shaders_params)
    shaders_response = open(
        'testdata/Explorer/Items/suros_shaders.json', 'r').read()
    mock_url_opener.add_response(shaders_url, shaders_response)

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
    mock_url_opener = MockURLOpener()
    destiny_api = destiny.DestinyAPI(url_opener=mock_url_opener)
    path = "/Manifest/InventoryItem/1274330687/"
    url = destiny_api.build_url(path)
    response = open('testdata/Manifest/InventoryItem/1274330687.json', 'r').read()
    mock_url_opener.add_response(url, response)
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
