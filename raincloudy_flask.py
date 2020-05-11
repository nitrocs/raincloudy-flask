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
# Usage: /api/[start|auto|stop|status|battery/[zone#]/[time in mins/0/1]
# 
# 
from flask import Flask, render_template, flash, request, jsonify
from raincloudy.core import RainCloudy
from raincloudy.faucet import RainCloudyFaucetZone
from raincloudy.helpers import serial_finder
from raincloudy import *
from pprint import pprint
import json

# App config.
DEBUG = False
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '326240760871083756038276035325'

valid_commands = ["start","auto", "stop", "status", "battery" ]

config = {
    "email": "EMAILADDRESS", # fill in your email
    "password": "PASSWORD" 
}
raincloudy = RainCloudy(config['email'], config['password'])

def sendCommand(command,zone,time):
	#if (valid_commands[command]):
	if command in str(valid_commands):
		raincloudy = RainCloudy(config['email'], config['password'])
		#my_vac = api.devices()[device]
		#vacbot = VacBot(api.uid, api.REALM, api.resource, api.user_access_token, my_vac, config['continent'])
		#time.sleep(o0.5)
		try:
			controller = raincloudy.controller.status
		except AttributeError:
			return("Controller not found")
		try: 
			faucet = raincloudy.controller.faucet.status
		except AttributeError:
			return("Faucet not found")
		
		#print(raincloudy.controllers)
		#print(raincloudy.controller.status)
		#print(raincloudy.controller.faucet.battery)
		#print(raincloudy.controller.faucet_battery)
		#test = raincloudy.controllers + raincloudy.controller.faucet_battery + raincloudy.status + raincloudy.controller.faucet.status
		#test = raincloudy.controller.status + raincloudy.controller.faucet.status +  raincloudy.controller.faucet.battery
	#	return(str(test))
		if (command == "battery"):
			return jsonify(battery=raincloudy.controller.faucet.battery)
		if (command == "status"):
			#raincloudy.controller.update()
			if (zone == 1):
				zone = raincloudy.controller.faucet.zone1
				auto_watering = getattr(zone,'auto_watering')
				is_watering = getattr(zone,'is_watering')
				watering_time = getattr(zone,'watering_time')
				rain_delay = getattr(zone,'rain_delay')
				name = getattr(zone,'name')
				return jsonify(zone="zone1",auto_watering=auto_watering, is_watering=is_watering, watering_time=watering_time, rain_delay=rain_delay, name=name)
				#battery=raincloudy.controller.faucet.battery)
			elif (zone == 2):
				zone = raincloudy.controller.faucet.zone2
				auto_watering = getattr(zone,'auto_watering')
				is_watering = getattr(zone,'is_watering')
				watering_time = getattr(zone,'watering_time')
				rain_delay = getattr(zone,'rain_delay')
				name = getattr(zone,'name')
				return jsonify(zone="zone2",auto_watering=auto_watering, is_watering=is_watering, watering_time=watering_time, rain_delay=rain_delay, name=name)
			elif (zone == 3):
				zone = raincloudy.controller.faucet.zone3
				auto_watering = getattr(zone,'auto_watering')
				is_watering = getattr(zone,'is_watering')
				watering_time = getattr(zone,'watering_time')
				rain_delay = getattr(zone,'rain_delay')
				name = getattr(zone,'name')
				return jsonify(zone="zone3",auto_watering=auto_watering, is_watering=is_watering, watering_time=watering_time, rain_delay=rain_delay, name=name)
			elif (zone == 4):
				zone = raincloudy.controller.faucet.zone4
				auto_watering = getattr(zone,'auto_watering')
				is_watering = getattr(zone,'is_watering')
				watering_time = getattr(zone,'watering_time')
				rain_delay = getattr(zone,'rain_delay')
				name = getattr(zone,'name')
				return jsonify(zone="zone4",auto_watering=auto_watering, is_watering=is_watering, watering_time=watering_time, rain_delay=rain_delay, name=name)
			else:
				return("Error: /api/status/[zone 1-4]");
				# should we return all statuses? Would it matter if
				# we break this down to individual HE drivers?
				print("{")
				count=1
				for zone in raincloudy.controller.faucet.zones:
					#print(getattr(zone,'is_watering'))
					print("'zone" + str(count) + "':")
					#print(zone._to_dict())
					auto_watering = getattr(zone,'auto_watering')
					is_watering = getattr(zone,'is_watering')
					watering_time = getattr(zone,'watering_time')
					rain_delay = getattr(zone,'rain_delay')
					if (count < 4):
						print(",")
					count+=1
				print("}")
				#return jsonify(out)
		if (command == "start") and (time > 0) and (time < 61):
			if (zone == 1):
				raincloudy.controller.faucet.zone1.watering_time=time  #manual_watering
				return(jsonify(zone="zone1",watering_time=time))
			elif (zone == 2):
				raincloudy.controller.faucet.zone2.watering_time=time
				return(jsonify(zone="zone2",watering_time=time))
			elif (zone == 3):
				raincloudy.controller.faucet.zone3.watering_time=time
				return(jsonify(zone="zone3",watering_time=time))
			elif (zone == 4):
				raincloudy.controller.faucet.zone4.watering_time=time
				return(jsonify(zone="zone4",watering_time=time))
			else:
				return("Error: /api/start/[zone 1-4]/[1-60]")
		if (command == "auto") and (zone > 0) and (zone < 5) and (time <= 1):
			if (zone == 1):
				raincloudy.controller.faucet.zone1.auto_watering=time
				#return(raincloudy.controller.faucet.zone1)
				return(jsonify(zone="zone1",auto_watering=time))
			elif (zone == 2):
				raincloudy.controller.faucet.zone2.auto_watering=time
				return(jsonify(zone="zone2",auto_watering=time))
			elif (zone == 3):
				raincloudy.controller.faucet.zone3.auto_watering=time
				return(jsonify(zone="zone3",auto_watering=time))
			elif (zone == 4):
				raincloudy.controller.faucet.zone4.auto_watering=time
				return(jsonify(zone="zone4",auto_watering=time))
			else:
				return("Error: /api/auto/[zone 1-4]/[0/1]")
		if (command =="stop"):
			if (zone == 1):
				raincloudy.controller.faucet.zone1.watering_time=0  #manual_watering
				return(jsonify(zone="zone1",watering_time=0))
			elif (zone == 2):
				raincloudy.controller.faucet.zone2.watering_time=0
				return(jsonify(zone="zone2",watering_time=0))
			elif (zone == 3):
				raincloudy.controller.faucet.zone3.watering_time=0
				return(jsonify(zone="zone3",watering_time=0))
			elif (zone == 4):
				raincloudy.controller.faucet.zone4.watering_time=0
				return(jsonify(zone="zone4",watering_time=0))
			else:
				print("Error: /api/stop/[zone 1-4]")

@app.route("/", methods=['GET'])
def info():
	return("/api/[start|stop|auto|status|battery/[zone#]/[time in mins/0/1]")

@app.route("/api/<string:command>", methods=['GET'])
@app.route("/api/<string:command>/<int:zone>", methods=['GET'])
@app.route("/api/<string:command>/<int:zone>/<int:time>", methods=['GET'])
def api(command,zone=0,time=0):
	try:
		val = sendCommand(command,zone,time)
		#print("VAL:" + val)
		return val
		#if val:
		#	return str(val)
		#else:
		#	return 'Error executing ' + command
	except:
		return "Error executing " + command
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5058, debug=False)


