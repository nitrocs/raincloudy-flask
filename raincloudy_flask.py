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

valid_commands = ["open","auto", "close", "status", "battery" ]

config = {
    "email": "EMAILADDRESS", # fill in your email
    "password": "PASSWORD" 
}

rdy = RainCloudy(config['email'], config['password'], ssl_warnings=False)

def sendCommand(c,f,command,zone,time):
	#if (valid_commands[command]):
	if command in str(valid_commands):
		rdy.update()
		for controller in rdy.controllers:
			if ((controller.id == c) and (controller.status == 'Online')):
				for faucet in controller.faucets:
					if ((faucet.id == f) and (faucet.status == 'Online')):
						z = zone - 1
						pZone = "zone" + str(zone)
						if (command == "battery"):
							return jsonify(battery=faucet.battery)
						elif (command == "status"):
							if (zone > 0 and zone < 5):
								watering_time = getattr(faucet.zones[z],'watering_time')
								auto_watering = getattr(faucet.zones[z],'auto_watering')
								is_watering = getattr(faucet.zones[z],'is_watering')
								rain_delay = getattr(faucet.zones[z],'rain_delay')
								name = getattr(faucet.zones[z],'name')
								return(jsonify(zone=pZone,auto_watering=auto_watering,is_watering=is_watering,watering_time=watering_time,rain_delay=rain_delay,name=name))
							else:
								return("/api/[controllerid]/[faucetid]/[open|close|status|battery/[zone#]/[time in mins/0/1]")
						elif (command == "open") and (time > 0) and (time < 61) and (zone > 0) and (zone < 5):
							setattr(faucet.zones[z], 'manual_watering', time)
							return(jsonify(zone=pZone,watering_time=time))
						elif (command == "auto") and (zone > 0) and (zone < 5) and (time <= 1):
							setattr(faucet.zones[z], 'auto_watering', time)
							pprint("here")
							return(jsonify(zone=pZone,auto_watering=time))
						elif (command =="close"):
							setattr(faucet.zones[z], 'manual_watering', 0)
							return(jsonify(zone=pZone,watering_time=0))
						else:
							return("/api/[controllerid]/[faucetid]/[open|close|status|battery/[zone#]/[time in mins/0/1]")
					else:
						return("Invalid faucet ID or faucet ID offline")
			else:
				return("Invalid controller ID. Check your controller id in your app - controller ID is case sensitive")
	else:
		return("/api/[controllerid]/[faucetid]/[open|close|status|battery/[zone#]/[time in mins/0/1]")

@app.route("/", methods=['GET'])
def info():
	return("/api/[controllerid]/[faucetid]/[open|close|status|battery/[zone#]/[time in mins/0/1]")

@app.route("/api/<string:controller>/<string:faucet>/<string:command>", methods=['GET'])
@app.route("/api/<string:controller>/<string:faucet>/<string:command>/<int:zone>", methods=['GET'])
@app.route("/api/<string:controller>/<string:faucet>/<string:command>/<int:zone>/<int:time>", methods=['GET'])
def api(controller,faucet,command,zone=0,time=0):
	try:
		val = sendCommand(controller,faucet,command,zone,time)
		return val
	except:
		return "Error executing " + command
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5058, debug=False)


