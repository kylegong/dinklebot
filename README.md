# dinklebot

## Getting started with development
- Set up a github account
- Make a directory that you want to use on your computer:
```
    mkdir -p ~/Documents/projects/dinklebot
    cd ~/Documents/projects/dinklebot
```
- Clone this repository to your computer:
```
    git clone git@github.com:YOUR_GITHUB_USERNAME/dinklebot.git
```
- Get a Bungie API key here: https://www.bungie.net/en/User/API
- Store it as BUNGIE_API_KEY in `secrets.py`:
```
    echo "BUNGIE_API_KEY = YOUR_BUNGIE_API_KEY" > secrets.py
```

## Running from the commandline
- You can run any command locally as follows:
```
    python dinklebot.py hi
    python dinklebot.py item gj
```

## Adding a new command
- Add a function to the `### Commands ###` section of `commands.py`
    that returns a string (this will be Dinklebot's response message).
- Wrap it with an `@command` decorator, giving it a name,
    a description of what will be done with the extra text (if used),
    and a short help message describing what the command does.  For example:
```
    @command('echo', extra='message', help_text='Repeat the message.')
    def echo(extra):
      return extra
```
