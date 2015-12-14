import destiny

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import SocketServer
import threading
import unittest
import urlparse

from data import items
from testing import mocks

class TestDestiny(unittest.TestCase):
  def setUp(self):
    self.mock_url_opener = mocks.MockURLOpener()
    self.destiny_api = destiny.DestinyAPI(url_opener=self.mock_url_opener)

  def test_make_api_request(self):
    path = "/Manifest/InventoryItem/1274330687/"
    url = self.destiny_api.build_url(path)
    response = open('testdata/Manifest/InventoryItem/1274330687.json').read()
    self.mock_url_opener.add_response(url, response)

    api_response = self.destiny_api.make_api_request(path)
    item_data = api_response['data']['inventoryItem']
    self.assertEqual(1274330687, item_data['itemHash'])
    self.assertEqual('Gjallarhorn', item_data['itemName'])

  def test_fetch_item(self):
    path = "/Manifest/InventoryItem/1274330687/"
    url = self.destiny_api.build_url(path)
    response = open('testdata/Manifest/InventoryItem/1274330687.json').read()
    self.mock_url_opener.add_response(url, response)

    # Both string and int item ids should work.
    item_ids = ["1274330687", 1274330687]
    for item_id in item_ids:
      item_data = self.destiny_api.fetch_item(item_id)
      self.assertEqual(1274330687, item_data['itemHash'])
      self.assertEqual('Gjallarhorn', item_data['itemName'])

  def test_search_item(self):
    path = "/Explorer/Items/"
    params = {
      'count': 1,
      'direction': 'Descending',
      'name': 'gjallarhorn',
      'definitions': 'true',
      'order': 'MinimumRequiredLevel',
      'categories': '',
    }
    url = self.destiny_api.build_url(path, params)
    response = open('testdata/Explorer/Items/gjallarhorn.json', 'r').read()
    self.mock_url_opener.add_response(url, response)

    results = self.destiny_api.search_item('gjallarhorn')
    self.assertEqual(1, len(results))
    item_data = results[0]
    self.assertEqual(1274330687, item_data['itemHash'])
    self.assertEqual('Gjallarhorn', item_data['itemName'])

  def test_search_item_with_max_results(self):
    path = "/Explorer/Items/"
    params = {
      'count': 2,
      'direction': 'Descending',
      'name': 'suros',
      'definitions': 'true',
      'order': 'MinimumRequiredLevel',
      'categories': '',
    }
    url = self.destiny_api.build_url(path, params)
    response = open(
        'testdata/Explorer/Items/suros_max_results.json', 'r').read()
    self.mock_url_opener.add_response(url, response)

    self.destiny_api = destiny.DestinyAPI(url_opener=self.mock_url_opener)
    items = self.destiny_api.search_item('suros', max_results=2)
    self.assertEqual(2, len(items))

  def test_search_item_with_category(self):
    path = "/Explorer/Items/"
    weapons_params = {
      'count': 5,
      'direction': 'Descending',
      'name': 'suros',
      'definitions': 'true',
      'order': 'MinimumRequiredLevel',
      'categories': items.WEAPON,
    }
    weapons_url = self.destiny_api.build_url(path, weapons_params)
    weapons_response = open(
        'testdata/Explorer/Items/suros_weapons.json', 'r').read()
    self.mock_url_opener.add_response(weapons_url, weapons_response)
    shaders_params = {
      'count': 5,
      'direction': 'Descending',
      'name': 'suros',
      'definitions': 'true',
      'order': 'MinimumRequiredLevel',
      'categories': items.SHADERS,
    }
    shaders_url = self.destiny_api.build_url(path, shaders_params)
    shaders_response = open(
        'testdata/Explorer/Items/suros_shaders.json', 'r').read()
    self.mock_url_opener.add_response(shaders_url, shaders_response)

    weapons = self.destiny_api.search_item('suros', category=items.WEAPON,
                                           max_results=5)
    self.assertLess(2, len(weapons))
    shaders = self.destiny_api.search_item('suros', category=items.SHADERS,
                                           max_results=5)
    self.assertEqual(1, len(shaders))
    item_data = shaders[0]
    self.assertEqual(2561402282, item_data['itemHash'])
    self.assertEqual('SUROS Minimalist', item_data['itemName'])

  def test_get_item_attachment(self):
    path = "/Manifest/InventoryItem/1274330687/"
    url = self.destiny_api.build_url(path)
    response = open(
        'testdata/Manifest/InventoryItem/1274330687.json', 'r').read()
    self.mock_url_opener.add_response(url, response)
    item_data = self.destiny_api.fetch_item(1274330687)
    expected = {
      'color': '#ceae33',
      'text': 'Exotic Rocket Launcher',
      'title': 'Gjallarhorn',
      'title_link': 'http://db.destinytracker.com/items/1274330687/',
      'thumb_url': ('http://www.bungie.net/common/destiny_content/icons/'
                    'eb8377390504838c0190d8d56e70d28e.jpg'),
    }

    self.assertEqual(expected, self.destiny_api.get_item_attachment(item_data))

  def test_get_item_color(self):
    exotic = {'tierTypeName': 'Exotic'}
    self.assertEqual(items.EXOTIC_COLOR,
                     self.destiny_api.get_item_color(exotic))
    legendary = {'tierTypeName': 'Legendary'}
    self.assertEqual(items.LEGENDARY_COLOR,
                     self.destiny_api.get_item_color(legendary))
    rare = {'tierTypeName': 'Rare'}
    self.assertEqual(items.RARE_COLOR,
                     self.destiny_api.get_item_color(rare))
    uncommon = {'tierTypeName': 'Uncommon'}
    self.assertEqual(items.UNCOMMON_COLOR,
                     self.destiny_api.get_item_color(uncommon))
    common = {'tierTypeName': 'Common'}
    self.assertEqual(items.COMMON_COLOR,
                     self.destiny_api.get_item_color(common))

  def test_get_account_summary(self):
    path = "/2/Account/4611686018428863262/Summary/"
    url = self.destiny_api.build_url(path)
    response = open('testdata/account_summary.json', 'r').read()
    self.mock_url_opener.add_response(url, response)

    player_id = 4611686018428863262
    summary = self.destiny_api.get_account_summary(player_id)
    self.assertEqual('4611686018428863262', summary['membershipId'])
    self.assertEqual(3, len(summary['characters']))

  def test_get_last_played_character(self):
    path = "/2/Account/4611686018428863262/Summary/"
    url = self.destiny_api.build_url(path)
    response = open('testdata/account_summary.json', 'r').read()
    self.mock_url_opener.add_response(url, response)

    player_id = 4611686018428863262
    summary = self.destiny_api.get_account_summary(player_id)
    last_played = self.destiny_api.get_last_played_character(summary)
    self.assertEqual('2305843009217219989', last_played['characterId'])

  def test_get_activity(self):
    path = "/Manifest/Activity/3743955707/"
    url = self.destiny_api.build_url(path)
    response = open('testdata/Manifest/Activity/3743955707.json', 'r').read()
    self.mock_url_opener.add_response(url, response)

    activity = self.destiny_api.get_activity(3743955707)
    self.assertEqual(3743955707, activity['data']['activity']['activityHash'])
    self.assertEqual('Tower', activity['data']['activity']['activityName'])

  def test_get_activity_name(self):
    path = "/Manifest/Activity/3743955707/"
    url = self.destiny_api.build_url(path)
    response = open('testdata/Manifest/Activity/3743955707.json', 'r').read()
    self.mock_url_opener.add_response(url, response)

    activity_name = self.destiny_api.get_activity_name(3743955707)
    self.assertEqual('Tower', activity_name)

    activity_name = self.destiny_api.get_activity_name(0)
    self.assertEqual('In orbit', activity_name)

  def test_get_daily_story(self):
    path = "/Advisors/"
    params = {
      'definitions': 'true'
    }
    url = self.destiny_api.build_url(path, params)
    response = open('testdata/Advisors/lost_to_light.json', 'r').read()
    self.mock_url_opener.add_response(url, response)
    
    daily_story = self.destiny_api.get_daily_story()
    self.assertEqual(2604992012, daily_story['activityHash'])
    self.assertEqual('Lost to Light', daily_story['activityName'])

  def test_related_exotic(self):
    path = "/Advisors/"
    params = {
      'definitions': 'true'
    }
    url = self.destiny_api.build_url(path, params)
    response = open('testdata/Advisors/lost_to_light.json', 'r').read()
    self.mock_url_opener.add_response(url, response)
    
    daily_story = self.destiny_api.get_daily_story()
    self.assertEqual('Lost to Light', daily_story['activityName'])
    related_exotic = self.destiny_api.related_exotic(daily_story)
    self.assertTrue(related_exotic.startswith('Black Spindle'))

  def test_get_xur_inventory_no_xur(self):
    path = "/Advisors/"
    params = {
      'definitions': 'true'
    }
    url = self.destiny_api.build_url(path, params)
    response = open('testdata/Advisors/no_xur.json', 'r').read()
    self.mock_url_opener.add_response(url, response)

    xur_inventory = self.destiny_api.get_xur_inventory()
    self.assertEqual([], xur_inventory)

  def test_get_xur_inventory(self):
    # TODO: need example JSON inventory with Xur there
    pass

if __name__ == '__main__':
    unittest.main()
