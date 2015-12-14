# coding=utf-8

import commands

import unittest

import destiny
from data import items
from testing import mocks

class TestCommand(unittest.TestCase):
  def setUp(self):
    self.mock_url_opener = mocks.MockURLOpener()
    self.destiny_api = destiny.DestinyAPI(url_opener=self.mock_url_opener)
    self.command_runner = commands.CommandRunner(self.destiny_api)

  def test_weapon_search(self):
    path = "/Explorer/Items/"
    params = {
      'count': 1,
      'direction': 'Descending',
      'name': 'Gjallarhorn',
      'definitions': 'true',
      'order': 'MinimumRequiredLevel',
      'categories': items.WEAPON,
    }
    url = self.destiny_api.build_url(path, params)
    json = open('testdata/Explorer/Items/gjallarhorn.json', 'r').read()
    self.mock_url_opener.add_response(url, json)
    response = self.command_runner.weapon_search('Gjallarhorn')
    expected_attachment = {
      'color': '#ceae33',
      'text': 'Exotic Rocket Launcher',
      'title': 'Gjallarhorn',
      'title_link': 'http://db.destinytracker.com/items/1274330687/',
      'thumb_url': ('http://www.bungie.net/common/destiny_content/icons/'
                    'eb8377390504838c0190d8d56e70d28e.jpg'),
    }
    self.assertEqual('in_channel', response['response_type'])
    self.assertFalse(response.has_key('text'))
    self.assertEqual(1, len(response['attachments']))
    self.assertEqual(expected_attachment, response['attachments'][0])

  def test_armor_search(self):
    path = "/Explorer/Items/"
    params = {
      'count': 1,
      'direction': 'Descending',
      'name': 'taiko',
      'definitions': 'true',
      'order': 'MinimumRequiredLevel',
      'categories': items.ARMOR,
    }
    url = self.destiny_api.build_url(path, params)
    json = open('testdata/Explorer/Items/taiko.json', 'r').read()
    self.mock_url_opener.add_response(url, json)
    response = self.command_runner.armor_search('taiko')
    expected_attachment = {
      'color': '#ceae33',
      'text': 'Exotic Helmet',
      'title': 'The Taikonaut',
      'title_link': 'http://db.destinytracker.com/items/591060261/',
      'thumb_url': ('http://www.bungie.net/common/destiny_content/icons/'
                    'f28523f56de25b2f6c5c56acb9d4b9a5.jpg'),
    }
    self.assertEqual('in_channel', response['response_type'])
    self.assertFalse(response.has_key('text'))
    self.assertEqual(1, len(response['attachments']))
    self.assertEqual(expected_attachment, response['attachments'][0])

  def test_speak(self):
    response = self.command_runner.speak(None)
    self.assertEqual('in_channel', response['response_type'])
    self.assertTrue(response['text'])

  def test_whisper(self):
    response = self.command_runner.whisper('speak')
    self.assertEqual('ephemeral', response['response_type'])
    self.assertTrue(response['text'])

  def test_online_players(self):
    pass

  def test_daily_with_exotic(self):
    path = "/Advisors/"
    params = {
      'definitions': 'true'
    }
    url = self.destiny_api.build_url(path, params)
    json = open('testdata/Advisors/lost_to_light.json', 'r').read()
    self.mock_url_opener.add_response(url, json)

    item_path = "/Manifest/InventoryItem/3227022822/"
    item_url = self.destiny_api.build_url(item_path)
    item_json = open(
        'testdata/Manifest/InventoryItem/black_spindle.json', 'r').read()
    self.mock_url_opener.add_response(item_url, item_json)

    response = self.command_runner.daily(None)
    self.assertEqual('Daily Heroic Story: Lost to Light\n'
                     'Exotic quest for:', response['text'])
    self.assertEqual(1, len(response.get('attachments')))
    attachment = response['attachments'][0]
    self.assertEqual('Black Spindle', attachment['title'])

  def test_xur_gone(self):
    path = "/Advisors/"
    params = {
      'definitions': 'true'
    }
    url = self.destiny_api.build_url(path, params)
    json = open('testdata/Advisors/no_xur.json', 'r').read()
    self.mock_url_opener.add_response(url, json)

    response = self.command_runner.xur(None)
    self.assertEqual('Xûr is gone, for now...', response['text'])

if __name__ == '__main__':
    unittest.main()
