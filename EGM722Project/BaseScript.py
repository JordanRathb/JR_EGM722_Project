#import pandas as pd
import geopandas as gpd
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
#import matplotlib.patches as patches
#import matplotlib.lines as lines
import matplotlib.pyplot as plt
#import rasterio as ras

#general template/workflow/to-do list:

#load the datasets
AONB = gpd.read_file('data_files/AONB.shp')    #AONB
NationalP = gpd.read_file('data_files/National_Parks_(December_2018)_Boundaries_GB_BGC.shp')    #NationalParks
MSettlements = gpd.read_file('data_files/Major_Towns_and_Cities__December_2015__Boundaries.shp')    #MajorCitiesandTowns
    #Rivers
    #Roads(?)

CRS = ccrs.UTM(30) #define crs

#figure creation
Figure = plt.figure(figsize=(30, 30), edgecolor='k')    #establish figure dimensions with plt
    #define a scale bar
Axes = plt.axes(projection=ccrs.Mercator())    #define axes
    #define legend library

#analysis idea:
    #where rivers intersect with AONB and NP
        #create buffer of rivers of x distance
    #buffer/distance function of roads and settlements
    #where buffers of rivers do not intersect with buffers of roads/settlements
        #store rivers in list
    #...

#to figure:
AONB_features = ShapelyFeature(AONB['geometry'], CRS, edgecolor='k', facecolor='green')    #add NP and AONB
NationalParks = ShapelyFeature(NationalP['geometry'], CRS, facecolor='darkseagreen')    #add new rivers
CitiesAndTowns = ShapelyFeature(MSettlements['geometry'], CRS, edgecolor='k', facecolor='dimgrey')
    #add settlement and road buffers
    #...
    #testing new branch

xmin, ymin, xmax, ymax = NationalP.total_bounds

Axes.set_extent([xmin, xmax, ymin, ymax], crs=CRS)
Axes.add_feature(AONB_features)
Axes.add_feature(NationalParks)
Axes.add_feature(CitiesAndTowns)

#output individual shapesfiles (if user wishes to manipulate further in GIS) -- may be redundant:
    #AONB.shp
    #NationalParks.shp
    #MajorCitiesandTowns.shp
    #Rivers.shp
    #Roads.shp

#output map figure of performed analysis in this script
Figure.savefig('testfigure.png', dpi=300)    #output map.png
