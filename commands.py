from data import phrases

def run(full_command_text):
  command, _, data = full_command_text.partition(' ')
  function = COMMANDS[command]
  if function:
    return function(data)
  else:
    return speak(data)

def speak(data):
  message = phrases.get_random_phrase()
  return message

COMMANDS = {
  'speak': speak,
}
