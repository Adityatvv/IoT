
# A very simple Bottle Hello World app for you to get started with...
from bottle import default_app, route, template
import requests
import get_weather
rows=[]
@route('/')
def hello_world():
    req = requests.get('http://api.openweathermap.org/data/2.5/find?lat=41.1&lon=-81.3&cnt=10')
    data = req.json()
    rows=[]
    for i in range(0,10):
	    tempk = data['list'][i]['main']['temp']
	    tempc = tempk - 273.16
	    tempf = tempc * 1.8 + 32.0
	    f2 = data['list'][i]['coord']['lat']
	    f3 = data['list'][i]['coord']['lon']
	    nam = data['list'][i]['name']
	    #we = ['list'][i]['weather'][0]['main']
	    #humidity = data['list'][i]['main']['humidity']
	    rows.append((f2,f3,tempf,nam))
    return template('map', rows=rows)

@route('/project')
def hello_project():
    req = requests.get('https://data.sparkfun.com/output/aGOE6rY5mxcxX1GNnOKq.json?limit=100&gt[timestamp]=2015-07-30&timezone=America/New_York')
    data = req.json()
    rows=[]
    for i in reversed(xrange(100)):
	    lat = data[i]['latitude']
	    lon = data[i]['longitude']
	    tempc=data[i]['temperature']
	    #zip = data[i]['zip']
	    light=data[i]['light']
	    rows.append((lat,lon,str(light),str(tempc)))
    return template('map_project', rows=rows)


application = default_app()
