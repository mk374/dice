#Python3 supported
import requests
import pandas as pd
import csv
import heapq
import numpy as np
import os
import json
import sys

import restaurant_search as rs
sys.path.append('../')
from mongodb import main_db as db
from pymongo import MongoClient

#Use your own api key. Try this one if it works. Make ur own
#(For yelp)
MY_API_KEY = "7rf6Fpz0BsOaifSmpsgxwA1azkflcYnz2YbcI3RHXtTs2Ab0EvViRcVj8UFVanDEFkkDf0H2fBPl5PRsOwvJdx9wi2OqpnDiC1KkwDO_572clGZ-6L9R-yTaJVMlXXYx"
MY_GOOGLE_KEY = "NOT AVAILABLE"

#General standards
num_of_restaurant_matches = 20

#for now, just restaurants. defaults to businesses/restuarants
business_url = 'https://api.yelp.com/v3/businesses/search'
#this is the prefix of the url. we input the parameters at the end of the url
distance_matrix_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'



#the key into the YELP api
headers = {
        'Authorization': 'Bearer {}'.format(MY_API_KEY),
}
#the Key for the Google API
google_headers = {
            'Authorization': 'Bearer {}'.format(MY_GOOGLE_KEY),
}
#Lots of different parameters. We can change that accordingly
#location, radius are our two most important parameters
location = 'Durham, NC' #can switch to certian latitude/longitude

SEARCH_LIMIT = 10

#for the distance_matrix
walking_distance = 5 #some limit we should come up with
car_distance = 20 # some limit for cars (time) we should come up with
bic_distance = 13 # limit for bicycles

#get a list of breakfasts, lunches, and dinners

client = MongoClient("mongodb+srv://mk374:Soon1621mi@cluster0-yisih.azure.mongodb.net/test?retryWrites=true&w=majority")

def saveData():
    x,y,z = rs.getRestaurants(headers, business_url, location)
    #breakfasts
    # print('breakfasts')
    # for ev in x['businesses']:
    #     print(ev['name'] + 'location: {}'.format(ev['coordinates']))
    # #lunches
    # print('lunches')
    # for ev in y['businesses']:
    #     print(ev['name'] + 'location: {}'.format(ev['coordinates']))
    # #dinners
    # print('dinners')
    # for ev in z['businesses']:
    #     print(ev['name'] + 'location: {}'.format(ev['coordinates']))
    db = client.cities
    rs.saveRestaurantsToDatabase(x,y,z,db, location)
    return

def readData():
    
    return

saveData()