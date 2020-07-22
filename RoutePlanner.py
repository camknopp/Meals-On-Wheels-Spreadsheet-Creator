import json
import folium
from openrouteservice import client, places, directions, distance_matrix
from geopy.geocoders import Nominatim
from statistics import median

# api key for openrouteservice (which will figure out the optimal route)
api_key = '5b3ce3597851110001cf62484c5ca3f76ff944dfa2d23b773efec8d7'
clnt = client.Client(key=api_key)

geolocator = Nominatim(user_agent='Meals On Wheels Route')

locs_addresses = ['64 pine street milford ma', '122 west spruce street milford ma', '8 della street milford ma',
                  '14 lawrence street milford ma', '17 lawrence street milford ma', '59 lawrence street milford ma',
                  '6 iadarola avenue milford ma', '36 highland street milford ma', '21 harding street milford ma', '8 western ave milford ma', '17 deluca rd milford ma', '3 prospect heights milford ma', '6 prospect heights milford ma', '34 prospect heights milford ma', ' 87 prospect heights milford ma']
locs_coords = []
latitudes = []
longitudes = []

# convert above addresses to coordinates using geopy
for loc in locs_addresses:
    curr = geolocator.geocode(loc)
    # print(curr.address)
    locs_coords.append((curr.longitude, curr.latitude))
    latitudes.append(curr.latitude)
    longitudes.append(curr.longitude)
    

# create folium map
m = folium.Map(location=(median(latitudes), median(longitudes)), zoom_start=15)

i = 1
for coord in locs_coords:
    folium.Marker([coord[1], coord[0]],
                  popup='<strong>{}</strong>'.format(i)).add_to(m)
    i += 1


def style_function(color):
    return lambda feature: dict(color=color,
                                weight=3,
                                opacity=1)


# generate optimal route in GeoJSON format
locs_coords.append(locs_coords[0])
routes = clnt.directions(locs_coords, format='geojson',
                         profile='driving-car', optimize_waypoints=True)

# overlay GeoJSON files on folium map
folium.GeoJson(routes, name='route').add_to(m)

# save map
m.save('map.html')
print(routes)
