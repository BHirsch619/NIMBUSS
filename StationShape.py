##########################################################################################
##########################################################################################
#   Created on: 20160415                                                                 #
#   Created by: Brian Hirsch                                                             #
#   Where: University of Missouri                                                        #
#   Actions: Makes Station shapefile realtime missouri mesonet data                      #
#   Permissions/Distribution: Copyrighted Brian Hirsch 2016                              #
#   Class: GEOG 4940                                                                     #
#   Final Project                                                                        #
##########################################################################################
##########################################################################################

##########################################################################################
#                               Initialization                                           #
##########################################################################################

##### Imports ##### 
import arcpy, os
from collections import OrderedDict
from arcpy import env
import arcpy_metadata as md

##########################################################################################
#                               Conversions                                              #
##########################################################################################

## Get station ID's
def StationID(station):
    if station == "Albany":
        ID = "ALB"
    if station == "Brunswick":
        ID = "BWK"
    if station == "Butler":
        ID = "BUT"
    if station == "Clarkton":
        ID = "CLK"
    if station == "Bradford Farm":
        ID = "BRD"
    if station == "Capen Park":
        ID = "CAP"
    if station == "Jefferson Farm":
        ID = "JEF"
    if station == "Sanborn Field":
        ID = "SAN"
    if station == "Cook Station":
        ID = "WUR"
    if station == "Green Ridge":
        ID = "GRG"
    if station == "Hayward":
        ID = "LEE"
    if station == "Lamar":
        ID = "LAM"
    if station == "Linneus":
        ID = "LIN"
    if station == "Monroe City":
        ID = "MOR"
    if station == "Moscow Mills":
        ID = "MOM"
    if station == "Mountain Grove":
        ID = "MTG"
    if station == "Mount Vernon":
        ID = "MTV"
    if station == "Portageville":
        ID = "PLB"
    if station == "St. Joseph":
        ID = "STJ"
    if station == "Vandalia":
        ID = "VAN"
    if station == "Versailles":
        ID = "VER"
    if station == "Unionville":
        ID = "UNV"
    if station == "Williamsburg":
        ID = "WIL"
    if station == "Novelty":
        ID = "NOV"
    return ID

## Simplify Dew point for Metar plot
def MetarDew(lngdew):
    dew = str(round(float(lngdew)))
    dew = dew.split(".")[0]
    return dew

## Simplify Temperature for Metar plot
def MetarTemp(lngTemp):
    temp = str(round(float(lngTemp)))
    temp = temp.split(".")[0]
    return temp

## Simplify Pressure for Metar plot
def MetarPress(lngPress):
    press = str(lngPress)
    press = press.replace(".","")[1:]   
    return press
    
##########################################################################################
#                               Write MetaData to Feature class                          #
##########################################################################################

##### This function writes metadata to a Feature class ##### 
def writeMetadata(ShapeFile, lngruntime):
    print "Writing metadata to shapefile"
    metadata = md.MetadataEditor(ShapeFile)
    metadata.title.set("Missouri Mesonet Stations")
    abstractMessage = "Missouri mesonet station data obtained from the Missouri Climate Center at %s. This data includes temperature, dew point, wind speed, wind direction, and pressure." % (lngruntime)
    metadata.abstract.set(abstractMessage)
    metadata.tags.add(["Missouri", "Climate", "Center", "Mesonet", "temperature", "dew", "point", "wind", "speed", "direction", "pressure"])
    metadata.finish()

##########################################################################################
#                               Let's make a Feature class                               #
##########################################################################################

##### This function creates a shapefile from the mesonet data ##### 
def makeShapefile(stations, runtime, lngruntime):

    ##### Station format w/ pressure [0StationNames, 1lat, 2lon, 3Temperature, 4DewPoint, 5WindSpeed, 6WindDirection, 7Pressure]
    ##### Station format w/o pressure [0StationNames, 1lat, 2lon, 3Temperature, 4DewPoint, 5WindSpeed, 6WindDirection]

    ##### Locations ##### 
    rootfolder = os.getcwd()
    env.workspace = os.path.join(rootfolder, "NIMBUSS.gdb")
    if __name__ == "__main__":
        outputFCName = "MOstationsTest1"
    else:
        outputFCName = "MOstations" + str(runtime)
    outputFC = os.path.join(env.workspace, outputFCName)

    ##### Environmental Variables ##### 
    env.overwriteOutput = True
    env.outputCoordinateSystem = arcpy.SpatialReference(4326)

    ##### Create the point shapefile #####
    print "\nMaking the station plot layer"
    arcpy.CreateFeatureclass_management(env.workspace, outputFCName, "POINT")

    ##### Create fields ##### 
    fields = OrderedDict()
    fields["StationNames"] = "Text"
    fields["Temperature"] = "Text"
    fields["DewPoint"] = "Text"
    fields["WindSpeed"] = "Float"
    fields["WindDirection"] = "Float"
    fields["Pressure"] = "Float"
    fields["MetarTemp"] = "Text"
    fields["MetarDew"] = "Text"
    fields["MetarPress"] = "Text"
    fields["StationID"] = "Text"

    ##### Add fields to the shapefile #####
    for fieldName, fieldType in fields.iteritems():
        arcpy.AddField_management(outputFC, fieldName, fieldType)


    ##### Start cursor to go through the rows of the shapefile attributes ##### 
    cursor = arcpy.da.InsertCursor(outputFC, ["SHAPE@", "StationNames", "Temperature", "DewPoint",
                                              "WindSpeed", "WindDirection", "Pressure", "MetarTemp",
                                              "MetarDew", "MetarPress", "StationID"])
    
    ##### Determine if there is pressure then add a row of data to the shapefile ##### 
    count = 0
    for station in stations:
        count += 1
        if len(station) == 8: 
            StationNames = station[0]
            lat = station[1]
            lon = station[2]
            Temperature = station[3]
            DewPoint = station[4]
            WindSpeed = station[5]
            WindDirection = station[6]
            Pressure = station[7]
            ## Convert temp, dew, and pressure to metar format
            mTemp = MetarTemp(Temperature)
            mDew = MetarDew(DewPoint)
            mPress = MetarPress(Pressure)
            ## Get station ID
            ID = StationID(StationNames)
            newPoint = arcpy.Point(lon, lat)
            newRow = [newPoint, StationNames, Temperature, DewPoint, WindSpeed, WindDirection,
                      Pressure, mTemp, mDew, mPress, ID]
            ## Insert new row to attribute table
            cursor.insertRow(newRow)
        if len(station) == 7:
            StationNames = station[0]
            lat = station[1]
            lon = station[2]
            Temperature = station[3]
            DewPoint = station[4]
            WindSpeed = station[5]
            WindDirection = station[6]
            # Return nothing for pressure if there is none
            Pressure = None
            ## Convert temp and dew to metar format
            mTemp = MetarTemp(Temperature)
            mDew = MetarDew(DewPoint)
            mPress = None
            ID = StationID(StationNames)
            newPoint = arcpy.Point(lon, lat)
            newRow = [newPoint, StationNames, Temperature, DewPoint, WindSpeed, WindDirection,
                      Pressure, mTemp, mDew, mPress, ID]
            ## Insert new row to attribute table
            cursor.insertRow(newRow)
    print "Maked station plot with %s of %s stations" %(count, len(stations))
    del count, station, cursor, StationNames, lat, lon, Temperature, DewPoint, WindSpeed, WindDirection, Pressure, newPoint,newRow, fields, rootfolder, env.workspace

    ## Write metadata
    writeMetadata(outputFC, lngruntime)

    ## return path location and feature class name
    return outputFC, outputFCName


# Test the functions
if __name__ == "__main__":
    import time
    stations = [['Albany', 40.241061, -94.343492, 74.9, 51.3, u'13.6', 157.5, u'29.91'],
                ['Brunswick', 39.412667, -93.1965, 77.7, 50.3, u'7.9', 157.5, u'29.94'],
                ['Butler', 38.25191, -94.343547, 77.3, 46.5, u'10.8', 180, u'29.91'],
                ['Clarkton', 36.490581, -89.961744, 76.1, 47.4, u'4.1', 90, u'30.07'],
                ['Bradford Farm', 38.897236, -92.21807, 75.0, 48.1, u'10.4', 135, u'29.97'],
                ['Capen Park', 38.929237, -92.321297, 78.3, 50.1, u'2.4', 202.5],
                ['Jefferson Farm', 38.906992, -92.269976, 75.4, 47.6, u'9.7', 157.5],
                ['Sanborn Field', 38.942301, -92.320395, 77.0, 46.2, u'3.3', 135, u'29.99'],
                ['Cook Station', 37.797945, -91.429645, 78.6, 46.7, u'4.4', 337.5, u'29.99'],
                ['Green Ridge', 38.621147, -93.416652, 78.2, 46.3, u'10.2', 180, u'29.94'],
                ['Hayward', 36.395972, -89.614473, 73.2, 48.3, u'7.9', 90, u'30.03'],
                ['Lamar', 37.493366, -94.318185, 77.0, 51.7, u'7.4', 180, u'29.95'],
                ['Linneus', 39.856919, -93.149726, 73.8, 51.6, u'14.5', 157.5],
                ['Monroe City', 39.635314, -91.72537, 72.7, 47.9, u'9.4', 157.5, u'30.03'],
                ['Moscow Mills', 38.938757, -90.931742, 71.3, 46.3, u'6.1', 112.5, u'30.03'],
                ['Mountain Grove', 37.153865, -92.268831, 75.1, 48.2, u'5.6', 135, u'30.05'],
                ['Mount Vernon', 37.077, -93.879, 78.4, 48.1, u'5.3', 202.5, u'29.97'],
                ['Novelty', 40.018917, -92.190781, 71.0, 51.2, u'12.5', 157.5, u'29.97'],
                ['Portageville', 36.413728, -89.69996, 75.2, 49.4, u'4.6', 90],
                ['St. Joseph', 39.757821, -94.794567, 75.9, 48.0, u'10.9', 157.5],
                ['Vandalia', 39.3023, -91.513, 72.0, 51.8, u'6.8', 112.5, u'30.05'],
                ['Versailles', 38.4347, -92.853733, 78.0, 48.1, u'5.5', 157.5, u'29.94'],
                ['Unionville', 40.466591, -93.002819, 71.2, 51.6, u'12.5', 180, u'29.91'],
                ['Williamsburg', 38.90735, -91.734217, 75.0, 47.5, u'8.7', 135, u'30.00']]
    lngruntime = time.strftime("%Y/%m/%d %H:%M", time.gmtime())
    srtruntime = time.strftime("%Y%m%d%H%M", time.gmtime())
    makeShapefile(stations, srtruntime, lngruntime)
    #for station in stations:
        #if len(station) == 8:
            #lngdew = station[7]
            #MetarPress(lngdew)
