from requests import get, post
from bs4 import BeautifulSoup
from Lap import Lap
from bson import json_util
import json
import re
import datetime
from dateutil import parser

from urllib.parse import urlencode
from urllib.request import Request, urlopen


def ScrapPage(url):
     lapInfo = []
     response = get(url)
     html_soup = BeautifulSoup(response.text, 'html.parser')
     for table in html_soup.find_all(class_='tabellaGiri'):
          for tr in table.find_all('tr'):
               lapInfo.append([td for td in tr.stripped_strings])
     return lapInfo


def GetSeconds(lapTimeInMinutes):
     time = re.split(':', lapTimeInMinutes)
     time[1:2] = [x.strip() for x in time[1].split('.')]
     return float(float(time[0]) * 60 + float(time[1]) * 1 + float(time[2]) / 1000)


def GetTopSpeed(topSpeedString):
     topSpeed = re.findall(r'\d+', topSpeedString)
     return topSpeed[0]


def GetOneLap(oneLapInfo, lapNumber, isNewLap = False, dateSet = "", recentLapEndTime = ""):
     endTime = 0
     startTime = 0
     secondsForLap = GetSeconds(oneLapInfo[0])
     topSpeed = GetTopSpeed(oneLapInfo[3])
     if isNewLap:
          endTime = datetime.datetime.now()
          startTime = endTime - datetime.timedelta(seconds = secondsForLap)
          endTime = endTime.strftime('%d.%m.%Y %H:%M:%S')
          startTime = startTime.strftime('%d.%m.%Y %H:%M:%S')
          print("new")
     else:
          if(recentLapEndTime != ""):
               startTime = parser.parse(recentLapEndTime)
          else:
               startTime = parser.parse(dateSet)
          endTime = startTime + datetime.timedelta(seconds = secondsForLap)
          endTime = endTime.strftime('%d.%m.%Y %H:%M:%S')
          startTime = startTime.strftime('%d.%m.%Y %H:%M:%S')
          recentLapEndTime = endTime


     lap = Lap(lapNumber, startTime, endTime, secondsForLap, topSpeed)
     return lap


def PostLap(lap, postUrl):
     header = {'Content-type': 'application/json'}
     postData = json.loads( json.dumps(lap.__dict__) )
     print(postData)
     r = post(postUrl, json = postData, headers = header)
     print(r.status_code, r.reason)



