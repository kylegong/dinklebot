import json
import logging
import os
import urllib
import urllib2

from data import items
import secrets

CONTENT_ROOT = "http://www.bungie.net"
API_ROOT = "https://www.bungie.net/Platform/Destiny"
DEFAULT_MAX_RESULTS = 1

class URLOpener(object):
  def open(self, request):
    try:
      return urllib2.urlopen(request).read()
    except urllib2.URLError as e:
      logging.warning('Error fetching %s:', request.get_full_url())
      logging.warning(e.read())

class DestinyAPI(object):
  def __init__(self, api_root=API_ROOT, url_opener=None):
    self.api_root = api_root
    if url_opener is None:
      url_opener = URLOpener()
    self.url_opener = url_opener

  ### Internal ###
  def make_api_request(self, path, params=None):
    request = self.build_api_request(path, params)
    http_response = self.url_opener.open(request)
    response = json.loads(http_response)
    if response['ErrorCode'] != 1:
      logging.warning('Error fetching %s: %s: %s', request.get_full_url(),
                      response['ErrorStatus'], response['Message'])
      return
    return response['Response']

  def build_url(self, path, params=None):
    url = self.api_root + path
    if params:
      url += '?%s' % urllib.urlencode(params)
    return url

  def build_api_request(self, path, params, api_key=secrets.BUNGIE_API_KEY):
    request = urllib2.Request(self.build_url(path, params))
    request.add_header('X-API-Key', api_key)
    return request

  def build_content_url(self, path, content_root=CONTENT_ROOT):
    return content_root + path

  def save_api_data(self, path, params):
    request = self.build_api_request(path, params)
    http_response = self.url_opener.open(request)
    TESTDATA = os.path.join(os.path.dirname(__file__), 'testdata')
    filepath = self.build_url(path, params, TESTDATA)
    if filepath.endswith('/'):
      filepath += 'index.html'
    parent = os.path.dirname(filepath)
    if not os.path.exists(parent):
      os.makedirs(parent)
    f = open(filepath, 'w')
    f.write(http_response)

  ### Public ###
  def search_item(self, query, category='', max_results=DEFAULT_MAX_RESULTS):
    params = {
      'name': query,
      'count': max_results,
      'categories': str(category),
      'definitions': 'true',
      # Sort by MinimumRequiredLevel Descending to prioritize newer versions
      'order': 'MinimumRequiredLevel',
      'direction': 'Descending',
    }
    path = "/Explorer/Items/"
    response = self.make_api_request(path, params)
    data = response['data']
    definitions = response['definitions']
    results = []
    item_ids = [str(item_id) for item_id in data['itemHashes']]
    items = definitions['items']
    for item_id in item_ids[:max_results]:
      results.append(items[item_id])
    return results

  def fetch_item(self, item_id):
    path = "/Manifest/InventoryItem/%s/" % item_id
    data = self.make_api_request(path)['data']
    return data['inventoryItem']

  def get_item_color(self, item_data):
    tier = item_data.get('tierTypeName')
    if tier == 'Exotic':
      return items.EXOTIC_COLOR
    elif tier == 'Legendary':
      return items.LEGENDARY_COLOR
    elif tier == 'Rare':
      return items.RARE_COLOR
    elif tier == 'Uncommon':
      return items.UNCOMMON_COLOR
    else:
      return items.COMMON_COLOR

  def get_destiny_tracker_url(self, item_data):
    item_id = item_data['itemHash']
    return "http://db.destinytracker.com/items/%s/" % item_id

  def get_account_summary(self, player_id):
    path = "/2/Account/%s/Summary/" % player_id
    response = self.make_api_request(path)
    return response['data']

  def get_last_played_character(self, account_summary):
    characters = [c['characterBase'] for c in account_summary['characters']]
    last_played_character = None
    for character in characters:
      if (last_played_character is None or
          last_played_character['dateLastPlayed'] < character['dateLastPlayed']):
        last_played_character = character
    return last_played_character

  def get_activity(self, activity_hash):
    path = "/Manifest/Activity/%s/" % activity_hash
    return self.make_api_request(path)

  def get_activity_name(self, activity_hash):
    if activity_hash == 0:
      return 'In orbit'
    response = self.get_activity(activity_hash)
    try:
      return response['data']['activity']['activityName']
    except (KeyError, TypeError):
      return 'Unknown [%s]' % activity_hash

  def get_advisors(self, definitions=True):
    params = {
      'definitions': 'true' if definitions else 'false'
    }
    path = "/Advisors/"
    return self.make_api_request(path, params)

  def get_daily_story(self):
    advisors = self.get_advisors()
    daily_hash = str(advisors['data']['dailyChapterHashes'][0])
    return advisors['definitions']['activities'][daily_hash]

  def related_exotic(self, daily):
    daily_hash = int(daily['activityHash'])
    if daily_hash == 2286628407: # Paradox
      return 'No Time To Explain: http://planetdestiny.com/no-time-to-explain/'
    elif daily_hash == 2604992012: # Lost to Light
      return 'Black Spindle: http://planetdestiny.com/black-spindle/'

  def get_item_attachment(self, item_data):
    attachment = {
      'title': item_data['itemName'],
      'title_link': self.get_destiny_tracker_url(item_data),
      'text':  '%s %s' % (item_data['tierTypeName'],
                          item_data['itemTypeName']),
      'thumb_url': self.build_content_url(item_data['icon']),
    }
    color = self.get_item_color(item_data)
    if color:
      attachment['color'] = color
    return attachment

  def get_xur_inventory(self):
    advisors = self.get_advisors()
    events = advisors['data']['events']['events']
    inventory = None
    for event in events:
      if event['eventIdentifier'] == "SPECIAL_EVENT_BLACK_MARKET":
        inventory = event['vendor']
    if inventory is None:
      return []
    item_categories = inventory['saleItemCategories']
    exotics = []
    for category in item_categories:
      if category['categoryTitle'] == 'Exotic Gear':
        exotics = category['saleItems']
    attachments = []
    for saleItem in exotics:
      item = saleItem['item']
      item_hash = item['itemHash']
      item_data = advisors['definitions']['items'][str(item_hash)]
      cost = saleItem['costs'][0]['value']
      item_attachment = self.get_item_attachment(item_data)
      item_attachment['text'] += '\n%d SC' % cost
      attachments.append(item_attachment)
    return attachments
