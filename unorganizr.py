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

