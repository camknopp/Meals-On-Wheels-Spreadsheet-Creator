from openrouteservice import client, places, directions, distance_matrix
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from geopy.geocoders import Nominatim
import json

api_key = '5b3ce3597851110001cf62484c5ca3f76ff944dfa2d23b773efec8d7'  # api key for openroute service
clnt = client.Client(key=api_key)

geolocator = Nominatim(user_agent='Meals On Wheels Route')

startpoint = geolocator.geocode("7 jencks road milford ma")

locs_addresses = ['hopkinton ma', 'ashland ma', 'holliston ma', 'east boston ma']
locs_coords = []

for loc in locs_addresses:
    curr = geolocator.geocode(loc)
    locs_coords.append((curr.longitude, curr.latitude))

request = {'locations': locs_coords,
           'profile': 'driving-car',
           'metrics': ['duration']}

locs_matrix = clnt.distance_matrix(**request)
print("Calculated {}x{} routes.".format(len(locs_matrix['durations']),len(locs_matrix['durations'][0])))

def getDistance(from_id, to_id):
    return int(locs_matrix['durations'][from_id][to_id])

tsp_size = len(locs_addresses)
num_routes = 1
start = 0

optimal_coords = []

if tsp_size > 0:
    routing = pywrapcp.RoutingModel(tsp_size, num_routes, start)
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()

    # Create the distance callback, which takes two arguments (the from and to node indices)
    # and returns the distance between these nodes.
    dist_callback = getDistance
    routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
    # Solve, returns a solution if any.
    assignment = routing.SolveWithParameters(search_parameters)
    if assignment:
        # Total cost of the 'optimal' solution.
        print("Total duration: " + str(round(assignment.ObjectiveValue(), 3) / 60) + " minutes\n")
        index = routing.Start(start) # Index of the variable for the starting node.
        route = ''
#         while not routing.IsEnd(index):
        for node in range(routing.nodes()):
            optimal_coords.append(locs_coords[routing.IndexToNode(index)])
            route += str(locs_addresses[routing.IndexToNode(index)]) + ' -> '
            index = assignment.Value(routing.NextVar(index))
        route += str(locs_addresses[routing.IndexToNode(index)])
        optimal_coords.append(locs_coords[routing.IndexToNode(index)])
        print("Route:\n" + route)




