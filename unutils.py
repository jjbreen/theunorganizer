'''
Copyright 2016

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import undbdata
import math
import roomdata
import datetime

# gets all the free rooms near a coordinate point
def getRoomsNear(coords):
	rCoord = undbdata.getGpsMappings()
	if coords:
		lon = coords[0]
		lat = coords[1]
	else:
		# not valid coords, use center of WPI
		lon = -7993563.4
		lat = 5202228.6

	# find the distance to all the known rooms
	distances = [{'room' : [x['name'],y['name']],
				'distance' : math.hypot(lon - y['point'][0], lat - y['point'][1]),
				'gps' : y['point']} for x in rCoord for y in x['rooms']]
	
	rooms = undbdata.getSpaces()
	avail = []
	
	# map the rooms together in union and check the status
	for x in distances:
		for y in rooms:
			if y['space_id'] == room2id(x['room']):
				avail.append({'details': y,
							'distance': x['distance'],
							'coordinates': x['gps'],
							'status': 'taken' if isTakenNow(y['space_id']) else 'free'})

	# sort and choose the best one
	avail.sort(key=lambda x: (x['status'], x['distance']))
	if coords and len(avail) > 0 and avail[0]['status'] == 'free':
		avail[0]['status'] = 'best'
	return avail

# converts a room name to a 25 live space id
def room2id(nameTuple):
	for room in roomdata.roomdata:
		if room['gps'] == nameTuple:
			return room['live25'][1]

# checks to see if a given space is reserved right now, and for the next 30 minutes
def isTakenNow(space_id):
	res = undbdata.getReservations({'space_id' : space_id})[0]

	if len(res['times']) <= 0:
		return False

	tnow = datetime.datetime.now()
	tranges = [{"start" : datetime.datetime.strptime(''.join(y["reservation_start_dt"].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None), "end" : datetime.datetime.strptime(''.join(y["reservation_end_dt"].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)} for y in res['times']]

	for x in tranges:
		if (x["start"] < tnow and x["end"] > tnow) or (x['start'] < (tnow + datetime.timedelta(minutes=30)) and x['end'] > (tnow + datetime.timedelta(minutes=30))):
			return True
	return False



# manually called, will attempt to match room ID's together and prints out alist of those that it can and can't match
def automatchRooms():
	import re
	alldata = undbdata.getSpaces()
	
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

	print(tmpdata)

if __name__ == "__main__":
	automatchRooms()

