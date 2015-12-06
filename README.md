# dinklebot


## Getting started with development

- Set up a github account
- Make a directory that you want to use on your computer:

```mkdir -p ~/Documents/projects/dinklebot
cd ~/Documents/projects/dinklebot
```

- Clone this repository to your computer:

    git clone git@github.com:YOUR_GITHUB_USERNAME/dinklebot.git

- Get a Bungie API key here: https://www.bungie.net/en/User/API
- Store it as BUNGIE_API_KEY in secrets.py:

    echo "BUNGIE_API_KEY = YOUR_BUNGIE_API_KEY" > secrets.py


## Running from the commandline
- You can run any command locally as follows:

    python commands_test.py hi
    python commands_test.py item gj

