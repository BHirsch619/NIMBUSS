##########################################################################################
##########################################################################################
# Created on: 20160417                                                                   #
# Created by: Brian Hirsch                                                               #
# Where: University of Missouri                                                          #
# Actions: Create a jpeg map                                                             #
# Permissions/Distribution: Copyrighted Brian Hirsch 2016                                #
# Class: GEOG 4940                                                                       #
# Final Project                                                                          #
##########################################################################################
##########################################################################################

##########################################################################################
#                               Initialization                                           #
##########################################################################################

##### Imports ##### 
import arcpy
from arcpy import env
import os, time

##########################################################################################
#                               Padded Extent Function                                   #
##########################################################################################

def paddedExtent(originalExtent, padPercentage = 1):
    # find the four corners of the extents
    XMin, YMin, XMax, YMax = originalExtent.XMin, originalExtent.YMin, originalExtent.XMax, originalExtent.YMax
    # calcate percent from padpercent 
    percent = float(padPercentage) / float(100)
    # find distance to extend the extent
    XPad = (XMax - XMin) * percent
    YPad = (YMax - YMin) * percent
    # return the new padded extent
    return arcpy.Extent(XMin - XPad, YMin - YPad, XMax + XPad, YMax + YPad)

##########################################################################################
#                               Makes map with avaliable data                            #
##########################################################################################

def MapMaker(stationFC, front, strtime, lngtime, StationsFCName):

    ## Locations  ##
    rootFolder = os.getcwd()
    outputFolder = os.path.join(rootFolder, "PDFs")
    outputPDF = os.path.join(outputFolder, strtime + ".pdf")
    outputJPGFolder = os.path.join(rootFolder, "JPGs")
    outputJPG = os.path.join(outputJPGFolder, strtime + ".jpg")

    ## Template Locations ##
    templateFolder = os.path.join(rootFolder, "templates")
    maptemplateLocation = os.path.join(templateFolder, "MapTemplate.mxd")
    FrontTemplate = os.path.join(templateFolder, "FrontTemplate.lyr")
    WindTemplate = os.path.join(templateFolder, "MOstations.lyr")
    LabelTemplate = os.path.join(templateFolder, "MOstationsLabel.lyr")
    MOTemplate = os.path.join(templateFolder, "MOCounties.lyr")

    ## Arc Environment ##
    env.workspace = os.path.join(rootFolder, "NIMBUSS.gdb")
    MoBackground = os.path.join(env.workspace, "MOCounties")
    env.overwriteOutput = True 

    print "\nMaking a map of the current conditions"
    
    ## Setup a variable for the map document and each data frame
    mapDocument = arcpy.mapping.MapDocument(maptemplateLocation)
    # Main map is the first data frame
    mainMap = arcpy.mapping.ListDataFrames(mapDocument)[0]

    ############# Label Stations ##############

    # locate the new layer (LabelLayer) in the map document
    LabelLayer = arcpy.mapping.ListLayers(mapDocument, '*', mainMap)[0]
    # Replace dataset
    LabelLayer.replaceDataSource(env.workspace,"FILEGDB_WORKSPACE", StationsFCName)
    # apply the symbology from a layer file to the stations layer
    arcpy.ApplySymbologyFromLayer_management(LabelLayer, LabelTemplate)

    # Make labels
    if LabelLayer.supports("LABELCLASSES"):
        ## Display class labels
        for lblclass in LabelLayer.labelClasses:
            lblclass.showClassLabels = True
    ## Show labels
    LabelLayer.showLabels = True
    ## Refresh view
    arcpy.RefreshActiveView()
    
    ############# Front ####################
    ## Chek if there was a front made
    if front <> None:
        frontLayer = "frontLayer"
        # Make the new featurelayer with front
        arcpy.MakeFeatureLayer_management(front, frontLayer)

        # name the new feature layer
        inFrontLayer = arcpy.mapping.Layer(frontLayer)
        # add the new layer to the top of the main map data frame 
        arcpy.mapping.AddLayer(mainMap, inFrontLayer, "BOTTOM")

        # locate the new layer (inFrontLayer) in the map document
        inFrontLayer = arcpy.mapping.ListLayers(mapDocument, '*', mainMap)[1]
        # apply the symbology from a layer file to the front layer
        arcpy.ApplySymbologyFromLayer_management(inFrontLayer, FrontTemplate)



    ############# Wind Stations ############

    # reserve place in memory for the stations
    tempStations = "in_memory\\Stations"
    # name the stationLabels layer
    WindLayer = "WindLayer"
    # copy the selected places into memory as feature class
    arcpy.CopyFeatures_management(stationFC, tempStations)
    # make the stations class a new feature layer
    arcpy.MakeFeatureLayer_management(stationFC, WindLayer)

    # name the new layer as inWindLayer here in the code
    inWindLayer = arcpy.mapping.Layer(WindLayer)
    # add the Wind layer to the top of the main map data frame 
    arcpy.mapping.AddLayer(mainMap, inWindLayer, "TOP")

    # locate the new layer (inWindLayer) in the map document
    inWindLayer = arcpy.mapping.ListLayers(mapDocument, '*', mainMap)[0]
    # apply the symbology from a layer file to the new inWindLayer in memory
    arcpy.ApplySymbologyFromLayer_management(inWindLayer, WindTemplate)

    ############# Base Layer ############

    # reserve place in memory for the base layer
    tempMO = "in_memory\\MO"
    # name the base
    MOLayer = "MO"
    # copy the layer into memory as feature class
    arcpy.CopyFeatures_management(MoBackground, tempMO)
    # make the base a new feature layer
    arcpy.MakeFeatureLayer_management(MoBackground, MOLayer)

    # name the new layer as inMOLayer here in the code
    inMOLayer = arcpy.mapping.Layer(MOLayer)
    # add the base layer to the top of the main map data frame 
    arcpy.mapping.AddLayer(mainMap, inMOLayer, "BOTTOM")
    # Check position of base layer depending on if there was a front found
    if front <> None:
        pos = 3
    if front == None:
        pos = 2
    # locate the new layer (inMOLayer) in the map document
    inMOLayer = arcpy.mapping.ListLayers(mapDocument, '*', mainMap)[pos]
    # apply the symbology from a layer file to the new inMOLayer in memory
    arcpy.ApplySymbologyFromLayer_management(inMOLayer, MOTemplate)

    # Change map title
    mapDocument.title = lngtime + "UTC"

    # Adjust the extent of the map
    mainMap.extent = paddedExtent(inMOLayer.getExtent(False))

    ## Export the map to a jpeg
    arcpy.mapping.ExportToJPEG(mapDocument, outputJPG, resolution = 300)

    # Close the function
    return None

# Test the functions
if __name__ == "__main__":
    
    rootfolder = os.getcwd()
    env.workspace = os.path.join(rootfolder, "FinalProject.gdb")
    stationFCName = "MOstationsTest"
    stationFC = os.path.join(env.workspace, stationFCName)
    front = os.path.join(env.workspace, "PolyFront")
    srtruntime = time.strftime("%Y%m%d%H%M", time.gmtime())
    lngruntime = time.strftime("%Y/%m/%d %H:%M", time.gmtime())
    StationFCName = "MOstationsTest1"
    
    MapMaker(stationFC, front, srtruntime, lngruntime, StationFCName)
