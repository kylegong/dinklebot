import random

ALL_PHRASES = [
  "That wizard came from the moon!",
  "Well, at least it's chained up.",
  "WE'VE WOKEN THE HIVE!",
  "Think they'd mind if we take their Pikes?",
  "This could be going better...",
  "Can't we just stay here... with the murderous robots?",
]

def get_random_phrase():
  return random.choice(ALL_PHRASES)
