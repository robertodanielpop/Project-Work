# Getting Started

## Overview

ParkAtDCU is an app that is used to search for carparks for each DCU campus.
The app returns information about the capacity of each carpark and the spaces currently available in that carpark.
Additionally the app also has BusStopAtDCU which is a feature that allows users to find the buses arriving at a specific campus.
It shows real time official departures from the campus and arrivals to the campus bus stops.

## Instructions for running the CA377 ParkAtDCU Django App with Docker Containers


## Setting up Repository

1. git clone https://gitlab.computing.dcu.ie/popr2/2021-ca377-popr2-parkatdcu.git
2. cd into 2021-ca377-popr2-parkatdcu/src/ca377
3. python3 manage.py makemigrations parkatdcu
4. python3 manage.py migrate
5. python3 manage.py loaddata ../../data/campus.json
6. python3 manage.py loaddata ../../data/carpark.json
7. cd into ca377, i.e. 2021-ca377-popr2-parkatdcu/src/ca377/ca377
8. Open settings.py and change the 'popr2/' in FORCE_SCRIPT_NAME = 'popr2/' with 'YOUR USERNAME'

## Running the Server:
* cd into 2021-ca377-popr2-parkatdcu/src/ca377
* python3 manage.py runserver 0.0.0.0:8080
* Access containers/computing.dcu.ie/YOUR USERNAME/parkatdcu/


## Running Tests

### Open settings.py
* cd into 2021-ca377-popr2-parkatdcu/src/ca377/ca377
* Make the following changes in settings.py:
    1. Comment out USE_X_FORAWARD_HOST = True
    2. Comment out FORCE_SCRIPT_NAME = 'YOUR USERNAME'
    3. Remove FORCE_SCRIPT_NAME from STATIC_URL

### Open urls.py
* cd into 2021-ca377-popr2-parkatdcu//src/ca377/ca377
* Comment out the following in urls.py: + static(settings.STATIC_SUFFIX, document_root=setting.STATIC_ROOT)


### Running the test
* cd into 2021-ca377-popr2-parkatdcu/src/ca377/
* python3 manage.py test

#### Disclaimer: before running the server make sure to undo the changes made in the settings.py and urls.py, otherwise the page won't load as intended.

