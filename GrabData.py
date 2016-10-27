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

##### Imports ##### 
import requests, time
from bs4 import BeautifulSoup
##########################################################################################
#                               Convert Wind Direction                                   #
##########################################################################################

##### This function converts a lettered wind direction to a degreed wind direction ##### 
def ConvertWindDirect(winddirc):
    if winddirc == "N":
        winddirc = 0
    if winddirc == "NNE":
        winddirc = 22.5
    if winddirc == "NE":
        winddirc = 45
    if winddirc == "ENE":
        winddirc = 67.5
    if winddirc == "E":
        winddirc = 90
    if winddirc == "ESE":
        winddirc = 112.5
    if winddirc == "SE":
        winddirc = 135
    if winddirc == "SSE":
        winddirc = 157.5
    if winddirc == "S":
        winddirc = 180
    if winddirc == "SSW":
        winddirc = 202.5
    if winddirc == "SW":
        winddirc = 225
    if winddirc == "WSW":
        winddirc = 247.5
    if winddirc == "W":
        winddirc = 270
    if winddirc == "WNW":
        winddirc = 292.5
    if winddirc == "NW":
        winddirc = 315
    if winddirc == "NNW":
        winddirc = 337.5
    if winddirc == "Calm":
        winddirc = None
    return winddirc

##########################################################################################
#                               Let's do some data mining                                #
##########################################################################################

## This function grabs data from the mesonet sites
def GrabData():
    print "Downloading station data"

    ## Start too lists to store the mined data
    #### Contains degree wind direcitons
    global_stations = []
    #### Contains the lettered wind directions (i.e. N, S, E, W)
    text_stations = []

    ## List of station names
    StationNames = ["Albany", "Brunswick", "Butler", "Clarkton", "Bradford Farm", "Capen Park", "Jefferson Farm",
                "Sanborn Field", "Cook Station", "Green Ridge", "Hayward", "Lamar", "Linneus", "Monroe City",
                "Moscow Mills", "Mountain Grove", "Mount Vernon", "Novelty", "Portageville",
                "St. Joseph", "Vandalia", "Versailles", "Unionville", "Williamsburg"]

    ## All of the URLs that will be mined
    URLs = ["http://agebb.missouri.edu/weather/realtime/albany.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/brunswick.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/butler.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/clarkton.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/columbiaBradford.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/columbiacapen.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/columbiajefferson.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/columbiaSanborn.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/cookstation.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/greenridge.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/hayward.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/lamar.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/linneus.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/monroe.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/moscowmills.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/mountaingrove.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/mtvernon.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/novelty.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/portageville.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/stjoseph.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/vandalia.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/versailles.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/unionville.php#more-conditions-page",
            "http://agebb.missouri.edu/weather/realtime/williamsburg.php#more-conditions-page"]

    ## Lists with the latitude and longidude of the station (order is important in these lists)
    lat = [40.241061, 39.412667, 38.251910, 36.490581, 38.897236, 38.929237, 38.906992,
           38.942301, 37.797945, 38.621147, 36.395972, 37.493366, 39.856919, 39.635314,
           38.938757, 37.153865, 37.077000, 40.018917, 36.413728, 39.757821, 39.302300,
           38.434700, 40.466591, 38.907350]
    lon = [-94.343492, -93.196500, -94.343547, -89.961744, -92.218070, -92.321297, -92.269976,
           -92.320395, -91.429645, -93.416652, -89.614473, -94.318185, -93.149726, -91.725370,
           -90.931742, -92.268831, -93.879000, -92.190781, -89.699960, -94.794567, -91.513000,
           -92.853733, -93.002819, -91.734217]
    
    ## Count is used as an index location in the predefined lists above
    count = 0

    ## For each URL in the URLs list
    for URL in URLs:
        ## Try to download the HTML
        try:
            rawHTML = requests.get(URL).text
        ## If unable to download the HTML wait five seconds and try again
        except:
            print "Couldn't get data, going to sleep."
            time.sleep(5)
            rawHTML = requests.get(URL).text

        ## Define flags in the HTML
        Datalocate = "collapsible"
        Dataclass = "ui-bar"
        Pressclass = "ui-body"

        ## Put some soup on the burner with a little html in there
        soup = BeautifulSoup(rawHTML, 'html.parser')

        ## Find all sections with the Datalocate flag
        for datalocate in soup.find_all("div", class_=Datalocate):
            
            ## Create lists for each station to be added to the larger list of all of the stations
            station = []
            text = []
            
            ## Insert station name, lat, and long into list
            station.append(StationNames[count])
            station.append(lat[count])
            station.append(lon[count])
            text.append(StationNames[count])
            text.append(lat[count])
            text.append(lon[count])
            ## add to count for next station info from predefined lists
            count += 1
            
            ## Get temp (F)
            #### Grab the first element with a Dataclass tag
            temp = datalocate.find_all("div", class_=Dataclass)[0]
            #### grab the first content from the temp string
            temp =  temp.contents[0]
            #### Remove the degree and F characters
            temp = float(temp[0:-2])
            #### Add the temp string to the lists
            text.append(temp)
            station.append(temp)
            del temp

            ##  Get dewpoint (F)
            #### Grab the second element with a Dataclass tag
            dew = datalocate.find_all("div", class_=Dataclass)[1]
            #### grab the first content from the dew string
            dew = dew.contents[0]
            #### Remove the degree and F characters
            dew = float(dew[0:-2])
            #### Add the dew string to the lists
            text.append(dew)
            station.append(dew)
            del dew

            ## Get Wind speed (mph)
            #### Grab the fifth element with a Dataclass tag
            windspd = datalocate.find_all("div", class_=Dataclass)[4]
            #### grab the first content from the windspeed string
            windspd = windspd.contents[0]
            #### Spilt by the space and grab the first part
            windspd = windspd.split(" ")[0]
            #### Add the text wind speed
            text.append(windspd)
            #### Change calm wind to 0
            if windspd == "Calm":
                windspd = 0
            #### Add the numeric wind speed
            station.append(windspd)
            del windspd

            ## Find wind direction
            #### Get all div flags
            datas = datalocate.find_all("div")
            #### Search div flags with Wind Dir: text
            data = datalocate.find("div", text="Wind Dir:")
            #### Find index of data then add 2 to the index to get location of wind direction
            winddirloc = long(datas.index(data)) + 2
            #### Get the wind direction data flag
            winddir = datalocate.find_all("div")[winddirloc]
            #### Remove the data from the flag
            winddir = winddir.string
            #### Add text wind direciton
            text.append(winddir)
            #### Convert to degree wind direction
            winddir = ConvertWindDirect(winddir)
            #### Add degree wind direciton to list
            station.append(winddir)
            del winddir, data

            ## Find pressure (in/Hg)
            #### Search div flags with Baro. Pressure: text
            data = datalocate.find("div", text="Baro. Pressure:")
            #### Check if pressure is messured at the station
            if data <> None:
                #### Find index of data then add 2 to the index to get location of pressure
                pressloc = long(datas.index(data)) + 2
                #### Get the wind direction data flag
                press = datalocate.find_all("div")[pressloc]
                #### Remove the data from the flag
                press = press.string
                #### Spilt by the space and grab the first part
                press = press.split(" ")[0]
                #### Add pressure to lists
                text.append(press)
                station.append(press)
                del press,data, datalocate, pressloc

            ## break stops the loop
            break
        ## Add individual staiton lists to the larger lists with all the data
        text_stations.append(text)
        global_stations.append(station)
    print "Downloaded data for %s of %s stations" %(count, len(StationNames))
    del count
    ## return the lists of data
    return global_stations, text_stations

# Test the functions
if __name__ == "__main__":
    GrabData()
