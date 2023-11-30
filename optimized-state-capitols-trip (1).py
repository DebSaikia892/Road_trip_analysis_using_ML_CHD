#!/usr/bin/env python
# coding: utf-8

# In[1]:


all_waypoints = ["Sector 1, Chandigarh",
                 "Sector 2, Chandigarh",
                 "Sector 3, Chandigarh",
                 "Sector 4, Chandigarh",
                 "Sector 5, Chandigarh",
                 "Sector 6, Chandigarh",
                 "Sector 7, Chandigarh",
                 "Sector 8, Chandigarh",
                 "Sector 9, Chandigarh",
                 "Sector 10, Chandigarh",
                 "Sector 11, Chandigarh",
                 "Sector 12, Chandigarh",
                 "Sector 13, Chandigarh",
                 "Sector 14, Chandigarh",
                 "Sector 15, Chandigarh",
                 "Sector 16, Chandigarh",
                 "Sector 17, Chandigarh",
                 "Sector 18, Chandigarh",
                 "Sector 19, Chandigarh",
                 "Sector 20, Chandigarh",
                 "Sector 21, Chandigarh",
                 "Sector 22, Chandigarh",
                 "Sector 23, Chandigarh",
                 "Sector 24, Chandigarh",
                 "Sector 25, Chandigarh",
                 "Sector 26, Chandigarh",
                 "Sector 27, Chandigarh",
                 "Sector 28, Chandigarh",
                 "Sector 29, Chandigarh",
                 "Sector 30, Chandigarh",
                 "Sector 31, Chandigarh",
                 "Sector 32, Chandigarh",
                 "Sector 33, Chandigarh",
                 "Sector 34, Chandigarh",
                 "Sector 35, Chandigarh",
                 "Sector 36, Chandigarh",
                 "Sector 37, Chandigarh",
                 "Sector 38, Chandigarh",
                 "Sector 39, Chandigarh",
                 "Sector 40, Chandigarh",
                 "Sector 41, Chandigarh",
                 "Sector 42, Chandigarh",
                 "Sector 43, Chandigarh",
                 "Sector 44, Chandigarh",
                 "Sector 45, Chandigarh",
                 ]
len(all_waypoints)


# In[2]:


import googlemaps

gmaps = googlemaps.Client(key='AIzaSyCucpOtseSkHzyALg9A_8DnEzHT7ID0Y3c')


# In[3]:


from itertools import combinations

waypoint_distances = {}
waypoint_durations = {}

for (waypoint1, waypoint2) in combinations(all_waypoints, 2):
    try:
        route = gmaps.distance_matrix(origins=[waypoint1],
                                      destinations=[waypoint2],
                                      mode='driving', # Change this to 'walking' for walking directions,
                                                      # 'bicycling' for biking directions, etc.
                                      language='English',
                                      units='metric')

        # 'distance' is in meters
        distance = route['rows'][0]['elements'][0]['distance']['value']

        # 'duration' is in seconds
        duration = route['rows'][0]['elements'][0]['duration']['value']

        waypoint_distances[frozenset([waypoint1, waypoint2])] = distance
        waypoint_durations[frozenset([waypoint1, waypoint2])] = duration
    
    except Exception as e:
        print('Error with finding the route between {} and {}.'.format(waypoint1, waypoint2))


# In[4]:


with open('my-waypoints-dist-dur.tsv', 'w') as out_file:
    out_file.write('\t'.join(['waypoint1',
                              'waypoint2',
                              'distance_m',
                              'duration_s']))
    
    for (waypoint1, waypoint2) in waypoint_distances.keys():
        out_file.write('\n' +
                       '\t'.join([waypoint1,
                                  waypoint2,
                                  str(waypoint_distances[frozenset([waypoint1, waypoint2])]),
                                  str(waypoint_durations[frozenset([waypoint1, waypoint2])])]))


# In[5]:


import pandas as pd
import numpy as np

waypoint_distances = {}
waypoint_durations = {}
all_waypoints = set()

waypoint_data = pd.read_csv('my-waypoints-dist-dur.tsv', sep='\t')

for i, row in waypoint_data.iterrows():
    # Distance = meters
    waypoint_distances[frozenset([row.waypoint1, row.waypoint2])] = row.distance_m
    
    # Duration = hours
    waypoint_durations[frozenset([row.waypoint1, row.waypoint2])] = row.duration_s / (60. * 60.)
    all_waypoints.update([row.waypoint1, row.waypoint2])

