##########################################################################################
##########################################################################################
#   Created on: 20160415                                                                 #
#   Created by: Brian Hirsch                                                             #
#   Where: University of Missouri                                                        #
#   Actions: Grabs realtime missouri mesonet data                                        #
#   Permissions/Distribution: Copyrighted Brian Hirsch 2016                              #
#   Class: GEOG 4940                                                                     #
#   Final Project                                                                        #
##########################################################################################
##########################################################################################

##########################################################################################
#                               Initialization                                           #
##########################################################################################
import os, time
##########################################################################################
#                               Let's make a Text Placefile                              #
##########################################################################################

##### This function creates a placefile from the mesonet data ##### 
def makePlaceFile(stations,time):
    # Set locations
    rootfolder = os.getcwd()
    txtFileName = "MOstations.txt"
    txtFilespec = os.path.join(rootfolder, "placefile\\", txtFileName)
    # delete existing placefile
    if os.path.isfile(txtFilespec) == True:
        os.remove(txtFilespec)    

    time = "Last Updated: " + str(time)
    ##### Placefile header
    file = open(txtFilespec, "w")
    file.write('; Placefile created and copyrighted by Brian Hirsch\n')
    file.write('; Data is obtained from the Missouri Climate Center\n')
    file.write(';\n')
    file.write('Title: Missouri Mesonet Stations\n')
    file.write('RefreshSeconds: 150\n')
    file.write('Font: 1, 20, 1, "Arial"\n')
    file.write('Font: 2, 12, 1, "Arial"\n')
    file.write('Threshold: 999\n')
    file.write('Color: 247 79 99\n')

    ##### Placefile body text
    ##### Only display temp outside of hover text
    
    ## For each station in the stations list
    for station in stations:
        ## If there is pressure data
        if len(station) == 8:
            ## Format station text for placeile
            StationNames = "Station: " + station[0]
            ## Get lat and long
            lat = station[1]
            lon = station[2]
            ## Format temperture text for placeile
            Temperature = str(station[3]) + " F"
            ## Format temperture text for placeile in hover over text
            hTemperature = "Teperature: " + str(station[3]) + " F"
            ## Format dewpoint text for placeile in hover over text
            DewPoint = "Dewpoint: " + str(station[4]) + " F"
            ## Format windspeed text for placeile in hover over text
            WindSpeed = str(station[5])
            if WindSpeed == "Calm":
                WindSpeed = "Wind Speed: " +  str(station[5])
            else:
                WindSpeed = "Wind Speed: " + str(station[5]) + " mph"
            ## Format wind direction text for placeile in hover over text
            WindDirection = "Wind Direction: " + station[6]
            ## Format pressure text for placeile in hover over text
            Pressure = "Pressure: " + str(station[7]) + " in/Hg"

            ## (second part of line)Create a string with \n in the string without adding another line in the textfile/placefile
            hover = repr("\n".join([StationNames, hTemperature, DewPoint, WindSpeed, WindDirection, Pressure, time]))
            ## Write the first part of the line 
            p1 = "Text: " + str(lat) + " ," + str(lon) + ", 2, " + '"' + Temperature + '", ' + '"'
            ## Add the two part of the line to the same line
            line = p1 + hover[2:-1] + '"'
            ## Write the newly created line
            file.write(line)
            file.write('\n')
            
        ## If there is no pressure data
        if len(station) == 7:
            ## Internal process of this if statment is the same as the above if statement
            StationNames = "Station: " + station[0]
            lat = station[1]
            lon = station[2]
            Temperature = str(station[3]) + " F"
            hTemperature = "Teperature: " + str(station[3]) + " F"
            DewPoint = "Dewpoint: " + str(station[4]) + " F"
            WindSpeed = str(station[5])
            if WindSpeed == "Calm":
                WindSpeed = "Wind Speed: " +  str(station[5])
            else:
                WindSpeed = "Wind Speed: " + str(station[5]) + " mph"
            WindDirection = "Wind Direction: " + station[6]

            hover = repr("\n".join([StationNames, hTemperature, DewPoint, WindSpeed, WindDirection, time]))
            p1 = "Text: " + str(lat) + " ," + str(lon) + ", 2, " + '"' + Temperature + '", ' + '"'
            line = p1 + hover[2:-1] + '"'
            file.write(line)
            file.write('\n')

    ## Close the newly created placefile
    print "Text Placefile Created\n"
    file.close()

    
# Test the functions
if __name__ == "__main__":
    stations = [['Albany', 40.241061, -94.343492, 55.1, 50.5, u'10.1', u'WNW', u'29.83'],
                ['Brunswick', 39.412667, -93.1965, 61.5, 52.0, u'16.3', u'WSW', u'29.83'],
                ['Butler', 38.25191, -94.343547, 62.2, 51.2, u'10.6', u'W', u'29.88'],
                ['Clarkton', 36.490581, -89.961744, 72.5, 60.6, u'6.8', u'WSW', u'29.94'],
                ['Bradford', 38.897236, -92.21807, 63.9, 49.1, u'12.2', u'SW', u'29.83'],
                ['Capen Park', 38.929237, -92.321297, 66.5, 51.6, u'3.5', u'SW'],
                ['Jefferson Farm', 38.906992, -92.269976, 65.3, 50.1, u'14.1', u'WSW'],
                ['Sanborn', 38.942301, -92.320395, 66.9, 49.1, u'9.1', u'SW', u'29.85'],
                ['Cook Station', 37.797945, -91.429645, 68.6, 53.0, u'9.8', u'W', u'29.88'],
                ['Green Ridge', 38.621147, -93.416652, 61.3, 49.9, u'14.7', u'WSW', u'29.85'],
                ['Hayward', 36.395972, -89.614473, 72.2, 60.4, u'3.8', u'S', u'29.88'],
                ['Lamar', 37.493366, -94.318185, 66.0, 51.2, u'12.3', u'W', u'29.94'],
                ['Linneus', 39.856919, -93.149726, 55.0, 52.0, u'8.9', u'WSW'],
                ['Monroe City', 39.635314, -91.72537, 65.6, 54.1, u'11.6', u'SSW', u'29.85'],
                ['Moscow Mills', 38.938757, -90.931742, 68.1, 51.3, u'6.3', u'S', u'29.83'],
                ['Mountain Grove', 37.153865, -92.268831, 67.5, 49.0, u'9.7', u'WSW', u'29.95'],
                ['Mount Vernon', 37.077, -93.879, 67.2, 47.6, u'15.0', u'W', u'29.94'],
                ['Novelty', 40.018917, -92.190781, 55.7, 53.7, u'11.6', u'WSW', u'29.80'],
                ['Portageville', 36.413728, -89.69996, 72.3, 60.5, u'5.1', u'SW'],
                ['St. Joseph', 39.757821, -94.794567, 60.1, 49.8, u'11.3', u'NW'],
                ['Vandalia', 39.3023, -91.513, 64.6, 52.6, u'11.2', u'SSW', u'29.89'],
                ['Versailles', 38.4347, -92.853733, 66.9, 48.5, u'12.6', u'W', u'29.86'],
                ['Unionville', 40.466591, -93.002819, 52.6, 52.4, u'6.1', u'SW', u'29.74'],
                ['Williamsburg', 38.90735, -91.734217, 64.9, 50.1, u'10.3', u'SSW', u'29.85']]
    lngruntime = time.strftime("%Y/%m/%d %H:%M", time.gmtime())
    makePlaceFile(stations,lngruntime)
