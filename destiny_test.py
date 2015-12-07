import destiny
import unittest

class TestDestiny(unittest.TestCase):

  def test_make_api_request(self):
    url = "https://www.bungie.net/Platform/Destiny/Manifest/InventoryItem/1274330687/"
    response = destiny.make_api_request(url)
    item_data = response['data']['inventoryItem']
    self.assertEqual(1274330687, item_data['itemHash'])
    self.assertEqual('Gjallarhorn', item_data['itemName'])

  def test_fetch_item(self):
    # Both string and int item ids should work.
    item_ids = ["1274330687", 1274330687]
    for item_id in item_ids:
      item_data = destiny.fetch_item(item_id)
      self.assertEqual(1274330687, item_data['itemHash'])
      self.assertEqual('Gjallarhorn', item_data['itemName'])

  def test_search_item(self):
    items = destiny.search_item('gjallarhorn')
    self.assertEqual(1, len(items))
    item_data = items[0]
    self.assertEqual(1274330687, item_data['itemHash'])
    self.assertEqual('Gjallarhorn', item_data['itemName'])

  def test_search_item_with_max_results(self):
    items = destiny.search_item('suros', max_results=2)
    self.assertEqual(2, len(items))

  def test_search_item_with_category(self):
    weapons = destiny.search_item('suros', category=destiny.WEAPON,
                                  max_results=5)
    self.assertLess(2, len(weapons))
    shaders = destiny.search_item('suros', category=destiny.SHADERS,
                                  max_results=5)
    self.assertEqual(1, len(shaders))
    item_data = shaders[0]
    self.assertEqual(2561402282, item_data['itemHash'])
    self.assertEqual('SUROS Minimalist', item_data['itemName'])

  def test_format_item_data(self):
    item_data = {
      'itemHash': 1274330687,
      'itemName': 'Gjallarhorn',
      'itemTypeName': 'Rocket Launcher',
      'tierTypeName': 'Exotic',
    }
    expected_text = """Gjallarhorn
Exotic Rocket Launcher
http://db.destinytracker.com/items/1274330687/"""
    self.assertEqual(expected_text, destiny.format_item_data(item_data))

if __name__ == '__main__':
    unittest.main()
