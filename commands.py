from data import phrases

def run(full_command_text):
  if not full_command_text:
    return default('')
  command, _, data = full_command_text.partition(' ')
  function = COMMANDS.get(command)
  if function:
    return function(data)
  else:
    return default(data)

def default(data):
  return speak(data)

def speak(data):
  message = phrases.get_random_phrase()
  return message

COMMANDS = {
  'speak': speak,
}
