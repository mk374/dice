#Python3 supported
import requests
import pandas as pd

#Use your own api key. Try this one if it works. Make ur own
#(For yelp)
MY_API_KEY = "7rf6Fpz0BsOaifSmpsgxwA1azkflcYnz2YbcI3RHXtTs2Ab0EvViRcVj8UFVanDEFkkDf0H2fBPl5PRsOwvJdx9wi2OqpnDiC1KkwDO_572clGZ-6L9R-yTaJVMlXXYx"

#for now, just restaurants. defaults to businesses/restuarants
business_url = 'https://api.yelp.com/v3/businesses/search'
#this is the prefix of the url. we input the parameters at the end of the url
distance_matrix_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'


#the key into the api
headers = {
        'Authorization': 'Bearer {}'.format(MY_API_KEY),
    }

#Lots of different parameters. We can change that accordingly
#location, radius are our two most important parameters
location = 'Durham, NC' #can switch to certian latitude/longitude
SEARCH_LIMIT = 10

#for the distance_matrix
walking_distance = 5 #some limit we should come up with
car_distance = 20 # some limit we should come up with
bic_distance = 13 #also includes some scooters or skateboard (electric)


restaurant_params = {
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
}


yelp_response = requests.get(business_url, headers=headers, params=restaurant_params)



distance_params = {
        ''
}
matrix_response = requests.get()
#there are three keys within the json file
#['businesses', 'total', 'region']
#focus on 'businesses'.
#we can narrow it down according to distance from a certain search location
#this search location can be specified by latitude, longitude (user's coordinates)

for ev in yelp_response.json()['businesses']:
    print(ev['name'] + 'location: {}'.format(ev['coordinates']))



