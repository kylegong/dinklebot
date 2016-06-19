#!/usr/bin/env python

import json
import url_opener

NBA_BLUE = "#3965A4"

def get_logo_url(team_code):
  """
  >>> get_team_logo_url("GSW")
  'http://z.cdn.turner.com/nba/nba/.element/img/4.0/global/logos/512x512/bg.white/png/GSW.png'
  """
  return ('http://z.cdn.turner.com/nba/nba/.element/img/4.0/'
          'global/logos/512x512/bg.white/png/%s.png' % team_code)

def get_stats(date):
  url = ('http://stats.nba.com/stats/scoreboard/?GameDate='
         '%(date)s&LeagueID=00&DayOffset=0' % {'date': date})
  opener = url_opener.create()
  response = opener.open(url)
  stats = json.load(response)
  return stats

def get_scores_for_team(stats, team_code):
  times = stats['resultSets'][0]['rowSet']
  games = stats['resultSets'][1]['rowSet']
  team_score = None
  game_id = None
  for game in games:
    if get_team_code(game) == team_code:
      game_id = get_game_id(game)
      team_score = game
      break
  if game_id is None:
    return None
  opp_score = None
  for game in games:
    if get_team_code(game) != team_code and get_game_id(game) == game_id:
      opp_score = game
      break
  period = None
  for time in times:
    if time[2] == game_id:
      period = time
  return (team_score, opp_score, period)

def get_team_code(score):
  return score[4]

def get_game_id(score):
  return score[2]

def get_points(score):
  return score[21]

def get_team_name(score):
  return score[5]

def get_period_time(period):
  return period[10].strip()

def get_period_name(period):
  return period[4]

def format_scores(scores):
  team_score, opp_score, period = scores
  team_pts = get_points(team_score)
  opp_pts = get_points(opp_score)
  if team_pts < opp_pts:
    logo = get_logo_url(get_team_code(opp_score))
  else:
    logo = get_logo_url(get_team_code(team_score))
  score = '%(team_name)s %(team_pts)s-%(opp_pts)s %(opp_name)s' % {
    'team_name': get_team_name(team_score),
    'opp_name': get_team_name(opp_score),
    'team_pts': team_pts,
    'opp_pts': opp_pts,
  }
  period_info = ' '.join((get_period_time(period), get_period_name(period)))
  return {
    "attachments": [
      {
        "title": score,
        "text": period_info,
        "thumb_url": logo,
        "color": NBA_BLUE,
        "fallback": " ".join((score, period_info)),
      }
    ]
  }