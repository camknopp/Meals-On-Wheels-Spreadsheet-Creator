from openrouteservice import client, places, directions, distance_matrix
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from geopy.geocoders import Nominatim
import json

api_key = '5b3ce3597851110001cf62484c5ca3f76ff944dfa2d23b773efec8d7'  # api key for openroute service
clnt = client.Client(key=api_key)

geolocator = Nominatim(user_agent='Meals On Wheels Route')

locs_addresses = ['milford ma', 'boston ma', 'hopkinton ma']
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

# tsp_size = len(locs_addresses)
tsp_size = len(locs_matrix)
num_routes = 1
start = 0

optimal_coords = []

if tsp_size > 0:
    manager = pywrapcp.RoutingIndexManager(tsp_size,
                                       num_routes, start)
    # routing = pywrapcp.RoutingModel(tsp_size, num_routes, start)
    routing = pywrapcp.RoutingModel(manager)
    # search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()

    # Create the distance callback, which takes two arguments (the from and to node indices)
    # and returns the distance between these nodes.
    # dist_callback = getDistance
    dist_callback = routing.RegisterTransitCallback(getDistance)
    routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve, returns a solution if any.
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        # Total cost of the 'optimal' solution.
        print("Total duration: " + str(round(solution.ObjectiveValue(), 3) / 60) + " minutes\n")
        index = routing.Start(start) # Index of the variable for the starting node.
        route = ''
#         while not routing.IsEnd(index):
        for node in range(routing.nodes()):
            optimal_coords.append(locs_coords[manager.IndexToNode(index)])
            route += str(locs_addresses[manager.IndexToNode(index)]) + ' -> '
            index = solution.Value(routing.NextVar(index))
        route += str(locs_addresses[manager.IndexToNode(index)])
        optimal_coords.append(locs_coords[manager.IndexToNode(index)])
        print("Route:\n" + route)

request = {'coordinates': optimal_coords,
           'profile': 'driving-car',
           'geometry': 'true',
           'format_out': 'geojson',
          }
request['coordinates'] = optimal_coords
optimal_route = clnt.directions(**request)

optimal_duration = 0
optimal_duration = optimal_route['features'][0]['properties']['summary']['duration'] / 60
print("Route duration is {}".format(optimal_duration))





