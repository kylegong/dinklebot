import flask

from data import phrases
import slack

app = flask.Flask(__name__)

@app.route('/hello/', methods=['GET', 'POST'])
def hello():
  message = phrases.get_random_phrase()
  return flask.jsonify(slack.response(message))

if __name__ == '__main__':
  app.run(debug=True)
