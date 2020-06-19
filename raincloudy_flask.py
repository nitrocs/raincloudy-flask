#!/usr/bin/python3
#
# 5/2020 - https://github.com/bdwilson/rainycloud-flask
#
# sudo apt-get install python3 python3-pip 
# sudo pip3 install flask-jsonpify
# sudo pip3 install flask
# sudo pip3 install raincloudy
#
# Set your email, password
# 
# Usage: /api/[controllerid]/[valveid]/[open|auto|close|status|battery/[zone#]/[time in mins/0/1]
# 
from flask import Flask, render_template, flash, request, jsonify
from raincloudy.core import RainCloudy
from raincloudy.faucet import RainCloudyFaucetZone
from raincloudy.controller import RainCloudyController 
from raincloudy.helpers import generate_soup_html, faucet_serial_finder, controller_serial_finder
from raincloudy import *
from pprint import pprint
import json

# App config.
DEBUG = False
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '326240760871083756038276035325'

valid_commands = ["open","auto", "close", "status", "rain" ]
api_commands = "[controllerid]/[faucetid]/[open|close|status|rain/[zone#]/[time in mins/0/1]"

config = {
    "email": "email", # fill in your email
    "password": "password" 
}

controllers = {}

rdy = RainCloudy(config['email'], config['password'], ssl_warnings=False)
rdy.update()
for controller in rdy.controllers:
	print("Controller: " + controller.id + "  Status: " + controller.status)
	for faucet in controller.faucets:
		print("> Faucet: " + faucet.id + "  Status: " + faucet.status)

def status (rc):
	rc.update()
	# get controllers
	for controller in rc.controllers:
		if not controllers.get("controllers"):
			controllers['controllers'] = {}
		if not controllers['controllers'].get(controller.id):
			controllers["controllers"][controller.id] = {}
		controllers["controllers"][controller.id]['status']=controller.status
		controllers["controllers"][controller.id]['name']=controller.name
		controllers["controllers"][controller.id]['id']=controller.id

		# get faucets
		if not controllers["controllers"][controller.id].get("faucets"):
			controllers["controllers"][controller.id]['faucets'] = {}
		for faucet in controller.faucets:
			if not controllers["controllers"][controller.id]['faucets'].get(faucet.id):
				controllers["controllers"][controller.id]['faucets'][faucet.id] = {}
			controllers["controllers"][controller.id]['faucets'][faucet.id]['name']=faucet.name
			controllers["controllers"][controller.id]['faucets'][faucet.id]['status']=faucet.status
			controllers["controllers"][controller.id]['faucets'][faucet.id]['battery']=faucet.battery
			controllers["controllers"][controller.id]['faucets'][faucet.id]['id']=faucet.id
			
			# get valves/zones
			if not controllers["controllers"][controller.id]['faucets'][faucet.id].get("valves"):
				controllers["controllers"][controller.id]['faucets'][faucet.id]['valves'] = {}
			for zone in faucet.zones:
				if zone.id not in controllers["controllers"][controller.id]['faucets'][faucet.id]['valves']:
					controllers["controllers"][controller.id]['faucets'][faucet.id]['valves'][zone.id] = {}
				#zone.update()
				controllers["controllers"][controller.id]['faucets'][faucet.id]['valves'][zone.id]['name']=zone.name
				controllers["controllers"][controller.id]['faucets'][faucet.id]['valves'][zone.id]['valve']=zone.id
				controllers["controllers"][controller.id]['faucets'][faucet.id]['valves'][zone.id]['id']=zone.id
				controllers["controllers"][controller.id]['faucets'][faucet.id]['valves'][zone.id]['auto_watering']=zone.auto_watering
				controllers["controllers"][controller.id]['faucets'][faucet.id]['valves'][zone.id]['is_watering']=zone.is_watering
				controllers["controllers"][controller.id]['faucets'][faucet.id]['valves'][zone.id]['rain_delay']=zone.rain_delay
				controllers["controllers"][controller.id]['faucets'][faucet.id]['valves'][zone.id]['watering_time']=zone.watering_time
	return controllers

def set (rc,cid,fid,zid,attr,val):
	for controller in rc.controllers:
		if ((controller.id == cid) and (controller.status == 'Online')):
			for faucet in controller.faucets:
				if ((faucet.id == fid) and (faucet.status == 'Online')):
					for zone in faucet.zones:
						if (zone.id == zid):
							zid = zid - 1
							ret = setattr(faucet.zones[zid],attr,val)
							return True

def sendCommand (c,f,command,zone,time):
	if command in str(valid_commands):
		if (command == "status"):
			return(status(rdy))
		elif (command == "open") and (time >= 0) and (time < 61) and (zone > 0) and (zone < 5):
			if (set(rdy,c,f,zone,'manual_watering',time)):
				return(status(rdy))
		elif (command == "auto") and (zone > 0) and (zone < 5) and (time <= 1):
			if (set(rdy,c,f,zone,"auto_watering",time)):
				return(status(rdy))
		elif (command == "close"):
			if (set(rdy,c,f,zone,"manual_watering",0)):
				return(status(rdy))
		elif (command == "rain") and (time >= 0) and (time < 8) and (zone > 0) and (zone < 5):
			if (set(rdy,c,f,zone,"rain_delay",time)):
				return(status(rdy))
		else:
			return(api_commands)
	else:
		return(api_commands)

#@app.route("/", methods=['GET'])
#def info():
#	return(api_commands)

@app.route("/api/status", methods=['GET'])
def doStatus():
	try:
		val=status(rdy)
		return(jsonify(val))
	except:
		return "Error executing status"

@app.route("/api/<string:controller>/<string:faucet>/<string:command>", methods=['GET'])
@app.route("/api/<string:controller>/<string:faucet>/<string:command>/<int:zone>", methods=['GET'])
@app.route("/api/<string:controller>/<string:faucet>/<string:command>/<int:zone>/<int:time>", methods=['GET'])
def api(controller,faucet,command,zone=0,time=0):
	try:
		val = sendCommand(controller,faucet,command,zone,time)
		return(jsonify((val)))
	except:
		return "Error executing " + command
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5059, debug=False)


