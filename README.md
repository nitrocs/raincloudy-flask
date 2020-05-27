# raincloudy-flask
Python Flask API version of Melnor Raincloud Access using
[raincloudy](https://github.com/vanstinator/raincloudy). I use this with
[Hubitat](https://github.com/bdwilson/hubitat/tree/master/Raincloud).

## Work in progress / To Do
* Put all controllers/faucets into a json dict that will always show statues of
all devices vs. having to poll each valve indvivdually.
* Keep track locally if faucets are running and do more frequent update() polls
if there are things going on - otherwise, backoff on updates
