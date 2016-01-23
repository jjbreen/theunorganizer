from xml.etree.ElementTree import ElementTree
import xml
import requests
import datetime 
import time 

from flask import Flask
from flask import render_template
from pymongo import MongoClient

app = Flask(__name__)

namespace = {'r25' : 'http://www.collegenet.com/r25'}

client = MongoClient("localhost", 27017)
dbspaces = client.db_spaces
dbidtimes = client.db_idtimes
dbroomtogps = client.db_roomgps

@app.route("/")
def hello():
    return render_template("landingpage.html")

@app.route("/location")
def getlocation():
    return parseWPILive()

@app.route('/public/<path:path>')
def send_js(path):
    return send_from_directory('public', path)

def parseWPILive():
	tpath = "https://25live.collegenet.com/25live/data/wpi/run/spaces.xml"

	r = requests.get(tpath)

	tree = xml.etree.ElementTree.fromstring(r.content)

	spaceList = tree.findall("r25:space", namespace)
	

	attrList = ["space_id", "space_name", "formal_name", "partition_name", "max_capacity"]
	queryDict = [{y : x.findall("r25:%s" % (y), namespace)[-1].text for y in attrList if len(x.findall("r25:%s" % (y), namespace)) > 0} for x in spaceList]

	"""
	#Do this later
	urlRInfo = "https://25live.collegenet.com/25live/data/wpi/run/space.xml?space_id=%s"
	for x in queryDict:
		r = requests.get(urlRInfo % (x["space_id"]))
		tree = xml.etree.ElementTree.fromstring(r.content)
		
		attrList = ["comments", "feature", "hour"]
	"""
		


	return queryDict


def queryTimes(space_id):
	tpath = "https://25live.collegenet.com/25live/data/wpi/run/rm_reservations.xml?space_id={0}&date_params=date_order%3A%20MDY%3B%24hour_inc%3A%201%3B%20minute_inc%3A%205%3B%20month_display%3A%20I%3B%20day_display%3A%20I%3B%20date_sep%3A%20S%3B%20time_display%3A%2012&scope=extended&browser=moz&include=closed+blackouts+pending+related&office_start=0000&office_end=2359&start_dt={1}&end_dt={2}&hr_format=12&office_hrs={3}"

	current_date = datetime.date.today()
	dt = "%04d%02d%02d" % (current_date.year, current_date.month, current_date.day)
	start_dt = "%s000000" % (dt)
	end_dt = "%s235959" % (dt)
	office_hrs = "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23"

	r = requests.get(tpath.format(space_id, start_dt, end_dt, office_hrs))
	
	tree = xml.etree.ElementTree.fromstring(r.content)

	reservations = tree.findall("r25:space_reservation", namespace)

	attrList = ["reservation_start_dt", "reservation_end_dt", "event/r25:event_name", "event/r25:event_title", "event/r25:event_description"]

	return {"%s" % space_id : [{y:x.findall("r25:%s" % y, namespace)[-1].text for y in attrList if len(x.findall("r25:%s" % y, namespace)) > 0 } for x in reservations]}

def isConflict(space_id):
	res = grabIDTimesInformationFromDB({'space_id' : space_id})
	
	tnow = datetime.datetime.now()

	tranges = [{"start" : datetime.datetime.strptime(''.join(y["reservation_start_dt"].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z'), "end" : datetime.datetime.strptime(''.join(y["reservation_end_dt"].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z')} for y in res]

	for x in tranges:
		if x["start"] > tnow:
			return False

		if x["start"] < tnow and x["end"] > tnow:
			return True

	return False

 
def listFreeRooms():
	qDict = grabSpaceInformationFromDB()
	freeRooms = []	
	for x in qDict:
		if isConflict(x["space_id"]) == False:
			freeRooms.append(x)

	return freeRooms

def flushSpaceInformation(searchDict = {}):
	dbspaces.delete_many(searchDict)

def flushIDTimesInformation(searchDict = {}):
	dbidtimes.delete_many(searchDict)

def flushRoomGPSInformation(searchDict = {}):
	dbroomtogps.delete_many(searchDict)

def refreshSpaceInformation():
	posts = dbspaces.posts
	results = posts.insert_many(parseWPILive())
	return results.inserted_ids

def grabSpaceInformationFromDB(searchDict = {}):
	posts = dbspaces.posts
	results = posts.find(searchDict)
	return list(results)

def refreshIDTimesInformation():
	posts = dbidtimes.posts

	rooms = grabSpaceInformationFromDB()

	for room in rooms:
		idtime = queryTimes(room["space_id"])
		print("Information: %s" % idtime)
		result = posts.insert_one(idtime)
		print("Updated Space ID: %s as %s" % (room["space_id"], result.inserted_id))
	
def grabIDTimesInformationFromDB(searchDict = {}):
	posts = dbidtimes.posts
	results = posts.find(searchDict)
	return list(results)

def grabRoomGPSInformationFromDB(searchDict = {}):
	posts = dbroomtogps.posts
	results = posts.find(searchDict)
	return list(results)

def distanceFormula(x1, x2, y1, y2):
	return (x2** 2 - x1 ** 2) ** (1/2) + (y2 ** 2 - y1 ** 2) ** (1/2)

def findNearbyRooms(GPS_coordinates):
	rCoord = grabRoomGPSInformationFromDB()
	lat = GPS_coordinates[0]
	lon = GPS_coordinates[1]

	distances = [{'room' : x['room'], 'distance' : distanceFormula(lat, rCoord['latitude'], lon, rCoord['longitude'])} for x in rCoord]
	
	sorted(distances, key = lambda x: x['distance'])

	rooms = listFreeRooms()
	
	avail = []
	for x in distances:
		for y in rooms:
			if y['space_name'] == x['room']:
				avail.append(y)

	return avail



if __name__ == "__main__":
    #print (refreshIDTimesInformation())

    app.run()
    
