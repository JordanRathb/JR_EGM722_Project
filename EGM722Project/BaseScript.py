import geopandas as gpd
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
from mpl_toolkits.axes_grid1 import make_axes_locatable as m_ax
import matplotlib.patches as patches
import matplotlib.pyplot as plt

# load the datasets
AONB = gpd.read_file('data_files/AONB_SE.shp')  # AONB
NationalP = gpd.read_file('data_files/NationalParks_SE.shp')  # National Parks
MSettlements = gpd.read_file('data_files/Settlements_SE.shp')  # Major Cities and Towns
PopDens = gpd.read_file('data_files/PopDens_SE.shp')  # Population Density
Watercourses = gpd.read_file('data_files/Watercourses_SE.shp')  # Rivers

# set the crs of shapefiles/define the intended crs of output
PopDens = PopDens.to_crs(epsg=27700)
Watercourses = Watercourses.to_crs(epsg=27700)
AONB = AONB.to_crs(epsg=27700)
NationalP = NationalP.to_crs(epsg=27700)
MSettlements = MSettlements.to_crs(epsg=27700)

CRS = ccrs.UTM(29)  # define crs

# figure creation
# define figure and axes with a subplot for a Choropleth plot
Figure, Axes = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=CRS))

xmin, ymin, xmax, ymax = PopDens.total_bounds  # define the maximum extent of figure to the population density shapefile
Axes.set_extent([xmin, xmax, ymin, ymax], crs=CRS)  # set the maximum extent of figure to the population density shapefile

gl = Axes.gridlines(draw_labels=False,
                    xlocs=[-8, -8.5, -9, -9.5, -10, -10.5, -11],
                    ylocs=[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4])
gl.right_labels = False
gl.bottom_labels = False


def scale_bar(axes, length, location=(0.85, 0.05), linewidth=3):
    """
    Creates a scale bar based on defined axes with a specified length.

    :param axes: the axes used to create the scale bar, based on the distance units of the projection.
    :param length: the length of the scale bar, calculated from the extent of the axes (in km).
    :param location: the desired location from 0, 0 to 10, 10.
    :param linewidth: the width of scale bar

    Typical usage:
    scale_bax(axes, 100)
    """
    # retrieve the extent of the axes in PlateCarree projection
    llx0, llx1, lly0, lly1 = Axes.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2  # centre the scale bar in the middle of the map
    sblly = lly0 + (lly1 - lly0) * location[1]
    tmc = ccrs.TransverseMercator(sbllx, sblly)

    x0, x1, y0, y1 = Axes.get_extent(tmc)  # retrieve the extent of the map in metres
    sbx = x0 + (x1 - x0) * location[0]  # plot the x location of the scale bar in metres on the map
    sby = y0 + (y1 - y0) * location[1]  # plot the y location of the scale bar in metres on the map

    if not length:
        length = (x1 - x0) / 5000  # calculate the length of the scale bar in km

    scaleb = [sbx - length * 500, sbx + length * 500]  
    axes.plot(scaleb, [sby, sby], transform=tmc, color='k', linewidth=linewidth)  # plot the scale bar on the map
    axes.text(sbx, sby, str(length) + ' km', transform=tmc,
              horizontalalignment='center', verticalalignment='bottom')  # plot the scale bar length and unit


scale_bar(Axes, 50)  # create a scale bar of 50 km


def generate_handles(label, colors, edge='k', alpha=1):
    # docstring
    # define legend library
    legendcolors = len(colors)  # get the length of the color list
    handle = []
    for i in range(len(label)):
        handle.append(patches.Rectangle((0, 0), 1, 1, facecolor=colors[i % legendcolors], edgecolor=edge, alpha=alpha))
    return handle

# ----------------------------------------------------------------------------------------------------------------------


def buffer_function(self, distance):
    """
    Applies a buffering function to the inputted dataset.

    :param self: the dataset to apply a buffer too
    :param distance: the selected buffer distance
    :return: the returned geometry buffers

    Typical usage:
    buffers = buffer_function(self, distance)
    """
    buffer = self.buffer(distance)
    return buffer


def conversion_function(self):
    """
    Converts a geoseries into a geodataframe.

    :param self: geoseries to be converted

    Typical usage:
    variable = conversion_function(geoseries)
    """
    conversion = gpd.GeoDataFrame(gpd.GeoSeries(self))  # convert the geoseries into a geodataframe
    # rename the geometry column from '0' to 'geometry'
    conversion = conversion.rename(columns={0: 'geometry'}).set_geometry('geometry')
    return conversion


# generate settlement buffers
Settlementbuffers = buffer_function(MSettlements, 10000)  # generate buffer around settlements with user defined distance
Settlementbuffers = conversion_function(Settlementbuffers)
Settlementbuffers.crs = 'epsg:27700'  # define the crs of the settlement buffers to epsg = 27700


# extract rivers that are outside the buffer zones
# select through difference where rivers do not overlay the buffers around settlements
RiverExtractOutsideSettlement = gpd.overlay(Watercourses, Settlementbuffers, how='difference', keep_geom_type=False)

# extract rivers that intersect with county polygons that are below a user defined threshold
PopDensitySelect = PopDens[PopDens['GB_dist__3'] > 360]  # select counties with a pop density above a certain threshold
# select rivers that lie outside of these counties
RiverExtractPopDens = gpd.overlay(RiverExtractOutsideSettlement, PopDensitySelect,
                                  how='difference', keep_geom_type=False)

# generate buffer around river lines
# generate a buffer around rivers outside of selected counties and distance from settlements
RiverBuffer = buffer_function(RiverExtractPopDens, 1000)
RiverBuffer = conversion_function(RiverBuffer)

# clip county polygons to those that lay within the river buffers
# select land that is within the river buffers
ViableLand = gpd.overlay(PopDens, RiverBuffer, how='intersection', keep_geom_type=False)
ViableLand = gpd.geoseries.GeoSeries([geom for geom in ViableLand.unary_union.geoms])  # merge land into one
ViableLand = conversion_function(ViableLand)

# ----------------------------------------------------------------------------------------------------------------------

# output elements to shapely features to be loaded into the figure:
AONB_features = ShapelyFeature(AONB['geometry'], CRS, edgecolor='k', facecolor='green')  # add AONB
NationalParks = ShapelyFeature(NationalP['geometry'], CRS, facecolor='darkseagreen', edgecolor='k')  # add national parks
CitiesAndTowns = ShapelyFeature(MSettlements['geometry'], CRS, edgecolor='k', facecolor='dimgrey')  # add settlements
CitiesAndTownsBuffer = ShapelyFeature(Settlementbuffers, CRS, edgecolor='k', alpha=0.5)  # add settlement buffers
Water_courses = ShapelyFeature(Watercourses['geometry'], CRS, edgecolor='b')  # add watercourses
ViableLandShp = ShapelyFeature(ViableLand['geometry'], CRS, edgecolor='k', facecolor='springgreen')
Water_coursesOS = ShapelyFeature(RiverExtractOutsideSettlement['geometry'], CRS, edgecolor='b')
RiverBufferShp = ShapelyFeature(RiverBuffer['geometry'], CRS, facecolor='b')


# define a colour bar for the pop density choropleth map
color_bar = m_ax(Axes)
cax = color_bar.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)
# add county polygons with graduation of colour for pop density
PopDens.plot(column='GB_dist__3', ax=Axes, vmin=50, vmax=1000, cax=cax, cmap='OrRd',
             legend=True, legend_kwds={'label': 'Population Density'})

# add features to the axes/figure
Axes.add_feature(CitiesAndTowns)
Axes.add_feature(ViableLandShp)
Axes.add_feature(Water_coursesOS)
Axes.add_feature(AONB_features)
Axes.add_feature(NationalParks)

# generate legend
corridor_handle = generate_handles(['Wildlife Corridors'], ['springgreen'])
river_handle = generate_handles(['Rivers'], ['b'])
settlement_handle = generate_handles(['Settlements'], ['dimgrey'])
NP_handle = generate_handles(['National Parks'], ['darkseagreen'])
AONB_handle = generate_handles(['AONB'], ['green'])

labels = ['Rivers', 'Wildlife Corridors', 'National Parks', 'AONB', 'Settlements']

handles = river_handle + corridor_handle + settlement_handle + AONB_handle + NP_handle
legend = Axes.legend(handles, labels, title='Legend', title_fontsize=11,
                     fontsize=8, loc='upper left', frameon=True, framealpha=1)

Figure.savefig('Test.png', dpi=300)  # output map figure of performed analysis in this script
