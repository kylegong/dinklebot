import json
import logging
import urllib
import urllib2

from data import activities
import secrets

CONTENT_ROOT = "http://www.bungie.net"
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
  message = '''%(item_name)s
%(tier)s %(item_type)s
%(destiny_tracker_url)s''' % {
    'item_name': item_name,
    'tier': tier,
    'item_type': item_type,
    'destiny_tracker_url': get_destiny_tracker_url(item_data),
  }
  return message

def get_item_color(item_data):
  tier = item_data['tierTypeName']
  if tier == 'Exotic':
    return EXOTIC_COLOR
  elif tier == 'Legendary':
    return LEGENDARY_COLOR
  elif tier == 'Rare':
    return RARE_COLOR
  elif tier == 'Uncommon':
    return UNCOMMON_COLOR

def get_destiny_tracker_url(item_data):
  item_id = item_data['itemHash']
  return "http://db.destinytracker.com/items/%s/" % item_id

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

def get_content_url(path):
  return CONTENT_ROOT + path

def get_account_summary(player_id):
  url = API_ROOT + "/2/Account/%s/Summary/" % player_id
  response = make_api_request(url)
  return response['data']

def get_last_played_character(account_summary):
  characters = [c['characterBase'] for c in account_summary['characters']]
  last_played_character = None
  for character in characters:
    if (last_played_character is None or
        last_played_character['dateLastPlayed'] < character['dateLastPlayed']):
      last_played_character = character
  return last_played_character

def get_activity_name(activity_hash):
  if activity_hash == 0:
    return 'In orbit'
  url = API_ROOT + "/Manifest/Activity/%s/" % activity_hash
  response = make_api_request(url)
  print response
  try:
    return response['data']['activity']['activityName']
  except (KeyError, TypeError):
    return 'Unknown [%s]' % activity_hash

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

# Destiny Tier Colors
UNCOMMON_COLOR = "#366f42"
RARE_COLOR = "#5076a3"
LEGENDARY_COLOR = "#522f65"
EXOTIC_COLOR = "#ceae33"
