#!/usr/bin/python

from twython import Twython
from datetime import datetime
import time
import locale

locale.setlocale(locale.LC_ALL,'')
now = time.strftime('%A %d %B %Y')
delta = datetime.now() - datetime(2011,11,4)

APP_KEY=""
APP_SECRET=""
OAUTH_TOKEN=""
OAUTH_TOKEN_SECRET=""

twitter = Twython(APP_KEY,APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)

twitter.update_status(status="Aujourd'hui, nous sommes le"+str(now)+". Il y a "+str(delta.days)+" jours, nous étions le 04/11/2011...)
