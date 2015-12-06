import flask
from flask import request

import commands
import slack

app = flask.Flask(__name__)

@app.route('/v1/', methods=['GET', 'POST'])
def command():
  full_command_text = slack.get_text()
  return flask.jsonify(slack.response(commands.run(full_command_text)))

if __name__ == '__main__':
  app.run(debug=True)
