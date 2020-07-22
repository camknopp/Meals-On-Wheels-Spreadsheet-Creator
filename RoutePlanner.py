from openrouteservice import client, places, directions, distance_matrix
from geopy.geocoders import Nominatim
import json
import folium

# api key for openrouteservice (which will figure out the optimal route)
api_key = '5b3ce3597851110001cf62484c5ca3f76ff944dfa2d23b773efec8d7'
clnt = client.Client(key=api_key)

geolocator = Nominatim(user_agent='Meals On Wheels Route')

locs_addresses = ['milford ma', 'boston ma', 'hopkinton ma', 'east boston']
locs_coords = []

# convert above addresses to coordinates using geopy
for loc in locs_addresses:
    curr = geolocator.geocode(loc) 
    locs_coords.append((curr.longitude, curr.latitude))

# create folium map
m = folium.Map(location=locs_coords[0], zoom_start=12)
m.save('map.html')

# generate optimal route in GeoJSON format
routes = clnt.directions(locs_coords, format='geojson', profile='driving-car', optimize_waypoints=True)

print(routes)