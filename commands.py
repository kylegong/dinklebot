from data import phrases
import destiny

def run(full_command_text):
  if not full_command_text:
    return default('')
  command, _, params = full_command_text.partition(' ')
  function = COMMANDS.get(command)
  if function:
    return function(params)
  else:
    return default(params)

def default(params):
  return speak(params)

def speak(params):
  message = phrases.get_random_phrase()
  return message

def item_search(params):
  query = params
  result = destiny.search_item(query)
  if result:
    return '%s\n%s %s\n%s' % result
  else:
    return 'No results found for "%s"' % query

COMMANDS = {
  'speak': speak,
  'item': item_search,
}
