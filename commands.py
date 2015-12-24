# coding=utf-8

import collections
import datetime
import json
import logging
import threading
import urlparse

from data import items
from data import players
from data import phrases
import destiny
import slack

COMMAND_LIST = []
COMMAND_MAP = {}

def command(name, extra=None, help_text=None, alt_names=None):
  """Decorates a function, adding it to dinklebot's list of commands.
  The function should have one mandatory parameter and return a slack response.

  Args:
    extra: (Optional) If extra text will be used, a short description.
    help_text: (Required) A short description of what the command does.
    alt_names: (Optional) Alternate names that will also trigger the command.
  """
  if not help_text:
    raise Exception('Commands must include help_text')
  if alt_names is None:
    alt_names = []
  def decorator(function):
    def wrapper(self, extra, *args, **kwargs):
      return function(self, extra, *args, **kwargs)
    wrapper.name = name
    wrapper.extra = extra
    wrapper.help_text = help_text
    wrapper.alt_names = alt_names
    COMMAND_LIST.append(wrapper)
    COMMAND_MAP[name] = wrapper
    for alt_name in alt_names:
      COMMAND_MAP[alt_name] = wrapper
    return wrapper
  return decorator

class CommandRunner(object):
  def __init__(self, request=None, destiny_api=None):
    self.request = request
    if destiny_api is None:
      destiny_api = destiny.DestinyAPI()
    self.destiny_api = destiny_api

  def run(self, full_command_text):
    """Returns a tuple of the command indicated and the extra text."""
    if not full_command_text:
      return CommandRunner.speak(self, None)
    command_name, _, extra = full_command_text.partition(' ')
    command = COMMAND_MAP.get(command_name)
    if command is None:
      command = CommandRunner.speak
    return command(self, extra)


  ### Commands ###
  @command('item', extra='query',
           help_text='Search for any item matching the query.',
           alt_names=['i'])
  def item_search(self, extra, category=None):
    query = extra
    results = []
    if category:
      results = self.destiny_api.search_item(query, category)
    else:
      results = self.destiny_api.search_item(query)
    if len(results) < 1:
      return slack.response('No results found for "%s"' % query)
    item_data = results[0]
    attachment = self.destiny_api.get_item_attachment(item_data)
    return slack.response(None, {
      'attachments': [attachment]
    })

  @command('weapon', extra='query',
           help_text='Search for a weapon matching the query.',
           alt_names=['w'])
  def weapon_search(self, extra):
    return self.item_search(extra, category=items.WEAPON)

  @command('armor', extra='query',
           help_text='Search for an armor piece matching the query.',
           alt_names=['a'])
  def armor_search(self, extra):
    return self.item_search(extra, category=items.ARMOR)

  @command('online', help_text='Show a list of who\'s online.',
           alt_names=['who'])
  def online_players(self, extra):
    last_played_chars = []
    threads = []
    def get_last_played(name, player_id):
      account_summary = self.destiny_api.get_account_summary(player_id)
      last_played_chars.append(
          (name, self.destiny_api.get_last_played_character(account_summary)))
    for name, player_id in players.PLAYER_IDS.items():
      t = threading.Thread(target=get_last_played, args=(name, player_id))
      t.start()
      threads.append(t)
    for thread in threads:
      thread.join()
    online_chars = []
    for name, last_played_char in last_played_chars:
      last_played_date = datetime.datetime.strptime(
          last_played_char['dateLastPlayed'], "%Y-%m-%dT%H:%M:%SZ")
      now = datetime.datetime.utcnow()
      if now - last_played_date < datetime.timedelta(minutes=15):
        online_chars.append((name, last_played_char))
    # Sort by name
    online_chars.sort(key=lambda x: x[0])
    online_count = len(online_chars)
    if online_count == 0:
      return slack.response('No players online.')
    message = 'Players online:\n'
    for name, character in online_chars:
      activity = self.destiny_api.get_activity_name(character['currentActivityHash'])
      message += '%s - %s\n' % (name, activity)
    return slack.response(message)

  @command('daily', help_text='Show the daily story mission.')
  def daily(self, extra):
    daily = self.destiny_api.get_daily_story()
    name = daily['activityName']
    message = 'Daily Heroic Story: %s' % name
    exotic = self.destiny_api.related_exotic(daily)
    if exotic:
      message += '\nExotic quest for:'
      attachments = [self.destiny_api.get_item_attachment(exotic)]
      return slack.response(message, {'attachments': attachments})
    return slack.response(message)

  @command('xur', help_text='Show  this week.')
  def xur(self, extra):
    attachments = self.destiny_api.get_xur_inventory()
    if not attachments:
      return slack.response('Xûr is gone, for now...')
    return slack.response('Xûr\'s Inventory', {
      'attachments': attachments
    })

  @command('spoiler', extra='message', help_text='Show a link to the message.')
  def spoiler(self, extra):
    import models
    message = extra
    username = slack.get_request_username(self.request)
    channel = slack.get_request_channel(self.request)
    spoiler_uri = models.Spoiler.save(username=username, channel=channel,
                                      message=message)
    domain = self.request.host_url
    url = urlparse.urljoin(domain, spoiler_uri)
    logging.info(domain, spoiler_uri, url)
    return slack.response('Spoiler from @%s:' % username, {'attachments': [{
      'title': 'Show spoiler...',
      'title_link': url,
    }]})

  @command('speak', help_text='Randomly say a classic dinklebot line.')
  def speak(self, extra):
    message = phrases.get_random_phrase()
    return slack.response(message)

  @command('whisper', help_text='Makes the response private to you.',
           alt_names=['me'])
  def whisper(self, extra):
    original_response = self.run(extra)
    return slack.ephemeral(original_response)

  @command('render', extra='json',
           help_text='Renders a json message privately for testing.')
  def render(self, extra):
    try:
      response = json.loads(extra)
      return slack.ephemeral(response)
    except ValueError:
      logging.warning('Invalid message:\n%s', extra)
      return slack.ephemeral(slack.response('Invalid message.'))

  @command('help', help_text='Show a list of available commands.',
           alt_names=['?'])
  def show_help(self, extra):
    help_messages = []
    for command in COMMAND_LIST:
      help_message = '*' + command.name + ''
      if command.extra:
        help_message += ' [' + command.extra + ']'
      help_message += '*: ' + command.help_text
      if command.alt_names:
        help_message += ' [' + ', '.join(command.alt_names) + ']'
      help_messages.append(help_message)
    return slack.response('\n'.join(help_messages), {
      'response_type': 'ephemeral'
    })
