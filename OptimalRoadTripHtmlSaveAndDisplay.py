"""
Randy Olson's Shortest Route Program modified By Andrew Liesinger to:
    1: Detect waypoints file at runtime - if found use it, otherwise look up distances via google calls (and then save to waypoint file)
    2: Dynamically create and open an HTML file showing the route when a shorter route is found
    3: Make it easier to tinker with the Generation / Population parameters
"""
from __future__ import print_function
from itertools import combinations
import googlemaps
import pandas as pd
import numpy as np
import os.path
import random
import webbrowser

GOOGLE_MAPS_API_KEY = "Your Key Here"
waypoints_file = "my-waypoints-dist-dur.tsv"

# This is the general filename - as shorter routes are discovered the Population fitness score will be inserted into the filename
# so that interim results are saved for comparision.  The actual filenames using the default below will be:
# Output_<Population Fitness Score>.html
output_file = 'Output.html'

# parameters for the Genetic algoritim
thisRunGenerations = 5000
thisRunPopulation_size = 100

all_waypoints = ["Sector 1,Chandigarh",
                 "Sector 2,Chandigarh",
                 "Sector 3,Chandigarh",
                 "Sector 4,Chandigarh",
                 "Sector 5,Chandigarh",
                 "Sector 6,Chandigarh",
                 "Sector 7,Chandigarh",
                 "Sector 8,Chandigarh",
                 "Sector 9,Chandigarh",
                 "Sector 10,Chandigarh",
                 "Sector 11,Chandigarh",
                 "Sector 12,Chandigarh",
                 "Sector 13,Chandigarh",
                 "Sector 14,Chandigarh",
                 "Sector 15,Chandigarh",
                 "Sector 16,Chandigarh",
                 "Sector 17,Chandigarh",
                 "Sector 18,Chandigarh",
                 "Sector 19,Chandigarh",
                 "Sector 20,Chandigarh",
                 "Sector 21,Chandigarh",
                 "Sector 22,Chandigarh",
                 "Sector 23,Chandigarh",
                 "Sector 24,Chandigarh",
                 "Sector 25,Chandigarh",
                 "Sector 26,Chandigarh",
                 "Sector 27,Chandigarh",
                 "Sector 28,Chandigarh",
                 "Sector 29,Chandigarh",
                 "Sector 30,Chandigarh",
                 "Sector 31,Chandigarh",
                 "Sector 32,Chandigarh",
                 "Sector 33,Chandigarh",
                 "Sector 34,Chandigarh",
                 "Sector 35,Chandigarh",
                 "Sector 36,Chandigarh",
                 "Sector 37,Chandigarh",
                 "Sector 38,Chandigarh",
                 "Sector 39,Chandigarh",
                 "Sector 40,Chandigarh",
                 "Sector 41,Chandigarh",
                 "Sector 42,Chandigarh",
                 "Sector 43,Chandigarh",
                 "Sector 44,Chandigarh",
                 "Sector 45,Chandigarh",
                 "Sector 46,Chandigarh",
                 ]


def CreateOptimalRouteHtmlFile(optimal_route, distance, display=True):
    optimal_route = ['Sector 1, Chandigarh','Sector 45, Chandigarh']
    optimal_route += [optimal_route[0]]

    Page_1 = """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
        <meta name="description" content="Randy Olson uses machine learning to find the optimal road trip across the U.S.">
        <meta name="author" content="Randal S. Olson">

        <title>The optimal road trip across the U.S. according to machine learning</title>
        <style>
          html, body, #map-canvas {
            height: 100%;
            margin: 0px;
            padding: 0px
          }
          #panel {
            position: absolute;
            top: 5px;
            left: 50%;
            margin-left: -180px;
            z-index: 5;
            background-color: #fff;
            padding: 10px;
            border: 1px solid #999;
          }
        </style>
        <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCucpOtseSkHzyALg9A_8DnEzHT7ID0Y3c&libraries=places"></script>
        <script>
            var routes_list = []
            var markerOptions = {icon: "http://maps.gstatic.com/mapfiles/markers2/marker.png"};
            var directionsDisplayOptions = {preserveViewport: true,
                                            markerOptions: markerOptions};
            var directionsService = new google.maps.DirectionsService();
            var map;

            function initialize() {
              var center = new google.maps.LatLng(30.7333, 76.7794);
              var mapOptions = {
                zoom: 13,
                center: center
              };
              map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
              for (i=0; i<routes_list.length; i++) {
                routes_list[i].setMap(map); 
              }
            }

            function calcRoute(start, end, routes) {

              var directionsDisplay = new google.maps.DirectionsRenderer(directionsDisplayOptions);

              var waypts = [];
              for (var i = 0; i < routes.length; i++) {
                waypts.push({
                  location:routes[i],
                  stopover:true});
                }

              var request = {
                  origin: start,
                  destination: end,
                  waypoints: waypts,
                  optimizeWaypoints: false,
                  travelMode: google.maps.TravelMode.DRIVING
              };

              directionsService.route(request, function(response, status) {
                if (status == google.maps.DirectionsStatus.OK) {
                    directionsDisplay.setDirections(response);      
                }
              });

              routes_list.push(directionsDisplay);
            }

            function createRoutes(route) {
                // Google's free map API is limited to 10 waypoints so need to break into batches
                route.push(route[0]);
                var subset = 0;
                while (subset < route.length) {
                    var waypointSubset = route.slice(subset, subset + 10);

                    var startPoint = waypointSubset[0];
                    var midPoints = waypointSubset.slice(1, waypointSubset.length - 1);
                    var endPoint = waypointSubset[waypointSubset.length - 1];

                    calcRoute(startPoint, endPoint, midPoints);

                    subset += 9;
                }
            }
    """
    Page_2 = """

            createRoutes(optimal_route);

            google.maps.event.addDomListener(window, 'load', initialize);

        </script>
      </head>
      <body>
        <div id="map-canvas"></div>
      </body>
    </html>
    """

    localoutput_file = output_file.replace('.html', '_' + str(distance) + '.html')
    with open(localoutput_file, 'w') as fs:
        fs.write(Page_1)
        fs.write("\t\t\toptimal_route = {0}".format(str(optimal_route)))
        fs.write(Page_2)

    if display:
        webbrowser.open_new_tab(localoutput_file)


def compute_fitness(solution):
    """
        This function returns the total distance traveled on the current road trip.

        The genetic algorithm will favor road trips that have shorter
        total distances traveled.
    """

    solution_fitness = 0.0

    for index in range(len(solution)):
        waypoint1 = solution[index - 1]
        waypoint2 = solution[index]
        solution_fitness += waypoint_distances[frozenset([waypoint1, waypoint2])]

    return solution_fitness


def generate_random_agent():
    """
        Creates a random road trip from the waypoints.
    """

    new_random_agent = list(all_waypoints)
    random.shuffle(new_random_agent)
    return tuple(new_random_agent)


def mutate_agent(agent_genome, max_mutations=3):
    """
        Applies 1 - `max_mutations` point mutations to the given road trip.

        A point mutation swaps the order of two waypoints in the road trip.
    """

    agent_genome = list(agent_genome)
    num_mutations = random.randint(1, max_mutations)

    for mutation in range(num_mutations):
        swap_index1 = random.randint(0, len(agent_genome) - 1)
        swap_index2 = swap_index1

        while swap_index1 == swap_index2:
            swap_index2 = random.randint(0, len(agent_genome) - 1)

        agent_genome[swap_index1], agent_genome[swap_index2] = agent_genome[swap_index2], agent_genome[swap_index1]

    return tuple(agent_genome)


def shuffle_mutation(agent_genome):
    """
        Applies a single shuffle mutation to the given road trip.

        A shuffle mutation takes a random sub-section of the road trip
        and moves it to another location in the road trip.
    """

    agent_genome = list(agent_genome)

    start_index = random.randint(0, len(agent_genome) - 1)
    length = random.randint(2, 20)

    genome_subset = agent_genome[start_index:start_index + length]
    agent_genome = agent_genome[:start_index] + agent_genome[start_index + length:]

    insert_index = random.randint(0, len(agent_genome) + len(genome_subset) - 1)
    agent_genome = agent_genome[:insert_index] + genome_subset + agent_genome[insert_index:]

    return tuple(agent_genome)


def generate_random_population(pop_size):
    """
        Generates a list with `pop_size` number of random road trips.
    """

    random_population = []
    for agent in range(pop_size):
        random_population.append(generate_random_agent())
    return random_population


def run_genetic_algorithm(generations=5000, population_size=100):
    """
        The core of the Genetic Algorithm.

        `generations` and `population_size` must be a multiple of 10.
    """

    current_best_distance = -1
    population_subset_size = int(population_size / 10.)
    generations_10pct = int(generations / 10.)

    # Create a random population of `population_size` number of solutions.
    population = generate_random_population(population_size)

    # For `generations` number of repetitions...
    for generation in range(generations):

        # Compute the fitness of the entire current population
        population_fitness = {}

        for agent_genome in population:
            if agent_genome in population_fitness:
                continue

            population_fitness[agent_genome] = compute_fitness(agent_genome)

        # Take the top 10% shortest road trips and produce offspring each from them
        new_population = []
        for rank, agent_genome in enumerate(sorted(population_fitness,
                                                   key=population_fitness.get)[:population_subset_size]):
            if (generation % generations_10pct == 0 or generation == generations - 1) and rank == 0:
                current_best_genome = agent_genome
                print("Generation %d best: %d | Unique genomes: %d" % (generation,
                                                                       population_fitness[agent_genome],
                                                                       len(population_fitness)))
                print(agent_genome)
                print("")

                # If this is the first route found, or it is shorter than the best route we know,
                # create a html output and display it
                if population_fitness[agent_genome] < current_best_distance or current_best_distance < 0:
                    current_best_distance = population_fitness[agent_genome]
                    CreateOptimalRouteHtmlFile(agent_genome, current_best_distance, False)

            # Create 1 exact copy of each of the top road trips
            new_population.append(agent_genome)

            # Create 2 offspring with 1-3 point mutations
            for offspring in range(2):
                new_population.append(mutate_agent(agent_genome, 3))

            # Create 7 offspring with a single shuffle mutation
            for offspring in range(7):
                new_population.append(shuffle_mutation(agent_genome))

        # Replace the old population with the new population of offspring 
        for i in range(len(population))[::-1]:
            del population[i]

        population = new_population
    return current_best_genome


if __name__ == '__main__':
    # If this file exists, read the data stored in it - if not then collect data by asking google
    print("Begin finding shortest route")
    file_path = waypoints_file
    if os.path.exists(file_path):
        print("Waypoints exist")
        # file exists used saved results
        waypoint_distances = {}
        waypoint_durations = {}
        all_waypoints = set()

        waypoint_data = pd.read_csv(file_path, sep="\t")

        for i, row in waypoint_data.iterrows():
            waypoint_distances[frozenset([row.waypoint1, row.waypoint2])] = row.distance_m
            waypoint_durations[frozenset([row.waypoint1, row.waypoint2])] = row.duration_s
            all_waypoints.update([row.waypoint1, row.waypoint2])

    else:
        # File does not exist - compute results       
        print("Collecting Waypoints")
        waypoint_distances = {}
        waypoint_durations = {}

        gmaps = googlemaps.Client(GOOGLE_MAPS_API_KEY)
        for (waypoint1, waypoint2) in combinations(all_waypoints, 2):
            try:
                route = gmaps.distance_matrix(origins=[waypoint1],
                                              destinations=[waypoint2],
                                              mode="driving",  # Change to "walking" for walking directions,
                                              # "bicycling" for biking directions, etc.
                                              language="English",
                                              units="metric")

                # "distance" is in meters
                distance = route["rows"][0]["elements"][0]["distance"]["value"]

                # "duration" is in seconds
                duration = route["rows"][0]["elements"][0]["duration"]["value"]

                waypoint_distances[frozenset([waypoint1, waypoint2])] = distance
                waypoint_durations[frozenset([waypoint1, waypoint2])] = duration

            except Exception as e:
                print("Error with finding the route between %s and %s." % (waypoint1, waypoint2))

        print("Saving Waypoints")
        with open(waypoints_file, "w") as out_file:
            out_file.write("\t".join(["waypoint1",
                                      "waypoint2",
                                      "distance_m",
                                      "duration_s"]))

            for (waypoint1, waypoint2) in waypoint_distances.keys():
                out_file.write("\n" +
                               "\t".join([waypoint1,
                                          waypoint2,
                                          str(waypoint_distances[frozenset([waypoint1, waypoint2])]),
                                          str(waypoint_durations[frozenset([waypoint1, waypoint2])])]))

    print("Search for optimal route")
    optimal_route = run_genetic_algorithm(generations=thisRunGenerations, population_size=thisRunPopulation_size)

    # This is probably redundant now that the files are created in run_genetic_algorithm,
    # but leaving it active to ensure  the final result is not lost
    CreateOptimalRouteHtmlFile(optimal_route, 1, True)