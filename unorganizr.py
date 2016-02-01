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

import json
import undbdata
import unutils

from flask import Flask
from flask import request
from flask import render_template
from flask import Response

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/location")
def getlocation():
    return render_template("location.html")

@app.route('/api/rooms', methods=['GET'])
def map_api():
	if request.args.get('longitude') and request.args.get('latitude'):
		coords = [float(request.args.get('longitude')), float(request.args.get('latitude'))]
	else:
		coords = None
	return Response(json.dumps(unutils.getRoomsNear(coords)), mimetype='application/json')

@app.route('/api/update')
@app.route('/api/update/<int:utype>')
def update_db(utype = 0):
	if utype == 0:
		undbdata.updateDB()
	elif utype == 1:
		undbdata.pullSpaces()
	elif utype == 2:
		undbdata.pullReservations()
	else:
		undbdata.pullGpsMappings()

	return "ok"

if __name__ == "__main__":
	app.run(debug = True)

