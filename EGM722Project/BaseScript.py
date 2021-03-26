# import pandas as pd
import geopandas as gpd
from cartopy.feature import ShapelyFeature
# from shapely.geometry import LineString, Polygon
import cartopy.crs as ccrs
# import matplotlib.patches as patches
# import matplotlib.lines as lines
import matplotlib.pyplot as plt

# load the datasets
AONB = gpd.read_file('data_files/AONB_SE.shp')  # AONB
NationalP = gpd.read_file('data_files/NationalParks_SE.shp')  # National Parks
MSettlements = gpd.read_file('data_files/Settlements_SE.shp')  # Major Cities and Towns
PopDens = gpd.read_file('data_files/PopDens_SE.shp')  # Population Density
Watercourses = gpd.read_file('data_files/Watercourses_SE.shp')  # Rivers

# set the crs of shapefiles/define the intended crs of output
PopDens = PopDens.to_crs(epsg=27700)
CRS = ccrs.UTM(29)  # define crs


# figure creation
Figure = plt.figure(figsize=(30, 30))  # establish figure dimensions with plt
# define a scale bar
Axes = plt.axes(projection=ccrs.Mercator())  # define axes
# define legend library

# analysis:

# Buffer function:
# for docstring


def bufferfunction(self, distance):
    global buffer
    buffer = self.buffer(distance)
    return buffer


# generate settlement buffers
buffer = bufferfunction(MSettlements, 10000)  # generate buffer around settlements with user defined distance
Settlementbuffers = buffer  # define variable containing settlement buffers
Settlementbuffers = gpd.geoseries.GeoSeries([geom for geom in Settlementbuffers.unary_union.geoms])  # merge overlapping buffers to one
Settlementbuffers_gdf = gpd.GeoDataFrame(gpd.GeoSeries(Settlementbuffers))  # convert the geoseries into a geodataframe
Settlementbuffers_gdf = Settlementbuffers_gdf.rename(columns={0: 'geometry'}).set_geometry('geometry')  # rename the geometry column from '0' to 'geometry'
Settlementbuffers_gdf.crs = 'epsg:27700'  # define the crs of the settlement buffers to epsg = 27700


# extract rivers that are outside the buffer zones
RiverExtractOutsideSettlement = gpd.overlay(Watercourses, Settlementbuffers_gdf, how='difference', keep_geom_type=False)  # select through difference where rivers do not overlay the buffers around settlements

# extract rivers that intersect with county polygons that are below a user defined threshold
# generate buffer around river lines
# clip county polygons to those that lay within the river buffers


# output elements to shapely features to be loaded into the figure:
AONB_features = ShapelyFeature(AONB['geometry'], CRS, edgecolor='k', facecolor='green')  # add AONB
NationalParks = ShapelyFeature(NationalP['geometry'], CRS, facecolor='darkseagreen')  # add national parks
CitiesAndTowns = ShapelyFeature(MSettlements['geometry'], CRS, edgecolor='k', facecolor='dimgrey')  # add settlements
CitiesAndTownsBuffer = ShapelyFeature(Settlementbuffers, CRS, edgecolor='k', alpha=0.5)  # add settlement buffers
PopulationDensity = ShapelyFeature(PopDens['geometry'], CRS, edgecolor='k', facecolor='lightsalmon')  # add county polygons with popdens
Water_courses = ShapelyFeature(Watercourses['geometry'], CRS, edgecolor='b')  # add watercourses
Water_coursesOS = ShapelyFeature(RiverExtractOutsideSettlement['geometry'], CRS, edgecolor='r')

xmin, ymin, xmax, ymax = PopDens.total_bounds  # define the maximum extent of figure to the population density shapefile
Axes.set_extent([xmin, xmax, ymin, ymax], crs=CRS)  # set the maximum extent of figure to the population density shapefile

# add features to the axes/figure
Axes.add_feature(PopulationDensity)
Axes.add_feature(CitiesAndTowns)
Axes.add_feature(Water_courses)
Axes.add_feature(Water_coursesOS)
Axes.add_feature(AONB_features)
Axes.add_feature(NationalParks)
Axes.add_feature(CitiesAndTownsBuffer)

# output individual shapefiles (if user wishes to manipulate further in GIS):
# AONB.shp
# NationalParks.shp
# MajorCitiesandTowns.shp
# Rivers.shp
# Roads.shp

Figure.savefig('Test.png', dpi=300)  # output map figure of performed analysis in this script
