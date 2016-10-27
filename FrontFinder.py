##########################################################################################
##########################################################################################
#   Created on: 20160415                                                                 #
#   Created by: Brian Hirsch                                                             #
#   Where: University of Missouri                                                        #
#   Actions: Looks for an atmopsheric boundry                                            #
#   Permissions/Distribution: Copyrighted Brian Hirsch 2016                              #
#   Class: GEOG 4940                                                                     #
#   Final Project                                                                        #
##########################################################################################
##########################################################################################

##########################################################################################
#                               Initialization                                           #
##########################################################################################

##### Imports ##### 
import os, itertools, math, copy
import arcpy
from geographiclib.geodesic import Geodesic
from arcpy import env

##########################################################################################
#                               Let's find an distance between points                    #
##########################################################################################

## This function finds the closest point
def closestPt(ptd,lst):
    ## Creates an arcpy point from the inputed point
    pt = arcpy.Point(ptd[0],ptd[1])
    ## Sets the coordinate system to GCS WGS 1984
    spatial_reference = arcpy.SpatialReference(4326)
    ## Creates points geometry for the points
    ptGeom = arcpy.PointGeometry(pt, spatial_reference)
    ## Creates two closest variable placeholders of nonetype
    closestDist = None
    clostestPt = None
    ## Loops through the list of possible closest points in the sent list
    for possiblepts in lst:
        ## makes the possible point into an arcpy point
        possiblept = arcpy.Point(possiblepts[0], possiblepts[1])
        ## finds the distance to the possible point from the inputted point (ptd)
        distance = ptGeom.distanceTo(possiblept)
        ## converts distance to point
        distance = float(distance)
        ## In human, "if closest found distance or closest is greater than found distance"
        if closestDist == None or closestDist > distance:
            ## Reset closest points to the new possible point
            clostestPt = possiblepts
            ## Reset closest disance to the new closest distance
            closestDist = distance
    ## Return the closest point and the corresponding distance
    return clostestPt, closestDist

##########################################################################################
#                               Let's find an atmospheric boundry                        #
##########################################################################################

##### This function looks for a boundary/front
def findFront(stations, time):
    ## iteration through all possible combinations of station points
    iteration = list(itertools.combinations(stations, 2))
    ## Start a list for found front points
    frontpoints = []
    ## look for possible frontal points, by looping through iteration
    for points in iteration:
        ## Get lat and long from point
        st1 = points[0]
        st2 = points[1]
        ## define the two station points as a tuple
        p0 = (st1[1],st1[2])
        p1 = (st2[1],st2[2])
        ## find the distance between points
        distance = math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
        ## if distance is less than 1.2 degrees and greater than 0.1 then
        if distance <= 1.2 and distance > 0.1:
            ## Get the temp, dewpoint and wind direction from the station data
            t0,t1 = st1[3],st2[3]
            d0,d1 = st1[4],st2[4]
            wd0, wd1 = st1[6], st2[6]
            ## Check if there is null wind speed
            if wd0 is not None:
                ## Check if there is null wind speed
                if wd1 is not None:
                    ## Find the midpoints Using geodesic module
                    if (abs(t0-t1) >= 10 and abs(d0-d1) >= 10) or (abs(wd0-wd1) >= 150):
                        ## Find the mid point
                        ## http://geographiclib.sourceforge.net/html/python/code.html#geographiclib.geodesic.Geodesic.Inverse
                        g = Geodesic.WGS84.Inverse(p0[0], p0[1], p1[0], p1[1])
                        h1 = Geodesic.WGS84.Direct(p0[0], p0[1], g['azi1'], g['s12']/2)
                        ## Grab the midpoint from the above function
                        mdlat = h1['lat2']
                        mdlon = h1['lon2']
                        ## Create a list for the mid point and add midpoint to list
                        md = []
                        md.append(mdlat)
                        md.append(mdlon)
                        ## Add new found mid point to front point list
                        frontpoints.append(md)
    del iteration, distance
    
    ## Is there really a front or is there just a few outliers
    print "\nChecking for an atmospheric boundary"
    ## By seeing if there is more than 5 points flagged
    if len(frontpoints) >= 5:
        ## Let the user know how many front points were found if there are enough
        print "Found a boundry useing %s points of the 5 needed" % len(frontpoints) 
        print "Looking for shortest path"
        ## Start lists for the distances between point and the points in that list
        lstdist = []
        fullpntlst = []
        
        ## Add first point before the while loop to be sure to include all points
        ## Pick a point from front points to start then do the rest
        for pt in frontpoints:
            ## Set distance to 0
            dist = 0
            ## Make a copy of the front points
            copyPts = copy.copy(frontpoints)
            ## Create a point list for this iteration
            pntlst = []
            ## Add the first point to the point list
            pntlst.append(pt)
            ## Remove the first list from the copied point list
            copyPts = [x for x in copyPts if x != pt]

            ## While there is still points in the copied point list
            while len(copyPts) > 0:
                ## find the losest point to the current point of interest
                pt2, new = closestPt(pt, copyPts)
                ## Update the distance
                dist += new
                ## Add new closest point to the list
                pntlst.append(pt2)
                ## Get rid of the new closest point 
                copyPts = [x for x in copyPts if x != pt2]
                ## Set the new point to be the starting point for next loop
                pt = pt2

            ## Add points of lines and the distance of the line to the lists    
            fullpntlst.append(pntlst)
            lstdist.append(dist)
            del pntlst, dist, pt, pt2

        ## Find the shortest path from the list of list of points  
        loc_shortest = lstdist.index(min(lstdist))
        shortest_dist = lstdist[loc_shortest]
        shortest_line = fullpntlst[loc_shortest]
        del shortest_dist, loc_shortest, lstdist, fullpntlst, frontpoints

        ## Set frontFound to true
        frontFound = True

        ## Return list of points of the shortest line and that a front was found
        ##### Returns valuse as (Y,X)
        return shortest_line, frontFound
            
    ## if there is not boundary return nothing and that a front was not found
    else:
        print "Could not find an atmopheric boundary"
        return None, False


# Test the functions
if __name__ == "__main__":
    import time
    stations = [['Albany', 40.241061, -94.343492, 53.4, 48.8, u'6.4', 337.5, u'30.21'],
                ['Brunswick', 39.412667, -93.1965, 59.0, 55.8, u'8.4', 337.5, u'30.21'],
                ['Butler', 38.25191, -94.343547, 58.7, 55.5, u'3.9', 22.5, u'30.18'],
                ['Bradford', 38.897236, -92.21807, 62.7, 59.8, u'2.3', 157.5, u'30.18'],
                ['Capen Park', 38.929237, -92.321297, 64.4, 63.2, 0, 225],
                ['Jefferson Farm', 38.906992, -92.269976, 63.8, 60.1, u'1.7', 225],
                ['Sanborn', 38.942301, -92.320395, 63.3, 61.2, u'2.6', 225, u'30.20'],
                ['Green Ridge', 38.621147, -93.416652, 57.6, 57.6, u'6.1', 0, u'30.18'],
                ['Lamar', 37.493366, -94.318185, 60.5, 59.1, u'4.2', 0, u'30.19'],
                ['Linneus', 39.856919, -93.149726, 56.9, 53.9, u'4.3', 337.5],
                ['Monroe City', 39.635314, -91.72537, 67.2, 61.0, u'5.0', 135, u'30.21'],
                ['Moscow Mills', 38.938757, -90.931742, 65.6, 59.6, u'2.1', 270, u'30.18'],
                ['Mountain Grove', 37.153865, -92.268831, 61.2, 57.4, u'3.6', 135, u'30.24'],
                ['Mount Vernon', 37.077, -93.879, 64.6, 57.4, u'4.0', 157.5, u'30.18'],
                ['Novelty', 40.018917, -92.190781, 60.1, 60.1, u'5.7', 337.5, u'30.18'],
                ['St. Joseph', 39.757821, -94.794567, 54.6, 53.5, u'5.2', 337.5],
                ['Vandalia', 39.3023, -91.513, 65.3, 62.6, u'3.6', 157.5, u'30.23'],
                ['Versailles', 38.4347, -92.853733, 62.7, 61.6, u'3.0', 292.5, u'30.17'],
                ['Unionville', 40.466591, -93.002819, 54.8, 53.2, u'4.1', 337.5, u'30.15'],
                ['Williamsburg', 38.90735, -91.734217, 62.7, 60.9, u'2.4', 180, u'30.19']]
    srtruntime = time.strftime("%Y%m%d%H%M", time.gmtime())
    findFront(stations, srtruntime)
