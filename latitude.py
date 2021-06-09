import requests
import time
import json
import random
import geocoder
from datetime import datetime, timedelta
from playsound import playsound

# Please change requirements below
age = 18 # Age of the person - 18/45
dose = 1 #Value should be 1 or 2. [Dose 1/ Dose 2] 
num_days = 4 # Number of days in the future to search for
vaccineType = "" #It should be COVISHIELD or COVAXIN or leave blank

today = datetime.today()
further_days = [today + timedelta(days=i) for i in range(num_days)]
dates = [i.strftime("%d-%m-%Y") for i in further_days]
randomnumber = random.randint(1,999999)
g = geocoder.ip('me')
lat = g.latlng[0]
lang = g.latlng[1]

while True:
    cnt = 0
    url = "https://cdn-api.co-vin.in/api/v2/appointment/centers/public/findByLatLong?lat={}&long={}&_={}".format(
        lat,lang, randomnumber)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
        }
    result = requests.get(url, headers = headers)
    if result.ok:
      response_json = result.json()
      flag = False
      if response_json['centers']:
        for center in response_json['centers']:
              for date in dates:
                url1 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByCenter?center_id={}&date={}&_{}".format(
        center['center_id'],date, randomnumber)
                resultsVal = requests.get(url1, headers = headers)
                if resultsVal.ok:
                    responseVal_json = resultsVal.json()
                    if responseVal_json and responseVal_json['centers'] and responseVal_json['centers']['sessions']:
                        for sessionVal in responseVal_json['centers']['sessions']:
                            if sessionVal['min_age_limit'] ==age and sessionVal['available_capacity_dose'+str(dose)] > 0  and sessionVal['available_capacity']>0 and (vaccineType == "" or sessionVal['vaccine'] == vaccineType):
                              print("\nPincode: " + str(responseVal_json['centers']['pincode']))
                              print('\nAvailability date: ' + date)
                              print("\nAddress: "+responseVal_json['centers']['address'])
                              print("\nCenter: "+responseVal_json['centers']['name'])
                              print("\nBlock Name: "+responseVal_json['centers']['block_name'])
                              print("\nPrice: "+responseVal_json['centers']['fee_type'])
                              print("\nAvailable capacity (Dose 1): "+str(sessionVal['available_capacity_dose1']))
                              print("\nAvailable capacity (Dose 2): "+str(sessionVal['available_capacity_dose2']))
                              print("\nVaccine Type: "+sessionVal['vaccine'])
                              cnt+=1
    else:
      print("\nIssue with API. No response.")
    if cnt==0:
      print("\nNo vaccine slots available.")
    else:
      print("\nFound vaccine! Please find the details above!")
      print("\nLogin to https://www.cowin.gov.in/home -> Sign in -> Book the vaccine appointment using the details.")
      playsound("notification_sound.mp3")

    print("\n==================================\n")

    delay = datetime.now()+timedelta(minutes=2)
    while datetime.now() < delay:
      time.sleep(5)
