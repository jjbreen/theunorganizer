from xml.etree.ElementTree import ElementTree
import requests
import datetime 

from flask import Flask

app = Flask(__name__)

namespace = {'r25' : 'http://www.collegenet.com/r25'}

@app.route("/")
def hello():
    return "Hello World!"


def parseWPILive(treePath):
	

	tree = ElementTree()
	tree.parse(treePath)
	root = tree.getroot()

	spaceList = root.findall("r25:space", namespace)
	

	attrList = ["space_id", "space_name", "formal_name", "partition_name", "max_capacity"]
	queryDict = [{y : x.findall("r25:%s" % (y), namespace)[0].text for y in attrList} for x in spaceList]

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

	r = request.get(tpath.format(space_id, start_dt, end_dt, office_hrs))
	
	tree = xml.etree.ElementTree.fromstring(r.content)

	reservations = tree.findall("r25:space_reversation", namespace)

	attrList = ["reservation_start_dt", "reservation_end_dt", "event_name", "event_title"]
	return [{y: x.findall("r25:%s" % y, namespace)[0].text for y in attrList} for x in reservations]

def isConflict(space_id):
	res = queryTimes(space_id)
	
	 


if __name__ == "__main__":
    app.run()
