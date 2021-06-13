import folium   # pip install
import pandas as pd     # pip install
from geopy import Nominatim     # pip install
import codecs
import webbrowser
import os


# The documentation for folium - https://python-visualization.github.io/folium/


def generate_map():
    my_map = folium.Map(location=[53.9171, -122.7497], zoom_start=5)  # coordinates for Prince George

    coordinates = [  # coords for putting points on the map
        [42.3581, -71.0636],
        [42.82995815, -74.78991444],
        [43.17929819, -78.56603306],
        [43.40320216, -82.37774519],
        [43.49975489, -86.20965845],
        [43.46811941, -90.04569087],
        [43.30857071, -93.86961818],
        [43.02248456, -97.66563267],
        [42.61228259, -101.41886832],
        [42.08133868, -105.11585198],
        [41.4338549, -108.74485069],
        [40.67471747, -112.29609954],
        [39.8093434, -115.76190821],
        [38.84352776, -119.13665678],
        [37.7833, -122.4167]]

    coordinates2 = [  # coords for drawing lines, always from start point outwards
        [53.9171, -122.7497], [52.974800, -122.497849],
        [53.9171, -122.7497], [54.442500, -124.247530],
        [53.9171, -122.7497], [54.018349, -123.995628],
        [53.9171, -122.7497], [55.129040, -120.993874],
    ]

    coordinates3 = [
        [53.9171, -122.7497], [52.974800, -122.497849],
        [54.442500, -124.247530], [54.018349, -123.995628],
         [55.129040, -120.993874]
    ]

    folium.PolyLine(coordinates2, color='purple', weight=2.5).add_to(my_map)  # drawing lines based on the coordinates

    for each in coordinates:  # looping over coordinates to plot points on the map
        folium.Marker(each, popup='Line1\nLine2\nLine3', icon=folium.Icon(color='green', icon='map-marker')).add_to(my_map)

    tooltip = "Click me"    # this message will be seen while hovering over a marker that is put on the map

    # star marker for PG
    folium.Marker(location=[53.9171, -122.7497], popup='Line1\nLine2\nLine3', tooltip=tooltip, icon=folium.Icon(color='red', icon='star')).add_to(my_map)

    folium.LatLngPopup().add_to(my_map)  # adds popup when you left click on map you can see long and lat coordinates of anywhere
    my_map.save('THE_MAP.html')


def generate_map2():    # looking at different markers here
    m = folium.Map(location=[45.372, -121.6972], zoom_start=12, tiles='Stamen Terrain')
    tooltip = 'Click me!'

    folium.Marker(location=[45.3288, -121.6625], popup='Mt. Hood Meadows', tooltip=tooltip).add_to(m)
    folium.Marker(location=[45.3311, -121.7113], popup='Timberline Lodge', icon=folium.Icon(color='darkred', icon='fire')).add_to(m)
    folium.Marker(location=[45.3300, -121.6823], popup='Some Other Location', icon=folium.Icon(color='darkpurple', icon='star')).add_to(m)
    folium.Marker(location=[45.4311, -121.7113], popup='Timberline Lodge', icon=folium.Icon(color='blue', icon='record')).add_to(m)

    m.save('THE_MAP2.html')


def generate_map3():    # example using pandas to store then loop over everything stored
    # Make a data frame with dots to show on the map
    data = pd.DataFrame({
        'lat': [-58, 2, 145, 30.32, -4.03, -73.57, 36.82, -38.5],
        'lon': [-34, 49, -38, 59.93, 5.33, 45.52, -1.29, -12.97],
        'name': ['Buenos Aires', 'Paris', 'melbourne', 'St Petersbourg', 'Abidjan', 'Montreal', 'Nairobi', 'Salvador']
    })

    # Make an empty map
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Add markers one by one on the map
    for i in range(0, len(data)):
        folium.Marker([data.iloc[i]['lon'], data.iloc[i]['lat']], popup=data.iloc[i]['name']).add_to(m)

    m.save('THE_MAP3.html')


def generate_map4():

    geolocator = Nominatim(user_agent="CPSC473")

    inp = ["Prince George, British Columbia", "Vanderhoof, British Columbia", "Burns Lake, British Columbia"]       # test input - one path
    spread_path = []    # this will hold spread path coordinates for plotting the line

    start_point_name = inp[0]    # index 0 is always starting point on the map
    inp.pop(0)      # remove from list

    initial_geoloc = geolocator.geocode(start_point_name, timeout=10)    # get initial geolocation for starting point

    # getting initial starting point latitude and longitude
    init_lat = initial_geoloc.latitude
    init_long = initial_geoloc.longitude

    tooltip = "Click for more information!"    # this message will show when hovering over markers put on the map

    m = folium.Map(location=[init_lat, init_long], zoom_start=7)  # set the starting point for the map at starting location
    # put down initial marker for start point
    folium.Marker(location=[init_lat, init_long], tooltip=tooltip, popup=start_point_name, icon=folium.Icon(color='darkpurple', icon='star')).add_to(m)

    spread_path.append([init_lat, init_long])

    for i in range(len(inp)):   # loop through rest of the cities
        geoloc = geolocator.geocode(inp[i], timeout=10)
        lat = geoloc.latitude
        long = geoloc.longitude
        spread_path.append([lat, long])
        folium.Marker([lat, long], popup=inp[i], tooltip=tooltip, icon=folium.Icon(color='orange', icon='map-marker')).add_to(m)

    folium.PolyLine(spread_path, color='red', weight=2.5).add_to(m)
    m.save('THE_MAP4.html')


def generate_map5():
    inp = [
        [(('Kitimat', 'British Columbia'), 'B.C.’s COVID-19 transmission remains high with 737 new cases – Kitimat Northern Sentinel'), (('Vanderhoof', 'British Columbia'), 'B.C.’s COVID-19 transmission remains high with 737 new cases – Vanderhoof Omineca Express'), (('Terrace', 'British Columbia'), 'B.C.’s COVID-19 transmission remains high with 737 new cases – Terrace Standard'), (('Houston', 'British Columbia'), 'B.C.’s COVID-19 transmission remains high with 737 new cases – Houston Today'), (('Burns Lake', 'British Columbia'), 'B.C.’s COVID-19 transmission remains high with 737 new cases – Burns Lake Lakes District News'), (('Houston', 'British Columbia'), 'B.C.’s COVID-19 transmission remains high with 737 new cases – Houston Today'), (('Prince Rupert', 'British Columbia'), 'B.C.’s COVID-19 transmission remains high with 737 new cases – Prince Rupert Northern View'), (('Smithers', 'British Columbia'), 'B.C.’s COVID-19 transmission remains high with 737 new cases – Smithers Interior News')],
        [(('Kitimat', 'British Columbia'), 'B.C.’s specialized COVID paramedics ‘impressed’ with Fort St. James’ community response – Kitimat Northern Sentinel'), (('Smithers', 'British Columbia'), 'B.C.’s specialized COVID paramedics ‘impressed’ with Fort St. James’ community response – Smithers Interior News'), (('Vanderhoof', 'British Columbia'), 'B.C.’s specialized COVID paramedics ‘impressed’ with Fort St. James’ community response – Vanderhoof Omineca Express'), (('Houston', 'British Columbia'), 'B.C.’s specialized COVID paramedics ‘impressed’ with Fort St. James’ community response – Houston Today'), (('Burns Lake', 'British Columbia'), 'B.C.’s specialized COVID paramedics ‘impressed’ with Fort St. James’ community response – Burns Lake Lakes District News'), (('Terrace', 'British Columbia'), 'B.C.’s specialized COVID paramedics ‘impressed’ with Fort St. James’ community response – Terrace Standard'), (('Houston', 'British Columbia'), 'B.C.’s specialized COVID paramedics ‘impressed’ with Fort St. James’ community response – Houston Today'), (('Prince Rupert', 'British Columbia'), 'B.C.’s specialized COVID paramedics ‘impressed’ with Fort St. James’ community response – Prince Rupert Northern View')],
        [(('Kitimat', 'British Columbia'), 'Canopy Growth to close 5 facilities across Canada, lay off 220 workers'), (('Smithers', 'British Columbia'), 'Canopy Growth to close 5 facilities across Canada, lay off 220 workers'), (('Vanderhoof', 'British Columbia'), 'Canopy Growth to close 5 facilities across Canada, lay off 220 workers'), (('Houston', 'British Columbia'), 'Canopy Growth to close 5 facilities across Canada, lay off 220 workers'), (('Burns Lake', 'British Columbia'), 'Canopy Growth to close 5 facilities across Canada, lay off 220 workers'), (('Terrace', 'British Columbia'), 'Canopy Growth to close 5 facilities across Canada, lay off 220 workers'), (('Houston', 'British Columbia'), 'Canopy Growth to close 5 facilities across Canada, lay off 220 workers'), (('Prince Rupert', 'British Columbia'), 'Canopy Growth to close 5 facilities across Canada, lay off 220 workers')],
        [(('Kitimat', 'British Columbia'), 'Active marine oil slick near Nootka Sound tied to historic 1968 Bligh Island shipwreck – Kitimat Northern Sentinel'), (('Smithers', 'British Columbia'), 'Active marine oil slick near Nootka Sound tied to historic 1968 Bligh Island shipwreck – Smithers Interior News'), (('Vanderhoof', 'British Columbia'), 'Active marine oil slick near Nootka Sound tied to historic 1968 Bligh Island shipwreck – Vanderhoof Omineca Express'), (('Houston', 'British Columbia'), 'Active marine oil slick near Nootka Sound tied to historic 1968 Bligh Island shipwreck – Houston Today'), (('Burns Lake', 'British Columbia'), 'Active marine oil slick near Nootka Sound tied to historic 1968 Bligh Island shipwreck – Burns Lake Lakes District News'), (('Terrace', 'British Columbia'), 'Active marine oil slick near Nootka Sound tied to historic 1968 Bligh Island shipwreck – Terrace Standard'), (('Houston', 'British Columbia'), 'Active marine oil slick near Nootka Sound tied to historic 1968 Bligh Island shipwreck – Houston Today'), (('Prince Rupert', 'British Columbia'), 'Active marine oil slick near Nootka Sound tied to historic 1968 Bligh Island shipwreck – Prince Rupert Northern View')]
    ]
    geolocator = Nominatim(user_agent="CPSC473")
    tooltip = "Click for more information!"
    for x in range(len(inp)):
        inputs = inp[x]
        origin = inp[x][0][0]
        initial_geoloc = geolocator.geocode(origin, timeout=10)
        big_lat = initial_geoloc.latitude
        big_long = initial_geoloc.longitude
        m = folium.Map(location=[big_lat, big_long], zoom_start=7)
        folium.Marker(location=[big_lat, big_long], tooltip=tooltip, popup=initial_geoloc,
                      icon=folium.Icon(color='darkpurple', icon='star')).add_to(m)
        all_coordinates = []
        #all_coordinates.append([init_lat,init_long])
        for x, i  in (inputs):
            initial_geoloc = geolocator.geocode((x), timeout=10)
            init_lat = initial_geoloc.latitude
            init_long = initial_geoloc.longitude
            long_lat = [init_lat, init_long]
            all_coordinates.append(long_lat)
            all_coordinates.append([big_lat,big_long])
        print(all_coordinates)

def open_map():     # opens the generated map automatically

    file_name = 'file:///' + os.getcwd() + '/' + 'THE_MAP4.html'
    webbrowser.open_new_tab(file_name)


if __name__ == '__main__':
    generate_map()
    # generate_map2()
    # generate_map3()
    # generate_map4()
    generate_map5()
    # open_map()
