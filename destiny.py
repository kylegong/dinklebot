import json
import logging
import urllib
import urllib2

import secrets

API_ROOT = "https://www.bungie.net/Platform/Destiny"

def search_item(query):
  encoded_query = urllib.quote_plus(query)
  url = API_ROOT + "/Explorer/Items/?name=%s" % encoded_query
  data = make_api_request(url)
  try:
    first_result = data['itemHashes'][0]
    return fetch_item(first_result)
  except IndexError:
    return

def fetch_item(item_id):
  url = API_ROOT + "/Manifest/InventoryItem/%s/" % item_id
  data = make_api_request(url)
  item_data = data['inventoryItem']
  item_name = item_data['itemName']
  item_type = item_data['itemTypeName']
  tier = item_data['tierTypeName']
  destiny_tracker_url = "http://db.destinytracker.com/items/%s/" % item_id
  return (item_name, tier, item_type, destiny_tracker_url)

def make_api_request(url):
  request = urllib2.Request(url)
  request.add_header('X-API-Key', secrets.BUNGIE_API_KEY)
  try:
    response = urllib2.urlopen(request).read()
    return json.loads(response)['Response']['data']
  except urllib2.URLError as e:
    logging.warning('Error fetching %s:\n%s', url, e.read())
