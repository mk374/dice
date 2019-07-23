#Python3 supported
import requests
import pandas as pd
import csv

#Use your own api key. Try this one if it works. Make ur own
#(For yelp)
MY_API_KEY = "7rf6Fpz0BsOaifSmpsgxwA1azkflcYnz2YbcI3RHXtTs2Ab0EvViRcVj8UFVanDEFkkDf0H2fBPl5PRsOwvJdx9wi2OqpnDiC1KkwDO_572clGZ-6L9R-yTaJVMlXXYx"
MY_BING_KEY = "ArcDM9D1dZ9pntV9ayBgz2JgBwLQxNY8AcXxPeSNIUNMuO4y77jUK-712M45INFM"
MY_GOOGLE_KEY = "AIzaSyDSVFuDlz9JLb96aXDjwoF586t6N32oILk"

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
            row.append(dis['duration']['text'])
        matrix.append(row)

    
    
    return (names, distance_params['origins'],matrix)
names, origins, matrix = getRestaurantDistanceMatrix(location)

download_dir = "example.csv"
csv = open(download_dir, "w")


