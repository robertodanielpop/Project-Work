from django.shortcuts import render
from django.http import HttpResponse
from parkatdcu.models import Carpark, Campus

from django.conf import settings


import os
import requests
import json

from .models import Campus, Carpark
import requests

from requests.auth import HTTPBasicAuth

# Create your views here.
def index(request):
    context = {}
    return render(request,"parkatdcu/index.html",context)

def carparks(request):

    campus_name = request.GET['campus']

    context = {}
    webservice_base_url = "http://jfoster.pythonanywhere.com/carparks/"

    #Carpark Code

    #Extracts the data from Campus json
    campus_names = Campus.objects.all()

    campus_ids = []

    #Iterates over the campus json data and add the name of each campus in a list if not present
    for ids in campus_names:
        if ids.name not in campus_ids:
            campus_ids.append(ids.name)

    #Allows the user input to be non-case sensitive
    for no_case in campus_ids:
        if campus_name.lower() == no_case.lower():
            campus_name = no_case

    #If the campus is present in the list, execute the following block otherwise go to the else.
    if campus_name in campus_ids:

        #Get the campus names
        campus = Campus.objects.get(name=campus_name)

        #Get the carpark data filtered by campus_id
        carparks = Carpark.objects.filter(campus_id=campus)


        carpark_info = []

        #Iterates over the carpark json
        for carpark in carparks:

            #Access the webservice and extract the data in json format
            webservice_url = webservice_base_url + carpark.name

            realtime_info = requests.get(webservice_url).json()

            #Checks if there are available spaces
            if 'spaces_available' in realtime_info:
                spaces_available = realtime_info['spaces_available']
            else:
                spaces_available = 'not available'

            #Add the data from the carpark and webservice to a list in a dictionary format
            carpark_info.append({
                                'name': carpark.name,
                                'spaces': carpark.spaces,
                                'disabled_spaces': carpark.disabled_spaces,
                                'spaces_available': spaces_available
                                }
                               )
        #If the list is empty, i.e. The campus exists in the api but there is no carpark data available
        if carpark_info == []:
            carpark_info = False

        context['campus'] = campus_name
        context['carparks'] = carpark_info
    
    #If the campus is not present in the list
    else:
        campus_name = "No such campus"
        context['campus'] = campus_name

    return render(request,"parkatdcu/carparks.html",context)

def bus(request):

    bus_stop_location = request.GET['bus']

    context = {}
   
   
    #Extra Functionality: Bus to and from DCU Campus

    #Accessing the GTFS-R api which contains bus journey real time information
    
    webservice_dublin_bus_url = " https://gtfsr.transportforireland.ie/v1/?format=json"

    #Access key embedded in the header
    headers = {
        'Cache-Control': 'no-cache',
        'x-api-key': 'b9162e578e1f4d159e737552a99d107c',
         }


    bus1={}
    response = requests.get(webservice_dublin_bus_url, headers=headers)
    
    bus1 = response.json()
                    
    #Bus data that contains all dcu stops
    dcu_bus = [{
        "id": 1,
        "db_bus": {'Name': 'DCU Ballymun Road, stop 37',
                   'Number': '8220DB000037'}},
    
       {"id" : 2, 
        "db_bus": {'Name': 'DCU Helix, stop 7571',
                   'Number': '8220DB007571'}},

       {"id": 3,
        "db_bus": {'Name':'DCU',
                   'Number': '8220B1350201'}},

       {"id": 4,
        "db_bus": {'Name': 'DCU, stop 4680',
                   'Number': '8220DB004680'}},

       {"id": 5,
        "db_bus": {'Name': 'St Pats, Clonturk Park, Drumcondra Road, stop 80283',
                   'Number': '8220DB000021'}},

       {"id": 6,
        "db_bus": {'Name': 'DCU St Patrick’s, stop 45',
                   'Number': '8220DB000045'}},

       {"id": 7,
        "db_bus": {'Name': 'DCU St Patrick’s, stop 7602',
                   'Number': '8220DB07602'}},

       {"id": 8,
        "db_bus": {'Name': 'DCU Collins Avenue, stop 81909',
                   'Number': '8220DB001644'}},
        
       {"id": 9,
        "db_bus": {'Name': 'DCU Collins Avenue, stop 81910',
                   'Number': '8220DB001646'}}
    ]

    
    Glasnevin = ['8220DB000037','8220DB007571', '8220B1350201', '8220DB004680', '8220DB001644', '8220DB001646']
    St_Pats = ['8220DB000021','8220DB000045', '8220DB07602']


    if bus_stop_location == "Glasnevin":
        bus_stop_location = Glasnevin
    elif bus_stop_location == "St. Pats":
        bus_stop_location = St_Pats
    else:
        bus_stop_location = "No Such Campus"
    
    context["Bus"] = bus_stop_location
    import sys

    #Trip Id and Routes

    #Txt file which contains the information about the trips
    trips = os.path.join(settings.BASE_DIR, "../../data/trips.txt")

    a = []

    #Opens trips.txt
    with open(trips) as f:
        trip = f.readlines()
        i = 0
        #Iterating over each line and putting it in a list and removing the "\n"
        while i < len(trip):
            location = trip[i].split("\n")
            a.append(location)
            i = i + 1


    o = 0

    location_id = []

    #Putting the data from the txt in a manageable list for extraction
    while o < len(a):
        locator = a[o][0].split(",")
        location_id.append({
        
        "Id": o,
        "Location_Route": {
            "Route_Id": locator[0][1:len(locator[0]) - 1],
            "Route_Number": locator[2][1:len(locator[2]) - 1],
            "Location_name": locator[4][1:len(locator[4]) - 1]
            }})
        o = o + 1


    #Bus Routes

    #Txt file which contains the information about the routes
    routes = os.path.join(settings.BASE_DIR, "../../data/routes.txt")

    route_id = []
    #Opens routes.txt
    with open(routes) as l:
        route = l.readlines()
        i = 0
        #Iterating over each line and putting it in a list and removing the "\n"
        while i < len(route):
            number_bus = route[i].split(",")
           #Putting the data from the txt in a manageable list for extraction
            route_id.append({
                "Id": i,
                "Bus_Route": {
                "Route_Id": number_bus[0][1:len(number_bus[0]) - 1],
                "Bus_Number": number_bus[2][1:len(number_bus[2]) - 1],
                "Location_Name": number_bus[3][1:len(number_bus[3]) - 1]
                }})
            i = i + 1

    i = 0

    route_data = []
    location_data = []
    bus_departures = []

    #Search throught the json data extracted from the api starting from the entity key
    for location in bus1['entity']:
        #Iterate through the bus stop data list to find all the stop available at the current time
        for dcu in dcu_bus:
            #If the bus is available put it in a list
            if dcu['db_bus']['Number'] in str(location) and location['id'] not in str(bus_departures):
                bus_departures.append(location)
                #Search through the data extracted from the trips.txt
                for data_location in location_id:
                    #If the route_number matches the location id //trip_id(trips.txt) == id(GTFS-r JSON)\\ and  the id is not already in the list put it in the list as a dictionary. Removes duplicates
                    if data_location['Location_Route']['Route_Number'] == location['id'] and location['id'] not in str(location_data):
                        location_data.append({ 
                            "Id": i,       
                            "Location_Route": {
                                "Route_Id": data_location['Location_Route']['Route_Id'],
                                "Route_Number": data_location['Location_Route']['Route_Number'],
                                "Location_name": data_location['Location_Route']['Location_name']

                            }})
                        i = i + 1

    i = 0

    #Search through the data extracted from routes.txt
    for data_route in route_id:
        #Iterates over the new data extracted from location_id
        for data_location_tailored in location_data:
            #If the two routes match // route_Id(route.txt) == route_Id(location_data) \\ and the Route_Id is not already in the list, add it to the list as a dictionary
            if data_route['Bus_Route']['Route_Id'] == data_location_tailored['Location_Route']['Route_Id'] and data_route['Bus_Route']['Route_Id'] not in str(route_data):
                route_data.append({                
                "Id": i,
                "Bus_Route": {
                    "Route_Id": data_route['Bus_Route']['Route_Id'],
                    "Bus_Number": data_route['Bus_Route']['Bus_Number'],                    
                    }})
                i = i + 1

    roster = []
    i = 0

    #Txt file which contains the information about the stop schedules
    stop_times = os.path.join(settings.BASE_DIR, '../../data/stop_times_dcu_only.txt')

    #Search through the data extracted from stop_times_dcu_only.txt
    with open(stop_times) as stop:
        schedule = stop.readlines()
        #Iterate over the data extracted from stop_times_dcu_only.txt and separate it by the ","
        for each in schedule:
            part = each.split(",")
            #if the trip_id is in location_data dictionary and the stop_id is in dcu_bus and the trip_id is not already in the roster dictionary // avoid duplicate trips
            if part[0][1:len(part[0]) - 1] in str(location_data) and part[3][1:len(part[3]) - 1] in str(dcu_bus) and int(part[4][1:len(part[4]) - 1]) != 1:
                roster.append({
                    "Id": i,
                    "Schedule": {
                        "Route_Number": part[0][1:len(part[0]) - 1],
                        "Route_Id": part[3][1:len(part[3]) - 1],
                        "Arrival": part[1][1:len(part[1]) - 1],
                        "Departure": part[2][1:len(part[2]) - 1],
                        "Sequence": part[4][1:len(part[4]) - 1]
                    }
            
                })
                i = i + 1
    
    no_delay = []
    for compatible in roster:
        for match in bus_departures:
            if compatible['Schedule']['Route_Number'] in str(match) and compatible['Schedule']['Route_Id'] not in str(match):
                no_delay.append(compatible['Schedule']['Route_Number'])
    #context["Roster"] = roster

    #Adds all the data to context to be used in carparks.html
    context["Data_Bus"] = bus_departures
    context["Route"] = route_id
    #context["Route_String"] = str(route) #Debugging purposes
    context["Location"] = location_data
    context["DCU"] = dcu_bus
    context["Roster"] = roster
    #context['Buus'] = bus1 #Debugging Purposes
    context['No_Delay'] = no_delay

    return render(request,"bus/bus.html",context)

def campus(request):
    context = {}
    return render(request,"bus/campus.html",context)