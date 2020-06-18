# Raincloudy Flask API
This flask API uses the [raincloudy](https://github.com/vanstinator/raincloudy)
python library.

I am not a Python programmer; this is really bad code. Please fix it. There is
no authentication because the expectation is that you're running this on your
internal, trusted home network. You've been warned.

WARNING: I only have 1 controller & 1 faucet, so while this *should* work for
multiples of each, it has not been tested.

# Installation (manual)
1. Install raincloudy, flask, flask-jsonpify, json
<pre>
# pip3 install raincloudy
# pip3 install flask
# pip3 install flask-jsonpify
# pip3 install json
</pre>
2. Change the login/password/port variables in the raincloudy_flask.py. My port in the example is 5059.
3. Change directory in the .service file to match where your raincloudy_flask.py file is.
4. Copy service file to /lib/systemd/system/ then enable it.
<pre>
# systemctl daemon-reload
# systemctl enable raincloudy.service
# systemctl start raincloudy.service 
</pre>

# Installation (Docker)
1. Grab the
[Dockerfile](https://raw.githubusercontent.com/bdwilson/raincloudy-flask/master/Dockerfile)
via wget and put it in a directory on your Docker server. Then run the commands
below from that directory
2. <code> # docker build -t ecovacs-api --build-arg EMAIL='your@email.address' --build-arg PASSWORD='your_password' --build-arg  .</code>
CTRL-C out of it when it's complete. PORT is optional and will default to 5059
3. Run your newly created image: <code> # docker run -p 5059:5059 --name raincloudy-flask -t raincloudy-flask</code> (if you changed the port when you built your image, you should also change it here)
4. That's it. If you need to troubleshoot your docker image, you can get into
it via:
<code> # docker exec -it raincloudy-flask /bin/bash</code> or 
<code># docker run -it raincloudy-flask /bin/bash</code> and then poke around and run the commands below in the troubleshooting section "sucks". 

# Usage
<pre>
# curl -s http://yourip:5059/api/status 
# curl -s http://yourip:5059/api/[controllerid|status]/[faucetid]/[open|close|auto|rain/[zone#]/[time in mins/0/1]
</pre>

# Hubitat
See [here](https://github.com/bdwilson/hubitat/master/Raincloud). 

# Troubleshooting
1. Your controller id and faucets should be listed when you start the image/script:
<pre>
Controller: d88039xxxxx  Status: Online
> Faucet: xxxx  Status: Online
 * Serving Flask app "raincloudy_flask" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5059/ (Press CTRL+C to quit)
</pre>
2. Test this inside, not hooked up before running in production. You can easily
hear the valves open and close.

Bugs/Contact Info
-----------------
Bug me on Twitter at [@brianwilson](http://twitter.com/brianwilson) or email me [here](http://cronological.com/comment.php?ref=bubba).
