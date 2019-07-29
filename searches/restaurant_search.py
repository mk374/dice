#Python3 supported
import requests
import pandas as pd
import csv
import heapq
import numpy as np
import os
import json

#Use your own api key. Try this one if it works. Make ur own
#(For yelp)
MY_API_KEY = "7rf6Fpz0BsOaifSmpsgxwA1azkflcYnz2YbcI3RHXtTs2Ab0EvViRcVj8UFVanDEFkkDf0H2fBPl5PRsOwvJdx9wi2OqpnDiC1KkwDO_572clGZ-6L9R-yTaJVMlXXYx"
MY_BING_KEY = "ArcDM9D1dZ9pntV9ayBgz2JgBwLQxNY8AcXxPeSNIUNMuO4y77jUK-712M45INFM"
MY_GOOGLE_KEY = "AIzaSyDSVFuDlz9JLb96aXDjwoF586t6N32oILk"

#General standards
num_of_restaurant_matches = 20

#for now, just restaurants. defaults to businesses/restuarants
business_url = 'https://api.yelp.com/v3/businesses/search'
#this is the prefix of the url. we input the parameters at the end of the url
distance_matrix_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

# # GOOGLE IS TOO EXPENSIVE. BING IS FREE
# distance_matrix_url = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key="
# distance_matrix_url += MY_BING_KEY


#the key into the api
headers = {
        'Authorization': 'Bearer {}'.format(MY_API_KEY),
    }
google_headers = {
            'Authorization': 'Bearer {}'.format(MY_GOOGLE_KEY),
}
#Lots of different parameters. We can change that accordingly
#location, radius are our two most important parameters
location = 'Durham, NC' #can switch to certian latitude/longitude
location2 = 'Charlotte NC'
SEARCH_LIMIT = 10

#for the distance_matrix
walking_distance = 5 #some limit we should come up with
car_distance = 20 # some limit we should come up with
bic_distance = 13 #also includes some scooters or skateboard (electric)


def getRestaurantDistanceMatrix(location, SEARCH_LIMIT=10):
    restaurant_params = {
            'location': location.replace(' ', '+'),
            'categories': 'restaurants',
            'limit': SEARCH_LIMIT
    }

    yelp_response = requests.get(business_url, headers=headers, params=restaurant_params)

    #there are three keys within the json file
    #['businesses', 'total', 'region']
    #focus on 'businesses'.
    #we can narrow it down according to distance from a certain search location
    #this search location can be specified by latitude, longitude (user's coordinates)

    # print(yelp_response)
    distance_params = {
        'origins': "",
        'destinations': "",
        'key' : MY_GOOGLE_KEY
    }
    names = []
    for ev in yelp_response.json()['businesses']:
        # print(ev['name'] + 'location: {}'.format(ev['coordinates']))
        names.append(ev['name'])
        distance_params['origins'] += '|{},{}'.format(ev['coordinates']['latitude'],ev['coordinates']['longitude']) 
        distance_params['destinations'] += '|{},{}'.format(ev['coordinates']['latitude'],ev['coordinates']['longitude']) 
    
    #this is exclusively for driving.
    google_response = requests.get(distance_matrix_url, headers=google_headers, params=distance_params)

    matrix =[]
    for ele in google_response.json()['rows']:
        row = []
        for dis in ele['elements']:
            row.append((dis['duration']['value'], dis['duration']['text']))
        matrix.append(row)

    return (names, distance_params['origins'],matrix)

def rankRestaurantsByDistance(names, matrix):
    ranked = []
    for row in range(len(matrix)):
        for col in range(row, len(names)):
            if row == col:
                continue
            else:
                #(value of distance, text distance, origin, destination)
                ranked.append((matrix[row][col][0], matrix[row][col][1], names[row], names[col]))
    ranked = sorted(ranked, key=lambda x: x[0])
    return ranked
    
    
def saveFile(location, ranked):
    os.chdir('..')
    download_file_name = "json/restuarantsJson.json"

    with open(download_file_name, 'w') as json_file:
        data = json.load(json_file)
        if location not in data:
            print('Creating new restaurants matrix in {}'.format(location))
            newRanked = {}
            newRanked[location] = []
            for i in range(num_of_restaurant_matches):
                newRanked.append(ranked[i])
        else:
            print("Updating the location")
        # json.dump(ranked, json_file)
    
# with open('data.json', 'r+') as f:
#     data = json.load(f)
#     data['id'] = 134 # <--- add `id` value.
#     f.seek(0)        # <--- should reset file position to the beginning.
#     json.dump(data, f, indent=4)
#     f.truncate()     # remove remaining part



names, coordinates, matrix = getRestaurantDistanceMatrix(location)
ranked = rankRestaurantsByDistance(names, matrix)
os.chdir('..')
with open('json/restaurantsJson.json', 'w') as json_file:
    try:
        data = json.load(json_file)
        if not data:
            print("hello")
    except:
        print('hello')
# saveFile (ranked)
