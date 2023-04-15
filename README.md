# Just trying out this markdown stuff

## Intro
BundesratsJet

This is a Python project that tracks the flight status of the jets used by the Swiss Federal Council (as well as other politicians) using their Mode S hex code (ICAO) and the ADS-B Exchange API. The project includes a simple database for storing the flight data and a class for tracking multiple airplanes and detecting their flight status (ground, take-off, in-air, or landing).

The project includes a simple example script that tracks the flight status of two airplanes and broadcasts events to a Twitter account via the Twitter API.

**This is still very early stage**

## Latest changes:

### v0 **April 09, 2023**
* Obligatory "Hello World"
* Setup of structure and dependencies

### v1 **April 09, 2023**
* Implementation of first API calls: Get current data
* Data saved in SQLight

### v1.2 **April 09, 2023**
* First attempt of filtering data and classify different states (only half worked)

### v1.3 **April 10, 2023**
* First implementation of Twitter API

### v1.4 **April 15, 2023**
* Bug fix, changed DB query for "last entry" (had to offset by 1)
* Get AirportInfo based on coordinates
---
 
## ToDos (to be expanded)

* ~~Get the classification done properly~~
* ~~Combine with past work on Twitter API to notify when event occurs~~

* Include a map?

* Somehow control how many requests I have left this month?
* Move to online DB?

* Get script running online somewhere?