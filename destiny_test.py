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
    destiny.search_item('gjallarhorn')

if __name__ == '__main__':
    unittest.main()
