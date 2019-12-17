import matplotlib.pyplot as plt 
import cartopy
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import pandas as pd

import random
import time

plt.ion()

# ax = plt.axes(projection = ccrs.PlateCarree())
# ax.stock_img()

# ny_lon, ny_lat = -75, 43
# delhi_lon, delhi_lat = 77.23, 28.61
# plt.show()

def epyGo(num):
    for i in range(num):
        x = random.randint(-90, 90)
        y = random.randint(-180, 180)
        infected = bool(random.getrandbits(1))
        if infected:
            plt.scatter(x, y, color = "red" , marker='o', transform=ccrs.Geodetic())
        plt.pause(0.5)



def plot_countries(df,projection,colors,annotation,title,edgecolor):

    ax = plt.axes(projection=projection)
    ax.add_feature(cartopy.feature.OCEAN, facecolor='white')
    ax.outline_patch.set_edgecolor(edgecolor)

    shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural',
                                          name='admin_0_countries')
    reader = shpreader.Reader(shpfilename)
    countries = reader.records()
    values = list(df[title].unique())

    for country in countries:
        attribute = 'ADM0_A3'
        ADM0_A3 = country.attributes['ADM0_A3']

        # get classification
        try:
            classification = df.loc[country.attributes[attribute]][title]
        except:
            pass

        ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                          facecolor=(colors[values.index(classification)]),
                          label=country.attributes[attribute],
                          edgecolor='#FFFFFF',
                          linewidth=.25)

    # legend
    import matplotlib.patches as mpatches
    handles = []
    for i in range(len(values)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i]))
        plt.legend(handles, values,
                   loc='lower left', bbox_to_anchor=(0.025, -0.0), 
                   fancybox=True, frameon=False, fontsize=5)

    # annotate
    ax.annotate(annotation, xy=(0, 0),  xycoords='figure fraction',
            xytext=(0.0275, -0.025), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='center', fontsize=4,
            )

    plt.title(title, fontsize=8)

    title = 'maps/'+title+'.png'
    plt.savefig(title, bbox_inches='tight', pad_inches=.2, dpi=300)
    print('Saved: {}'.format(title))


def main():
    df = pd.read_csv('countries.csv', index_col='ISO_CODE')

    projection = ccrs.Robinson()
    title = 'Four Regions With The Same Population'
    colors = ['#f4b042', '#92D050','#71a2d6','#b282ac','#DDDDDD']
    #colors = ['#orange' ,'#green','#blue ','#purple','#grey  ']
    annotation = 'Four Regions With The Same Population: https://mapchart.net/showcase.html'
    plot_countries(df,projection,colors,annotation,title,edgecolor='white')

    projection = ccrs.Orthographic(-30,40)
    colors = ['#71a2d6','#DDDDDD']
    annotation = 'NATO Member Countries: https://en.wikipedia.org/wiki/Member_states_of_NATO'
    title = 'NATO Members'
    plot_countries(df,projection,colors,annotation,title,edgecolor='grey')

    projection = ccrs.Orthographic(10,50)
    colors = ['#000099','#DDDDDD']
    annotation = 'EU Member Countries: https://en.wikipedia.org/wiki/Member_state_of_the_European_Union'
    title = 'EU Members'
    plot_countries(df,projection,colors,annotation,title,edgecolor='grey')

    print('Done.\n')



if __name__ == '__main__':
    main()








































































def main1():
    # df = pd.read_csv('states.csv')
    df = pd.read_csv('states.csv', index_col='State')

    # States Visited
    projection = ccrs.LambertConformal()
    title = 'States Visited'
    colors = ['#71a2d6','#DDDDDD']
    annotation = ''
    plot_states(df,projection,colors,annotation,title,edgecolor='white')

    # 13 Original Colonies
    projection = ccrs.LambertConformal()
    title = '13 Original Colonies'
    colors = ['#DDDDDD','#71a2d6']
    annotation = ''
    plot_states(df,projection,colors,annotation,title,edgecolor='white')

    print('Done.\n')




def plot_states(df,projection,colors,annotation,title,edgecolor):

    ax = plt.axes([0, 0, 1, 1],
                  projection=projection)
    ax.background_patch.set_visible(False)
    ax.outline_patch.set_visible(False)
    ax.set_extent([-125, -66.5, 20, 50], ccrs.Geodetic())

    shapename = 'admin_1_states_provinces_lakes_shp'
    shpfilename = shpreader.natural_earth(resolution='110m',
                                         category='cultural', name=shapename)

    reader = shpreader.Reader(shpfilename)
    states = reader.records()
    values = list(df[title].unique())


    for state in states:
        attribute = 'name'
        name = state.attributes[attribute]

        # get classification
        try:
            classification = df.loc[state.attributes[attribute]][title]
        except:
            pass

        ax.add_geometries(state.geometry, ccrs.PlateCarree(),
                          facecolor=(colors[values.index(classification)]),
                          label=state.attributes[attribute],
                          edgecolor='#FFFFFF',
                          linewidth=.25)

    # legend
    import matplotlib.patches as mpatches
    handles = []
    for i in range(len(values)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i]))
        plt.legend(handles, values,
                   loc='lower left', bbox_to_anchor=(0.025, -0.0), 
                   fancybox=True, frameon=False, fontsize=5)

    # annotate
    ax.annotate(annotation, xy=(0, 0),  xycoords='figure fraction',
            xytext=(0.0275, -0.025), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='center', fontsize=4,
            )

    plt.title(title, fontsize=8)

    title = title+'.png'
    plt.savefig(title, bbox_inches='tight', pad_inches=.2, dpi=300)
    print('Saved: {}'.format(title))