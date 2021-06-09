import requests
import time
import json
import random
from datetime import datetime, timedelta
from playsound import playsound

# Please change requirements below
age = 18 # Age of the person - 18/45
dose = 1 #Value should be 1 or 2. [Dose 1/ Dose 2] 
districtcodes = ['603','581','596','604'] # Codes/s to search vaccine availability - https://bit.ly/districtcodes
num_days = 4 # Number of days in the future to search for
vaccineType = "" #It should be COVISHIELD or COVAXIN or leave blank

today = datetime.today()
further_days = [today + timedelta(days=i) for i in range(num_days)]
dates = [i.strftime("%d-%m-%Y") for i in further_days]
randomnumber = random.randint(1,999999)

while True:
    cnt = 0
    for code in districtcodes:
        for date in dates:
            url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}&_{}".format(
                code, date,randomnumber)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
                }
            result = requests.get(url, headers = headers)
            if result.ok:
              response_json = result.json()
              flag = False
              if response_json['centers']:
                for center in response_json['centers']:
                  for session in center['sessions']:
                    if session['min_age_limit'] ==age and session['available_capacity_dose'+str(dose)] > 0  and session['available_capacity']>0 and (vaccineType == "" or session['vaccine'] == vaccineType):
                      print("\nPincode: " + str(center['pincode']))
                      print('\nAvailability date: ' + date)
                      print("\nAddress: "+center['address'])
                      print("\nCenter: "+center['name'])
                      print("\nBlock Name: "+center['block_name'])
                      print("\nPrice: "+center['fee_type'])
                      print("\nAvailable capacity (Dose 1): "+str(session['available_capacity_dose1']))
                      print("\nAvailable capacity (Dose 2): "+str(session['available_capacity_dose2']))
                      print("\nVaccine Type: "+session['vaccine'])
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
