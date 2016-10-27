##########################################################################################
##########################################################################################
#   Created on: 20160507                                                                 #
#   Created by: Brian Hirsch                                                             #
#   Where: University of Missouri                                                        #
#   Actions: Main script for NUMBUSS                                                     #
#   Permissions/Distribution: Copyrighted Brian Hirsch 2016                              #
#   Class: GEOG 4940                                                                     #
#   Final Project                                                                        #
##########################################################################################
##########################################################################################

## To run NIMBUSS simply run this this script either in a shell or in a command line.
## The script will ask you how often you want it to make a map.
## Once NIMBUSS knows how often it run it will continue to run till the end of time.
## Unless the script is stopped by the user.

## NIMBUSS will put out a JPEG map of the surface stations in Missouri and an atmospheric
## boundary (if found). NIMBUSS also creates a Placefile of the stations data to be used
## in GRLevelX software.

## This script much be in a folder with other folders called JPGs, placefile, and templates, 
## as well as, a geodatabase called NIMBUSS. See the documentation for more information
## about these folders.

## In order for this scritp to run six other scripts need to be in the same folder. These
## scripts are FrontFinder, GrabData, MapMaker, PlacefileMaker, PolylineMaker,
## and StationShape.

##########################################################################################
#                               Initialization                                           #
##########################################################################################

##### Imports ##### 
import os, schedule, time
from GrabData import GrabData
from StationShape import makeShapefile
from FrontFinder import *
from PolylineMaker import PolylineMaker
from MapMaker import MapMaker
from PlacefileMaker import makePlaceFile

##### Set Global Variables #####

##### Get input from user for how often to run #####
print "Hello my name is Newly Interpolated Meso-scale Boundaries Using Surface Stations! But you can call me NIMBUSS. My purpose is to process meso-scale meteorlogical data, look for atmospheric boundaries, and map the station plots and boundaries. I will also create a placefile for use in GRLevelX every five minutes.\n"
print "I just have one thing to ask you before I get going."
Maptime = raw_input("How often (hours) would you like me to make a map?")
print "\nYour wish is my command, I'll map every " + Maptime + " hours.\n"
# Convert interval time to secdonds
Maptime = float(Maptime) * 3600

##########################################################################################
#                               Main Scheduled Workflow                                  #
##########################################################################################


## This function makes a placefile
def placefile():
        
        ## Get the time 
        lngruntime = time.strftime("%Y/%m/%d %H:%M", time.gmtime())
        print "Starting to create a placefile at " + lngruntime

        ## Grab the data
        stations,textStations = GrabData()
        #### This output isnt needed for this function (placefile)
        del stations

        ## Make a text placefile for GRLevelX
        makePlaceFile(textStations, lngruntime)
        
        ## Clean Up
        del textStations, lngruntime

## This function is the workflow for creating map of the data
def mapper():
        
        ## Get the time
        #### This time is used for file names
        srtruntime = time.strftime("%Y%m%d%H%M", time.gmtime())
        #### This time is used to display the time in the command line
        lngruntime = time.strftime("%Y/%m/%d %H:%M", time.gmtime())
        #### This time will be used in the outputted map
        titletime = time.strftime("%B %d, %Y %H:%M", time.gmtime())
        print "Starting to make a map at " + lngruntime

        ## Grab the data
        stations,textStations = GrabData()
        #### This output isnt needed for this function (mapper)
        del textStations

        ## Make a of the stations feature class in ArcGIS
        stationShp, stationName = makeShapefile(stations, srtruntime, lngruntime)

        ## Looking for a boundary; returns the boundary and if one was found
        frontpnt,frontfound = findFront(stations, srtruntime)

        ## If there is a boundry draw the boundary, then map the surface stations and boundary
        ## If there is no boundary, map the surface stations
        if frontfound == True:
                front = PolylineMaker(frontpnt)
                MapMaker(stationShp, front, srtruntime, titletime, stationName)
        if frontfound == False:
                front = None
                MapMaker(stationShp, front, srtruntime, titletime, stationName)
        print "Finished making the map\n"
        
        ## Clean Up
        del stations,srtruntime, lngruntime, titletime, stationShp, stationName, frontpnt, frontfound, front

## Set up the schedules
#### Schedule to make a placefile every five minutes
schedule.every(5).minutes.do(placefile)
#### Schuale to make the map at a user defined time interval
schedule.every(Maptime).seconds.do(mapper)

## Create initial placefile and map
placefile()
mapper()

## While script is running check every second if any functions are scheduled
## to run at the current time
while True:
    schedule.run_pending()
    time.sleep(1)
