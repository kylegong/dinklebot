import commands

import unittest

class TestCommand(unittest.TestCase):
  def test_weapon_search(self):
    response = commands.weapon_search('Gjallarhorn')
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
    response = commands.armor_search('taiko')
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
    response = commands.speak(None)
    self.assertEqual('in_channel', response['response_type'])
    self.assertTrue(response['text'])

  def test_whisper(self):
    response = commands.whisper('speak')
    self.assertEqual('ephemeral', response['response_type'])
    self.assertTrue(response['text'])

if __name__ == '__main__':
    unittest.main()