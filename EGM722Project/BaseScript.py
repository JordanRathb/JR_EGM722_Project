# import pandas as pd
import geopandas as gpd
from cartopy.feature import ShapelyFeature
# from shapely.geometry import LineString, Polygon
import cartopy.crs as ccrs
from mpl_toolkits.axes_grid1 import make_axes_locatable as max
import matplotlib.patches as patches
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
Figure, Axes = plt.subplots(1, 1, figsize=(30, 30), subplot_kw=dict(projection=CRS))  # define figure and axes with a subplot for a Choropleth plot
# define legend library


def generate_handles(labels, colors, edge='k', alpha=1):
    # docstring
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(patches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles
# define a scale bar

# analysis:

# Buffer function:


def bufferfunction(self, distance):
    # for docstring
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
PopDensitySelect = PopDens[PopDens['GB_dist__3'] > 360]  # select counties with a pop density above a certain threshold
RiverExtractPopDens = gpd.overlay(RiverExtractOutsideSettlement, PopDensitySelect, how='difference', keep_geom_type=False)  # select rivers that lie outside of these counties

# generate buffer around river lines
RiverBuffer = bufferfunction(RiverExtractPopDens, 1000)  # generate a buffer around rivers outside of selected counties and distance from settlements
RiverBuffer = gpd.GeoDataFrame(gpd.GeoSeries(RiverBuffer))  # convert the geoseries into a geodataframe
RiverBuffer = RiverBuffer.rename(columns={0: 'geometry'}).set_geometry('geometry')  # rename the geom column from 0 to geometry

# clip county polygons to those that lay within the river buffers
ViableLand = gpd.overlay(PopDens, RiverBuffer, how='intersection', keep_geom_type=False)  # select land that is within the river buffers
ViableLand = gpd.geoseries.GeoSeries([geom for geom in ViableLand.unary_union.geoms])  # merge land into one
ViableLand = gpd.GeoDataFrame(gpd.GeoSeries(ViableLand))  # convert the geoseries into a geodataframe
ViableLand = ViableLand.rename(columns={0: 'geometry'}).set_geometry('geometry')  # rename the geom column from 0 to geometry

# output elements to shapely features to be loaded into the figure:
AONB_features = ShapelyFeature(AONB['geometry'], CRS, edgecolor='k', facecolor='green')  # add AONB

NationalParks = ShapelyFeature(NationalP['geometry'], CRS, facecolor='darkseagreen')  # add national parks

CitiesAndTowns = ShapelyFeature(MSettlements['geometry'], CRS, edgecolor='k', facecolor='dimgrey')  # add settlements

CitiesAndTownsBuffer = ShapelyFeature(Settlementbuffers, CRS, edgecolor='k', alpha=0.5)  # add settlement buffers

Water_courses = ShapelyFeature(Watercourses['geometry'], CRS, edgecolor='b')  # add watercourses

Water_coursesOS = ShapelyFeature(RiverExtractOutsideSettlement['geometry'], CRS, edgecolor='r')

ViableLandShp = ShapelyFeature(ViableLand['geometry'], CRS, edgecolor='b', facecolor='springgreen')

RiverBufferShp = ShapelyFeature(RiverBuffer['geometry'], CRS, facecolor='b')

xmin, ymin, xmax, ymax = PopDens.total_bounds  # define the maximum extent of figure to the population density shapefile
Axes.set_extent([xmin, xmax, ymin, ymax], crs=CRS)  # set the maximum extent of figure to the population density shapefile

# add features to the axes/figure
colorbar = max(Axes)
cax = colorbar.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)
PopDens.plot(column='GB_dist__3', ax=Axes, vmin=50, vmax=1000, cax=cax, cmap='OrRd',
             legend=True, legend_kwds={'label': 'Population Density'})  # add county polygons with graduation of colour for pop density


Axes.add_feature(CitiesAndTowns)
# Axes.add_feature(Water_courses)
Axes.add_feature(Water_coursesOS)
# Axes.add_feature(RiverBufferShp)
Axes.add_feature(ViableLandShp)
Axes.add_feature(AONB_features)
Axes.add_feature(NationalParks)
# Axes.add_feature(CitiesAndTownsBuffer)

# generate legend
corridor_handle = generate_handles(['Wildlife Corridors'], ['springgreen'])

river_handle = generate_handles(['Rivers'], ['r'])

settlement_handle = generate_handles(['Settlements'], ['dimgrey'])

NP_handle = generate_handles(['National Parks'], ['darkseagreen'])

AONB_handle = generate_handles(['AONB'], ['green'])

labels = ['Rivers', 'Wildlife Corridors', 'National Parks', 'AONB', 'Settlements']

handles = river_handle + corridor_handle + settlement_handle + AONB_handle + NP_handle
legend = Axes.legend(handles, labels, title='Legend', title_fontsize=30,
                     fontsize=25, loc='upper left', frameon=True, framealpha=1)

# output individual shapefiles (if user wishes to manipulate further in GIS):
# AONB.shp
# NationalParks.shp
# MajorCitiesandTowns.shp
# Rivers.shp
# Roads.shp

Figure.savefig('Test.png', dpi=300)  # output map figure of performed analysis in this script
