# -*- coding: utf-8 -*-
"""American Airlines Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nBgnwQHhsgcCcDiJs9bj35JJdHnRmBAs
"""

import datetime
import requests

dummy=[{'flightNumber': '1619', 
   'origin': {'code': 'DEL', 'city': 'Delhi', 'timezone': 'America/Chicago'}, 
   'destination': {'code': 'JFK', 'city': 'San Fransisco', 'timezone': 'America/New_York'}, 
   'departureTime': '2020-10-01T03:41:40.000-05:00', 
   'arrivalTime': '2020-10-01T2:35:40.000-04:00'},

   {'flightNumber': '1620', 
   'origin': {'code': 'JFK', 'city': 'San Fransisco', 'timezone': 'America/Chicago'}, 
   'destination': {'code': 'DFW', 'city': 'Dallas', 'timezone': 'America/New_York'}, 
   'departureTime': '2020-10-02T01:41:40.000-05:00', 
   'arrivalTime': '2020-10-02T05:35:40.000-04:00'},

   {'flightNumber': '1621', 
   'origin': {'code': 'DFW', 'city': 'Dallas', 'timezone': 'America/Chicago'}, 
   'destination': {'code': 'VEG', 'city': 'Los Vegas', 'timezone': 'America/New_York'}, 
   'departureTime': '2020-10-02T07:41:40.000-05:00', 
   'arrivalTime': '2020-10-02T10:35:40.000-04:00'}
]

dummy2 = []
for flight in dummy:
  fields = ['flightNumber', 'origin', 'destination', 'departureTime', 'arrivalTime']
  temp = {k:v for k,v in flight.items() if k in fields}
  temp['departureTime'] = datetime.datetime.strptime(temp['departureTime'][:-10], '%Y-%m-%dT%H:%M:%S')
  temp['arrivalTime'] = datetime.datetime.strptime(temp['arrivalTime'][:-10], '%Y-%m-%dT%H:%M:%S')
  dummy2.append(temp)


for i in range(len(dummy2)-1):

  if dummy2[i]['arrivalTime'] - dummy2[i + 1]['departureTime'] <= datetime.timedelta(3600):
      print(dummy2[i]['arrivalTime'].strftime("%Y-%m-%d"))
      url = "https://flightdetails1.herokuapp.com/flights?date="+ dummy2[i]['arrivalTime'].strftime("%Y-%m-%d") + "&origin=" + dummy2[i]['destination']['code']
      resp = requests.get(url = url)
      temp_flights = resp.json() 
      new_flights = []
      fields = ['flightNumber', 'origin', 'destination', 'departureTime', 'arrivalTime']
      for flight in temp_flights:
        if flight['destination']['code'] == dummy2[i + 1]['destination']['code']:
          # print(flight)
          temp2 = {k:v for k,v in flight.items() if k in fields}
          # print(temp2)
          temp2['origin'].pop('location')
          temp2['destination'].pop('location')
          temp2['departureTime'] = datetime.datetime.strptime(temp2['departureTime'][:-10], '%Y-%m-%dT%H:%M:%S')
          temp2['arrivalTime'] = datetime.datetime.strptime(temp2['arrivalTime'][:-10], '%Y-%m-%dT%H:%M:%S')
          # print(temp2.keys())
          new_flights.append(temp2)
      print(new_flights)

      # dummy3 = dummy2.copy()
      if new_flights:
        dummy2[i + 1] = new_flights[0]
        