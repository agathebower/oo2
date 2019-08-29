from flask import Flask, request, render_template
import time
import subprocess
import re
import io
import sentry_sdk
import requests
import threading
import sqlite3
from sentry_sdk import capture_message

app = Flask(__name__, template_folder='../templates')

@app.route('/', methods=['GET'])
def my_form():
#  sentry_sdk.init("https://4678861467f644b28d0b6b7ed2557bd7@sentry.io/1524102", debug=True)
  return render_template('my-form.html')
#  return login()


@app.route('/', methods=['POST'])
def handle_post():
  post_data = request.form['text']
  return login(post_data)


def get_credentials():
  conn = open_db()
  if not conn: print('no connection to db')
  with conn:
    cur = conn.cursor()
    cur.execute('SELECT name from pws;')
    name = cur.fetchall()
  return name[0][0]


def open_db():
  db_file = '/db/testdb'
  try:
    conn = sqlite3.connect(db_file)
    return conn
  except Exception as e:
    db_file = 'testdb'
    try:
      conn = sqlite3.connect(db_file)
      return conn
    except Exception as e2:
      print('error -- unable to access db')


def login(post_data):
  with requests.Session() as s:
    s.get('https://intranet.akra.de')
    s.get('https://intranet.akra.de/session/new')
    name = get_credentials()
    c = {'login':name, 'password':post_data, 'x':31, 'y':10}
    s.post('https://intranet.akra.de/session', data=c)
    r2 = s.get('https://intranet.akra.de/users/tied/time_sheet')
    if 'Arbeitszeiten heute:' in r2.text:
      return calc(r2.text)        
    else:
      return '<font size="18">NO DATA</font>'


def calc(f):
  res = ''
  #pattern_date = '.*(\d{2}\.\d{2}\.20\d{2}).*'
  #all_dates = re.findall(pattern_date, f)
  #for d in all_dates:
  #  res += '{0}</br>'.format(d)
  pattern = '.*heute: (\d{1,2})h (\d{1,2}).*'
  all_work_items = re.findall(pattern, f)
  if all_work_items:
    acc = 0
    i = 0
    for el in all_work_items:
      hours = el[0]
      minutes = el[1]
      if int(hours) == int(minutes) and int(minutes) == 0:
        continue
      #res += 'hours: {0} minutes: {1}</br>'.format(hours, minutes)
      #res += 'Found: {0}</br>'.format(el)
      overall_minutes = int(hours)*60+int(minutes)
      minutes_to_work = 7*60+42
      if overall_minutes > minutes_to_work:
        over_minutes = overall_minutes - minutes_to_work
        #res += 'over minutes for today: {0}</br>'.format(over_minutes)
        acc += over_minutes
      elif overall_minutes < minutes_to_work:
        under_minutes = minutes_to_work - overall_minutes
        #res += 'under minutes for today: {0}</br>'.format(under_minutes)
        acc -= under_minutes
      else:
        continue
      #res += 'current:  {0}</br></br>'.format(acc)
  else:
#    sentry_sdk.capture_message('NO DATA GIVEN')
    return '<font size="18">NO DATA</font>'

  if abs(acc) < 60:
    hours = 0
    minutes = acc
  else:
    hours = float(acc)/60
    minutes = hours % 1
    hours = hours - minutes
    minutes = minutes * 60
  res += '<font size="18">{0} hours {1} minutes</font>'.format(int(hours), int(minutes))
  return res
