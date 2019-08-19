#Python3 supported
import requests
import pandas as pd
import csv
import heapq
import numpy as np
import os
import json
import sys

sys.path.append('../')
# from mongodb import main_db as db

def getRestaurants(headers, business_url, location, SEARCH_LIMIT=10):
    breakfast_params = {
            'location': location.replace(' ', '+'),
            'categories': 'breakfast',
            'limit': SEARCH_LIMIT
    }
    lunch_params = {
            'location': location.replace(' ', '+'),
            'categories': 'lunch',
            'limit': SEARCH_LIMIT
    }
    dinner_params = {
            'location': location.replace(' ', '+'),
            'categories': 'dinner',
            'limit': SEARCH_LIMIT
    }


    breakfast_response = requests.get(business_url, \
        headers=headers, params=breakfast_params)
    lunch_response = requests.get(business_url, \
        headers=headers, params=breakfast_params)
    dinner_response = requests.get(business_url, \
        headers=headers, params=breakfast_params)

    return breakfast_response.json(), lunch_response.json(), \
        dinner_response.json()

def saveRestaurantsToDatabase(breaks,lunches,dinners, db, city):#city represent
    #the database within cities database

    for breakfastPlace in breaks['businesses']:
        breakie = {
            'city': city,
            'type': 'restaurant',
            'info':{
                'restaurantType': 'breakfast',
                'name': breakfastPlace['name'],
                'coordinates': (breakfastPlace['coordinates']['latitude'],\
                    breakfastPlace['coordinates']['longitude']),
                'rating': breakfastPlace['rating'],
                'price': breakfastPlace['price']    
            }
        }
        db[city].insert_one(breakie)

    for lunchPlace in lunches['businesses']:
        lunch = {
            'city': city,
            'type': 'restaurant',
            'info':{
                'restaurantType': 'lunch',
                'name': lunchPlace['name'],
                'coordinates': (lunchPlace['coordinates']['latitude'],\
                    lunchPlace['coordinates']['longitude']),
                'rating': lunchPlace['rating'],
                'price': lunchPlace['price']    
            }
        }
        db[city].insert_one(lunch)

    for dinnerPlace in dinners['businesses']:
        dinner = {
            'city': city,
            'type': 'restaurant',
            'info':{
                'restaurantType': 'dinner',
                'name': dinnerPlace['name'],
                'coordinates': (dinnerPlace['coordinates']['latitude'],\
                    dinnerPlace['coordinates']['longitude']),
                'rating': dinnerPlace['rating'],
                'price': dinnerPlace['price']    
            }
        }
        
        db[city].insert_one(dinner)
    
        



# def getRestaurantDistanceMatrix(location, SEARCH_LIMIT=10):
#     restaurant_params = {
#             'location': location.replace(' ', '+'),
#             'categories': 'restaurants',
#             'limit': SEARCH_LIMIT
#     }

#     yelp_response = requests.get(business_url, \
#         headers=headers, params=restaurant_params)

#     #there are three keys within the json file
#     #['businesses', 'total', 'region']
#     #focus on 'businesses'.
#     #we can narrow it down according to distance from a certain search location
#     #this search location can be specified by latitude, longitude (user's coordinates)

#     # print(yelp_response)
#     distance_params = {
#         'origins': "",
#         'destinations': "",
#         'key' : MY_GOOGLE_KEY
#     }
#     names = []
#     for ev in yelp_response.json()['businesses']:
#         # print(ev['name'] + 'location: {}'.format(ev['coordinates']))
#         names.append(ev['name'])
#         distance_params['origins'] += '|{},{}'.\
#             format(ev['coordinates']['latitude'],\
#                 ev['coordinates']['longitude']) 
#         distance_params['destinations'] += '|{},{}'.\
#             format(ev['coordinates']['latitude'],\
#                 ev['coordinates']['longitude']) 
    
#     #this is exclusively for driving.
#     google_response = requests.get(distance_matrix_url, \
#         headers=google_headers, params=distance_params)

#     matrix =[]
#     for ele in google_response.json()['rows']:
#         row = []
#         for dis in ele['elements']:
#             row.append((dis['duration']['value'], \
#                 dis['duration']['text']))
#         matrix.append(row)

#     return (names, distance_params['origins'],matrix)

# def rankRestaurantsByDistance(names, matrix):
#     ranked = []
#     for row in range(len(matrix)):
#         for col in range(row, len(names)):
#             if row == col:
#                 continue
#             else:
#                 #(value of distance, text distance, origin, destination)
#                 ranked.append((matrix[row][col][0], \
#                     matrix[row][col][1], names[row], names[col]))
#     ranked = sorted(ranked, key=lambda x: x[0])
#     return ranked
    
    
# with open('data.json', 'r+') as f:
#     data = json.load(f)
#     data['id'] = 134 # <--- add `id` value.
#     f.seek(0)        # <--- should reset file position to the beginning.
#     json.dump(data, f, indent=4)
#     f.truncate()     # remove remaining part



# names, coordinates, matrix = getRestaurantDistanceMatrix(location)
# ranked = rankRestaurantsByDistance(names, matrix)
# os.chdir('..')
# with open('json/restaurantsJson.json', 'w') as json_file:
#     try:
#         data = json.load(json_file)
#         if not data:
#             print("hello")
#     except:
#         print('hello')
# saveFile (ranked)

# names, coordinates, matrix = getRestaurantDistanceMatrix(location)
# ranked = rankRestaurantsByDistance(names, matrix)
# print(ranked)
