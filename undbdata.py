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

import xml25live
import roomdata
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
dbspaces = client.db_spaces
dbidtimes = client.db_idtimes
dbroomtogps = client.db_roomgps

# updateDB
def updateAll():
	pullSpaces();
	pullReservations();
	pullGpsMappings();

# DELETEs all spaces matching the MongoDB search dict
def deleteSpaces(searchDict = {}):
	dbspaces.posts.delete_many(searchDict)

# DELETEs all reservations matching the MongoDB search dict
def deleteReservations(searchDict = {}):
	dbidtimes.posts.delete_many(searchDict)

# DELETEs all gps info matching the MongoDB search dict
def deleteGpsMappings(searchDict = {}):
	dbroomtogps.posts.delete_many(searchDict)

# GETs all spaces from 25 live cache
def getSpaces(searchDict = {}):
	return cleanMongoIDs(dbspaces.posts.find(searchDict))

# GETs all reservations from 25 live cache
def getReservations(searchDict = {}):
	return cleanMongoIDs(dbidtimes.posts.find(searchDict))

# GETs all gps info from mongo cache
def getGpsMappings(searchDict = {}):
	return cleanMongoIDs(dbroomtogps.posts.find(searchDict))
	
# REFRESHs all spaces from 25 live
def pullSpaces():
	deleteSpaces()
	results = dbspaces.posts.insert_many(xml25live.querySpaces())

# REFRESHs all reservations from 25 live
def pullReservations():
	deleteReservations()
	for room in getSpaces():
		idtime = xml25live.queryTimes(room["space_id"])
		print("Information: %s" % idtime)
		result = dbidtimes.posts.insert_one(idtime)
		print("Updated Space ID: %s as %s" % (room["space_id"], result.inserted_id))

# REFRESHs all GPS mappings from roomdata
def pullGpsMappings():
	deleteGpsMappings()
	dbroomtogps.posts.insert_many(roomdata.fixCoordinates())
	dbroomtogps.posts.insert_many(roomdata.conData)

# removes the un-JSON-able Mongo ID from a result set
def cleanMongoIDs(data):
	results = list(data)
	
	# remove the un-JSON-able Mongo ID
	for x in results:
		del x['_id']
	return results

