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
m = folium.Map(location=(locs_coords[0][1], locs_coords[0][0]), zoom_start=12)

# Global tooltip
tooltip = 'Click for more info'

i = 1
for coord in locs_coords:
    folium.Marker([coord[1],coord[0]],
                popup='<strong>{}</strong>'.format(i),
                tooltip=tooltip).add_to(m)
    i+=1


# generate optimal route in GeoJSON format
routes = clnt.directions(locs_coords, format='geojson', profile='driving-car', optimize_waypoints=True)

folium.GeoJson(routes, name='Meals on Wheels').add_to(m)

m.save('map.html')
print(routes)