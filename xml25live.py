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

from xml.etree.ElementTree import ElementTree
import xml
import requests
import datetime

namespace = {'r25' : 'http://www.collegenet.com/r25'}

# Pulls down all the spaces on campus
def querySpaces():
	tpath = "https://25live.collegenet.com/25live/data/wpi/run/spaces.xml"
	
	# query the API
	r = requests.get(tpath)
	tree = xml.etree.ElementTree.fromstring(r.content)
	
	# find all spaces
	spaceList = tree.findall("r25:space", namespace)
	attrList = ["space_id", "space_name", "formal_name", "partition_name", "max_capacity"]
	
	# pull out each space info
	queryDict = [{y : x.findall("r25:%s" % (y), namespace)[-1].text for y in attrList if len(x.findall("r25:%s" % (y), namespace)) > 0} for x in spaceList]

	
	# Do this later to pull features about each room!
	urlRInfo = "https://25live.collegenet.com/25live/data/wpi/run/space.xml?space_id=%s"
	for x in queryDict:
		print("Pulling room info on " + x["space_name"])
		r = requests.get(urlRInfo % (x["space_id"]))
		tree = xml.etree.ElementTree.fromstring(r.content)
		tree = tree.findall("r25:space", namespace)[-1]
		
		commentlist = tree.findall("r25:comments", namespace)[-1].text

		hour_attr = ["open", "close"]
		hourlist = [{y : z.findall("r25:%s" % (y), namespace)[-1].text for y in hour_attr} for z in tree.findall("r25:hours", namespace)]

		blackout_attr = ["blackout_profile_name", "blackout_init_start", "blackout_init_end"]
		blackoutlist = [{y : z.findall("r25:%s" % (y), namespace)[-1].text for y in blackout_attr} for z in tree.findall("r25:blackouts", namespace)]

		feature_attr = ["feature_name", "quantity"]
		featurelist = [{y : z.findall("r25:%s" % (y), namespace)[-1].text for y in feature_attr} for z in tree.findall("r25:feature", namespace)]
		featuremap = {y["feature_name"].replace(".", "") : y["quantity"] for y in featurelist}

		x["room_details"] = {"comments" : commentlist, "hours" : hourlist, "blackouts" : blackoutlist, "features" : featuremap}
	return queryDict

# Pulls down all the reservations for today for a given space
def queryTimes(space_id):
	tpath = "https://25live.collegenet.com/25live/data/wpi/run/rm_reservations.xml?space_id={0}&date_params=date_order%3A%20MDY%3B%24hour_inc%3A%201%3B%20minute_inc%3A%205%3B%20month_display%3A%20I%3B%20day_display%3A%20I%3B%20date_sep%3A%20S%3B%20time_display%3A%2012&scope=extended&browser=moz&include=closed+blackouts+pending+related&office_start=0000&office_end=2359&start_dt={1}&end_dt={2}&hr_format=12&office_hrs={3}"

	# TODO: use better date formatting library?
	current_date = datetime.date.today()
	dt = "%04d%02d%02d" % (current_date.year, current_date.month, current_date.day)
	start_dt = "%sT000000" % (dt)
	end_dt = "%sT235959" % (dt)
	office_hrs = "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23" # TODO: 25 live does not show 0-7

	# pull information for the given space today
	r = requests.get(tpath.format(space_id, start_dt, end_dt, office_hrs))
	tree = xml.etree.ElementTree.fromstring(r.content)
	
	# pull out all reservations and their metadata
	reservations = tree.findall("r25:space_reservation", namespace)
	attrList = ["reservation_start_dt", "reservation_end_dt", "event/r25:event_name", "event/r25:event_title", "event/r25:event_description"]

	return {"space_id" : space_id,
			"times" : [{y:x.findall("r25:%s" % y, namespace)[-1].text for y in attrList if len(x.findall("r25:%s" % y, namespace)) > 0 } for x in reservations]}

