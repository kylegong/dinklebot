# dinklebot

## Getting started with development
- Set up a github account
- Sign in, and then fork this repository to your account. The Fork button
    should be at the top right of this page.
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
    echo "BUNGIE_API_KEY = 'YOUR_BUNGIE_API_KEY'" > secrets.py
```

## Running from the commandline
- You can run any command locally as follows:
```
    python dinklebot.py hi
    python dinklebot.py item gj
```

## Adding a new command
- Add a function to the `### Commands ###` section of `commands.py`
    that returns a slack response (this will be Dinklebot's response message).
- Wrap it with an `@command` decorator, giving it a name,
    a description of what will be done with the extra text (if used),
    and a short help message describing what the command does.  For example:
```
    @command('echo', extra='message', help_text='Repeat the message.')
    def echo(extra):
      return slack.response(extra)
```

# Destiny API
## General notes
Game objects seem to identified through hashes, which is an integer value
representing the object.  More information about that hash can usually be
obtained by adding a definitions=true parameter, which will return a response
that includes data about the associated things, indexed by type and hash.

The following are useful links to known Endpoints and Globals:
http://bungienetplatform.wikia.com/wiki/Endpoints
http://bungienetplatform.wikia.com/wiki/Globals

## Postman
Postman is a pretty useful tool for testing REST APIs like the Destiny API.
You can get it here.
https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en

You will need to set your Bungie API Key as an 'X-API-Key' header in your
requests. You should then be able to make API requests through Postman and
see the raw JSON responses.

## /Explorer/Items
This allows item lookups based on partial name matches and other filters.
Known item categories are available in destiny.py

If definitions=true, it will include item_data. Otherwise, it's just the hashes.

e.g. http://www.bungie.net/Platform/Destiny/Explorer/Items/?name=suros&count=10&categories=2&definitions=true

## Manifest
This returns data about an individual item.
e.g. https://www.bungie.net/Platform/Destiny/Manifest/InventoryItem/1274330687/

## GetAccountSummary
You can get this from going to https://www.bungie.net/en/Profile and opening
the gear page for one of your characters. That link will be of the form:
https://www.bungie.net/en/Legend/Gear/{membershipType}/{destinyMembershipId}/{characterId}
e.g. https://www.bungie.net/en/Legend/Gear/2/4611686018428863262/2305843009249214248

You can then use this information to access GetAccountSummary:
http://www.bungie.net/Platform/Destiny/{membershipType}/Account/{destinyMembershipId}/Summary/
e.g. http://www.bungie.net/Platform/Destiny/2/Account/4611686018428863262/Summary/?definitions=false

PSN appears to be membershipType=2

### characterBase/dateLastPlayed
When someone is actively playing Destiny, dateLastPlayed will be updated for
the character they are logged in as.  dateLastPlayed does not seem to be
updated very frequently when the character is in orbit. In an activity it
seems to be updated about once a minute.

### characterBase/currentActivityHash
This seems to be set to 0 when the character is logged out or in orbit.
The activity hashes can be decoded with /Destiny/Manifest/Activity/[activityHash]/
