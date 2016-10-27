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
import os
import arcpy
from arcpy import env
from itertools import tee, izip

##########################################################################################
#                               Let's group the points into pairs                        #
##########################################################################################

## http://stackoverflow.com/questions/5764782/iterate-through-pairs-of-items-in-a-python-list

def pointPair(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


##########################################################################################
#                               Let's make the polyline                                  #
##########################################################################################

########  Make a polyline front the shortest line  ###############
def PolylineMaker(frontpnts):
    print "Making polyline"  

    ## Locations ##
    rootfolder = os.getcwd()
    env.overwriteOutput = True
    env.workspace = os.path.join(rootfolder, "NIMBUSS.gdb")
    polyFront = os.path.join(env.workspace, "PolyFront")
    env.outputCoordinateSystem = arcpy.SpatialReference(4326)

    ## Check if polyline exists ##
    if arcpy.Exists(polyFront) == False:
        arcpy.CreateFeatureclass_management(env.workspace, "PolyFront", "POLYLINE")
    if arcpy.Exists(polyFront) == True:
        arcpy.Delete_management(polyFront)
        arcpy.CreateFeatureclass_management(env.workspace, "PolyFront", "POLYLINE")
      
    ## Set up Cursor and arrays
    array = arcpy.Array()
    featureList = []
    cursor = arcpy.InsertCursor(polyFront)
    feat = cursor.newRow()

    ## Create polyline ##
    for point1, point2 in pointPair(frontpnts):
        # Set X and Y for start and end points
        point = arcpy.Point(point1[1],point1[0])
        array.add(point)
        point = arcpy.Point(point2[1],point2[0])
        array.add(point)   
        # Create a Polyline object based on the array of points
        polyline = arcpy.Polyline(array)
        # Clear the array for future use
        array.removeAll()
        # Append to the list of Polyline objects
        featureList.append(polyline)
        # Insert the feature
        feat.shape = polyline
        cursor.insertRow(feat)
    del feat
    del cursor
        
    print "Polyline made"
    return polyFront
      
# Test the functions
if __name__ == "__main__":
    frontpnts = [[39.2877220942487, -91.32659052845936], [39.66111397792826, -91.85014042346452],
                 [39.82735204345924, -91.95742840508046], [39.458104421739684, -92.2045349974983],
                 [39.15598398062984, -92.70550038653711], [38.783011651599786, -92.86975282309447],
                 [38.776477297599364, -92.87015256967844], [38.76547746600604, -92.84445776734152],
                 [38.66640438964101, -92.53692385489886], [38.52826251130394, -93.13482935959159],
                 [39.0169723914758, -93.30718958881475], [37.285390354276416, -94.0979875758242]]
    PolylineMaker(frontpnts)

