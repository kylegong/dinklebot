import json
import logging
import urllib
import urllib2

import secrets

API_ROOT = "https://www.bungie.net/Platform/Destiny"
DEFAULT_MAX_RESULTS = 1

def search_item(query, category='', max_results=DEFAULT_MAX_RESULTS):
  params = {
    'name': query,
    'count': max_results,
    'categories': str(category),
    'definitions': 'true',
    # Sort by MinimumRequiredLevel Descending to prioritize newer versions
    'order': 'MinimumRequiredLevel',
    'direction': 'Descending',
  }
  url = API_ROOT + "/Explorer/Items/?%s" % urllib.urlencode(params)
  response = make_api_request(url)
  data = response['data']
  definitions = response['definitions']
  results = []
  item_ids = [str(item_id) for item_id in data['itemHashes']]
  items = definitions['items']
  for item_id in item_ids[:max_results]:
    results.append(items[item_id])
  return results

def fetch_item(item_id):
  url = API_ROOT + "/Manifest/InventoryItem/%s/" % item_id
  data = make_api_request(url)['data']
  return data['inventoryItem']

def format_item_data(item_data):
  item_id = item_data['itemHash']
  item_name = item_data['itemName']
  item_type = item_data['itemTypeName']
  tier = item_data['tierTypeName']
  destiny_tracker_url = "http://db.destinytracker.com/items/%s/" % item_id
  message = '''%(item_name)s
%(tier)s %(item_type)s
%(destiny_tracker_url)s''' % {
    'item_name': item_name,
    'tier': tier,
    'item_type': item_type,
    'destiny_tracker_url': destiny_tracker_url,
  }
  return message

def make_api_request(url):
  request = urllib2.Request(url)
  request.add_header('X-API-Key', secrets.BUNGIE_API_KEY)
  try:
    response = json.loads(urllib2.urlopen(request).read())
    if response['ErrorCode'] != 1:
      logging.warning('Error fetching %s: %s: %s', url, response['ErrorStatus'],
                      response['Message'])
      return
    return response['Response']
  except urllib2.URLError as e:
    logging.warning('Error fetching %s:\n%s', url, e.read())

# Destiny Item Categories
WEAPON = 1
PRIMARY_WEAPON = 2
SPECIAL_WEAPON = 3
HEAVY_WEAPON = 4
AUTO_RIFLE = 5
HAND_CANNON = 6
PULSE_RIFLE = 7
SCOUT_RIFLE = 8
FUSION_RIFLE = 9
SNIPER_RIFLE = 10
SHOTGUN = 11
MACHINE_GUN = 12
ROCKET_LAUNCHER = 13
SIDEARM = 14
CURRENCIES = 18
EMBLEMS = 19
ARMOR = 20
WARLOCK = 21
TITAN = 22
HUNTER = 23
BOUNTIES = 26
CONSUMABLES = 35
GHOST = 39
MATERIALS = 40
SHADERS = 41
SHIPS = 42
SPARROWS = 43
HELMETS = 45
ARMS = 46
CHEST = 47
LEGS = 48
CLASS_ITEMS = 49
INVENTORY = 52
