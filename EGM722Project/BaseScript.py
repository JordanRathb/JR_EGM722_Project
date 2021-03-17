import pandas as pd
import geopandas as gpd
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as patches
import matplotlib.lines as lines
import matplotlib.pyplot as plt
import rasterio as ras

#general template/workflow/to-do list:

#load the datasets
    #AONB
    #NationalParks
    #MajorCitiesandTowns
    #Rivers
    #Roads(?)

#define crs

#figure creation
    #establish figure dimensions with plt
    #define a scale bar
    #define axes
    #define legend library

#analysis idea:
    #where rivers intersect with AONB and NP
        #create buffer of rivers of x distance
    #buffer/distance function of roads and settlements
    #where buffers of rivers do not intersect with buffers of roads/settlements
        #store rivers in list
    #...

#to figure:
    #add NP and AONB
    #add new rivers
    #add settlement and road buffers
    #...
    #testing new branch

#output individual shapesfiles (if user wishes to manipulate further in GIS) -- may be redundant:
    #AONB.shp
    #NationalParks.shp
    #MajorCitiesandTowns.shp
    #Rivers.shp
    #Roads.shp

#output map figure of performed analysis in this script
    #output map.png
