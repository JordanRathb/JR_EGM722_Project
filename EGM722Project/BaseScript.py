#import pandas as pd
import geopandas as gpd
from cartopy.feature import ShapelyFeature
from shapely.geometry import LineString, Polygon
import cartopy.crs as ccrs
#import matplotlib.patches as patches
#import matplotlib.lines as lines
import matplotlib.pyplot as plt
#import rasterio as ras

#general template/workflow/to-do list:

#load the datasets
AONB = gpd.read_file('data_files/AONB_SE.shp') #AONB
NationalP = gpd.read_file('data_files/NationalParks_SE.shp') #National Parks
MSettlements = gpd.read_file('data_files/Settlements_SE.shp') #Major Cities and Towns
PopDens = gpd.read_file('data_files/PopDens_SE.shp') #Population Density
Watercourses = gpd.read_file('data_files/Watercourses_SE.shp')  #Rivers

PopDens = PopDens.to_crs(epsg=27700)
CRS = ccrs.UTM(29) #define crs


#figure creation
Figure = plt.figure(figsize=(30, 30))    #establish figure dimensions with plt
    #define a scale bar
Axes = plt.axes(projection=ccrs.Mercator())    #define axes
    #define legend library

#analysis idea:
SettlementBuffer = MSettlements.buffer(10000) #generate buffer around settlements with user defined distance
    #extract rivers that are outside the buffer zones
    #extract rivers that intersect with county polygons that are below a user defined threshold
    #generate buffer around river lines
    #clip county polygons to those that lay within the river buffers
    #output to figure

#to figure:
AONB_features = ShapelyFeature(AONB['geometry'], CRS, edgecolor='k', facecolor='green') #add AONB
NationalParks = ShapelyFeature(NationalP['geometry'], CRS, facecolor='darkseagreen') #add national parks
CitiesAndTowns = ShapelyFeature(MSettlements['geometry'], CRS, edgecolor='k', facecolor='dimgrey') #add settlements
CitiesAndTownsBuffer = ShapelyFeature(SettlementBuffer, CRS, edgecolor='r', alpha=0.5)
PopulationDensity = ShapelyFeature(PopDens['geometry'], CRS, edgecolor='k', facecolor='lightsalmon') #add county polygons with popdens
Water_courses = ShapelyFeature(Watercourses['geometry'], CRS, edgecolor='b') #add watercourses

xmin, ymin, xmax, ymax = PopDens.total_bounds

Axes.set_extent([xmin, xmax, ymin, ymax], crs=CRS)


Axes.add_feature(PopulationDensity)
Axes.add_feature(CitiesAndTowns)
Axes.add_feature(Water_courses)
Axes.add_feature(AONB_features)
Axes.add_feature(NationalParks)
Axes.add_feature(CitiesAndTownsBuffer)

#output individual shapesfiles (if user wishes to manipulate further in GIS):
    #AONB.shp
    #NationalParks.shp
    #MajorCitiesandTowns.shp
    #Rivers.shp
    #Roads.shp

#output map figure of performed analysis in this script
#Figure.savefig('Test.png', dpi=300)    #output map.png
