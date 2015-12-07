import collections

from data import phrases
import destiny

COMMAND_LIST = []
COMMAND_MAP = {}

def command(name, extra=None, help_text=None, alt_names=None):
  """Decorates a function, adding it to dinklebot's list of commands.
  The function should have one mandatory parameter and return a string.

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
    def wrapper(extra, *args, **kwargs):
      return function(extra, *args, **kwargs)
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

def run(full_command_text):
  """Runs the command indicated by the text."""
  if not full_command_text:
    return default('')
  command, _, extra = full_command_text.partition(' ')
  function = COMMAND_MAP.get(command)
  if function:
    return function(extra)
  else:
    return default(extra)


### Commands ###
@command('item', extra='query',
         help_text='Search for any item matching the query.',
         alt_names=['i'])
def item_search(extra, category=None):
  query = extra
  results = []
  if category:
    results = destiny.search_item(query, category)
  else:
    results = destiny.search_item(query)
  if len(results) < 1:
    return 'No results found for "%s"' % query
  first_result = results[0]
  return destiny.format_item_data(first_result)

@command('weapon', extra='query',
         help_text='Search for a weapon matching the query.',
         alt_names=['w'])
def weapon_search(extra):
  return item_search(extra, category=destiny.WEAPON)

@command('armor', extra='query',
         help_text='Search for an armor piece matching the query.',
         alt_names=['a'])
def armor_search(extra):
  return item_search(extra, category=destiny.ARMOR)

@command('speak', help_text='Randomly say a classic dinklebot line.')
def speak(extra):
  message = phrases.get_random_phrase()
  return message

@command('help', help_text='Show a list of available commands.',
         alt_names=['?'])
def show_help(extra):
  help_messages = []
  for command in COMMAND_LIST:
    help_message = command.name
    if command.extra:
      help_message += ' [' + command.extra + ']'
    help_message += ': ' + command.help_text
    if command.alt_names:
      help_message += ' [' + ', '.join(command.alt_names) + ']'
    help_messages.append(help_message)
  return '\n'.join(help_messages)
