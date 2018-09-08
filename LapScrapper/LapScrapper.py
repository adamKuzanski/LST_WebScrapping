#url = 'https://www.racetimeapp.com/riders/all_times_riders.php?idutente=2143&idcircuito=8025&_=1536160307478'
url = 'http://localhost:8000/site.html'
#postUrl = 'http://localhost:8000/lap'
postUrl = 'http://localhost:55201/api/lap'
dateSet = "2018-08-31 11:00:00.0000"


import time
import Functions


lapCounter = 0 
lapsNumberArchive = -1
allLaps = []
recentLapEndTime = ""

scrappedLaps = Functions.ScrapPage(url)
nbOfLaps = len(scrappedLaps)
if nbOfLaps != 0:
    for lap in reversed(scrappedLaps):
         lapCounter += 1
         if lapCounter != len(scrappedLaps): #to avoid last index which is in different format
               allLaps.append(Functions.GetOneLap(lap, lapCounter, False, dateSet, recentLapEndTime))
               recentLapEndTime = allLaps[lapCounter - 1].End

#post returned objects
for lapObject in allLaps:
     Functions.PostLap(lapObject, postUrl)
     

#look for new laps, infinite loop
while True:
     print("Searching...")
     scrappedLaps = Functions.ScrapPage(url)
     newLapsNumber = len(scrappedLaps)

     if newLapsNumber > lapCounter:
          print("Lap found")
          lapsNumberArchive = lapCounter
          lapObject = Functions.GetOneLap(scrappedLaps[1],lapCounter, True)
          lapCounter += 1
          Functions.PostLap(lapObject, postUrl)
     else:
          print("Not found")
     time.sleep(2)
