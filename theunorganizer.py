from xml.etree.ElementTree import ElementTree
import xml
import requests
import datetime 
import time 
import roomdata
import json 

from flask import Flask
from flask import request 
from flask import render_template
from flask import Response 
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
    return render_template("index.html")

@app.route("/wpilive")
def getwpilib():
    return parseWPILive()

@app.route('/public/<path:path>')
def send_js(path):
    return send_from_directory('public', path)

@app.route('/api/closest', methods=['GET'])
def map_api():

	lon = float(request.args.get('longitude'))
	lat = float(request.args.get('latitude'))

	return Response(json.dumps(findNearbyRooms([lon, lat])), mimetype='application/json')

@app.route('/api/closed', methods=['GET'])
def closed_api():
	lon = float(request.args.get('longitude'))
	lat = float(request.args.get('latitude'))

	return Response(json.dumps(findTakenRooms([lon, lat])), mimetype='application/json')

@app.route('/api/update')
@app.route('/api/update/<int:utype>')
def update_db(utype = 0):
	if utype == 0:
		updateDB()
	elif utype == 1:
		refreshSpaceInformation()
	elif utype == 2:
		refreshIDTimesInformation()
	else:
		refreshRoomGPSInformation()

	return "ok"



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
	start_dt = "%sT000000" % (dt)
	end_dt = "%sT235959" % (dt)
	office_hrs = "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23"

	r = requests.get(tpath.format(space_id, start_dt, end_dt, office_hrs))
	
	print (tpath.format(space_id, start_dt, end_dt, office_hrs))

	tree = xml.etree.ElementTree.fromstring(r.content)

	reservations = tree.findall("r25:space_reservation", namespace)

	attrList = ["reservation_start_dt", "reservation_end_dt", "event/r25:event_name", "event/r25:event_title", "event/r25:event_description"]

	return {"space_id" : space_id,
			"times" : [{y:x.findall("r25:%s" % y, namespace)[-1].text for y in attrList if len(x.findall("r25:%s" % y, namespace)) > 0 } for x in reservations]}

def isConflict(space_id):
	res = grabIDTimesInformationFromDB({'space_id' : space_id})[0]
	
	print(res)

	if len(res['times']) <= 0:
		return False

	tnow = datetime.datetime.now()


	tranges = [{"start" : datetime.datetime.strptime(''.join(y["reservation_start_dt"].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None), "end" : datetime.datetime.strptime(''.join(y["reservation_end_dt"].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)} for y in res['times']]

	for x in tranges:
		if (x["start"] < tnow and x["end"] > tnow) or (x['start'] < (tnow + datetime.timedelta(minutes=30)) and x['end'] > (tnow + datetime.timedelta(minutes=30))):
			return True

	return False


def listTakenRooms():
	qDict = grabSpaceInformationFromDB()
	takenRooms = []	
	for x in qDict:
		if isConflict(x["space_id"]) == True:
			takenRooms.append(x)

	return takenRooms

def listFreeRooms():
	qDict = grabSpaceInformationFromDB()
	freeRooms = []	
	for x in qDict:
		if isConflict(x["space_id"]) == False:
			freeRooms.append(x)

	return freeRooms

def flushSpaceInformation(searchDict = {}):
	dbspaces.posts.delete_many(searchDict)

def flushIDTimesInformation(searchDict = {}):
	dbidtimes.posts.delete_many(searchDict)

def flushRoomGPSInformation(searchDict = {}):
	dbroomtogps.posts.delete_many(searchDict)

def refreshSpaceInformation():
	flushSpaceInformation()
	posts = dbspaces.posts
	results = posts.insert_many(parseWPILive())
	return results.inserted_ids

def grabSpaceInformationFromDB(searchDict = {}):
	posts = dbspaces.posts
	results = posts.find(searchDict)

	results = list(results)
	for x in results:
		del x['_id']

	return results

def refreshIDTimesInformation():
	flushIDTimesInformation()
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
	
	results = list(results)
	for x in results:
		del x['_id']


	return results 

def refreshRoomGPSInformation():
	flushRoomGPSInformation()
	posts = dbroomtogps.posts
	results = posts.insert_many(roomdata.fixCoordinates())

	conresults = posts.insert_many(roomdata.conData)

	return results.inserted_ids 

def grabRoomGPSInformationFromDB(searchDict = {}):
	posts = dbroomtogps.posts
	results = posts.find(searchDict)

	results = list(results)
	for x in results:
		del x['_id']

	return results 

def updateDB():
	refreshSpaceInformation();
	refreshIDTimesInformation();
	refreshRoomGPSInformation();

def distanceFormula(x1, x2, y1, y2):
	return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1/2)

def findNearbyRooms(GPS_coordinates):
	rCoord = grabRoomGPSInformationFromDB()
	lon = GPS_coordinates[0]
	lat = GPS_coordinates[1]

	distances = [{'room' : [x['name'],y['name']],
				'distance' : distanceFormula(lon, y['point'][0], lat, y['point'][1]),
				'gps' : y['point']} for x in rCoord for y in x['rooms']]
	
	sorted(distances, key = lambda x: x['distance'])

	rooms = listFreeRooms()
	
	avail = []
	for x in distances:
		for y in rooms:
			if y['space_id'] == transformRoomtoID(x['room']):
				avail.append({'details': y,
							'distance': x['distance'],
							'coordinates': x['gps'],
							'status': 'free'})

	avail = sorted(avail, key=lambda x: x['distance'])
	avail[0]['status'] = 'best'
	return avail

def findTakenRooms(GPS_coordinates):
	rCoord = grabRoomGPSInformationFromDB()
	lon = GPS_coordinates[0]
	lat = GPS_coordinates[1]

	distances = [{'room' : [x['name'],y['name']],
				'distance' : distanceFormula(lon, y['point'][0], lat, y['point'][1]),
				'gps' : y['point']} for x in rCoord for y in x['rooms']]
	
	rooms = listTakenRooms()
	
	avail = []
	for x in distances:
		for y in rooms:
			if y['space_id'] == transformRoomtoID(x['room']):
				avail.append({'details': y,
							'distance': x['distance'],
							'coordinates': x['gps'],
							'status': 'taken'})

	avail = sorted(avail, key=lambda x: x['distance'])
	return avail

def transformRoomtoID(nameTuple):
	for room in roomdata.roomdata:
		if room['gps'] == nameTuple:
			return room['live25'][1]


def automatchRooms():
	import re
	alldata = grabSpaceInformationFromDB()
	
	tmpdata = []

	for rm in alldata:
		m = re.match('([A-Z]{2}) [AB]?[0-9]{1,3}[A-F]?$', rm["space_name"])
		if m:
			print( rm["space_name"] + " - " + rm["space_id"])
			for floors in roomdata.allData:
				if re.match(m.group(1), floors["name"]):
					for room in floors["rooms"]:
						n = re.match('([ABab]?)([0-9]{1,3})([A-Fa-f]?)', room["name"])
						if not n:
							continue
						proper = "{} {}{:0>3}{}".format(m.group(1), n.group(1).upper(), int(n.group(2)), n.group(3).upper())
						if rm["space_name"] == proper:
							print("matched " + proper)
							tmpdata.append({"gps": [floors["name"], room["name"]], "live25": [rm["space_name"], rm["space_id"]]})
		else:
			print( "\t\t\t\t\t\t\t\t" + rm["space_name"] + " - " + rm["space_id"])
			pass

	print( tmpdata)


if __name__ == "__main__":
	app.run(debug = False, host="0.0.0.0")





    
