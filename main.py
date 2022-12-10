app_version = "v09"
# put the name of this python file in txt file for processing by other scripts
with open("_current_app_version.txt", "w") as version_file:
    version_file.write(app_version + "\n")

# import datetime
import json
import os
import sys
import socket

import numpy as np
import pandas as pd
from datetime import datetime
import pytz
from numpy import nan

import urllib3
# info:  https://urllib3.readthedocs.io/en/latest/user-guide.html#response-content
#        https://urllib3.readthedocs.io/en/latest/user-guide.html#headers

import certifi

import dash
import plotly
from dash import Dash, html, dcc, Input, Output, State
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from figures.configs import default_modebar
from figures.graphs import radar_sensor_px_static, mapbox_px_static2, mapbox_go_static
from layouts import rows
from layouts.header import build_header
from layouts.footer import build_footer
from config.locations import sensor_locations
from config import strings
from utils import geo_mapbox

test_set = { 
          1: {"start": '2022-09-28 08:50:00',  # used in TEST1
              "end": '2022-09-28 09:15:00'},
    
          2: {"start": '2022-09-28 08:00:00',  # used in  TEST1
              "end": '2022-09-28 12:00:00'},

          3: {"start": '2022-09-28 08:13:00',  # used in  TEST1
              "end": '2022-09-28 09:05:00'},

          9: {"start": '2022-09-29 12:11:00',  # used in TEST1 # LET OP , deze heeft geen schipsdata !!
              "end": '2022-09-29 12:28:20'},

          10: {"start": '2022-10-21 11:25:00',  # Deze heeft aanvaring
               "end": '2022-10-21 11:55:00'},

          11: {"start": '2022-10-21 11:33:00',  # Deze heeft aanvaring
               "end": '2022-10-21 11:45:00'},

          20: {"start": '2022-10-20 13:50:00',  # Nog geen scheepsdata
               "end": '2022-10-20 14:00:00'},
}

# debugging
export_to_csv = False
test = 11
verbose = True

# system info
the_hostname = socket.gethostname()

run_on = os.getenv("RUN_LOCATION", "local")
if run_on.lower() in ["heroku"]:
    verbose = False

python_version = sys.version.split()[0]
dash_version = dash.__version__
plotly_version = plotly.__version__


def create_marks_items(df, column_name):  # define datetime markers for the dynamic slider

    unique_dt_list = list(df[column_name].unique())

    items = {}
    i = 1

    for unique_dt in unique_dt_list:
        items[i] = {'label': unique_dt[0:19],
                    'style': {'color': 'black',
                              'writing-mode': 'vertical-rl',  # make sure that datetime is readable 
                              'font-size': '10px',
                              'height': '18em'  # text is 19 chars
                                                # https://www.w3schools.com/cssref/css_units.asp
                              }
                    }
        i = i + 1

    return items


def sensordata_to_df_10S(data_dir, data_file, position, csv_export):
    # load sensor data from file and set the index to datetime in UTC and resample per 10 sec
    with open(data_dir + data_file, 'r') as jsonf:
        sensor_data = json.load(jsonf)

    unitdivider = 1  # measurement in meters
    if sensor_data['data']['meas_unit'] == 'centimeter':
        unitdivider = 100
        
    sensor_unit = sensor_data['data']['reference']
    print(sensor_unit)
    # print(sensor_data['data']['values'])

    return_df = pd.DataFrame(sensor_data['data']['values'], columns=['epoch_UTC', 'afstand_' + str(position)])

    # set distance in meters and round distance to 1 decimal
    return_df['afstand_' + str(position)] = return_df['afstand_' + str(position)]/unitdivider
    return_df['afstand_' + str(position)] = return_df['afstand_' + str(position)].round(1)

    # set generic datetime columns
    return_df['dt_UTC'] = pd.to_datetime(return_df['epoch_UTC'], unit='ms')
    return_df['dt_UTC'] = return_df['dt_UTC'].dt.tz_localize('UTC')

    # now we can drop the epoch_UTC column as it is not needed anymore
    return_df.drop(columns='epoch_UTC', inplace=True)
    
    # set index to datetime column
    return_df.set_index('dt_UTC', inplace=True)

    # setting the uniform datetime interval and using the minimum value 
    return_df = return_df.resample('10S').min()

    # add same values until new value; this ensures that there will always be a value present for all timestamps
    return_df.interpolate(method="pad", inplace=True)

#   # Kept for future reference
#   # now we need to (re)create the epoch_UTC colum with the correct epoch value (which is present in the index)
#   return_df['epoch_UTC'] = return_df.index.astype(np.int64) // 10**6

    return_df['afstand_' + str(position)] = return_df['afstand_' + str(position)].astype(str)
    return_df.loc[return_df['afstand_' + str(position)] == '-999.0', 'afstand_' + str(position)] = 'error'
    
    if csv_export:
        return_df.to_csv("sensor" + str(position) + "_data_df.csv")
    
    # index of returned df should always be datetime column in UTC format and value is string format
    return return_df


def locationdata_to_df_file(data_dir, data_file, csv_export):
    # load location data from file and set the index to datetime in UTC
    return_df = pd.read_csv(data_dir + data_file,
                            usecols=['balenaAISmessageUTC_str', 'mmsi',
                                     'AIS_lat', 'AIS_lon', 'AIS_course', 'AIS_speed'])

    return_df['dt_UTC'] = pd.to_datetime(return_df['balenaAISmessageUTC_str'], format='%Y-%m-%dT%H:%M:%S')

    # set index to datetime column
    return_df.set_index('dt_UTC', inplace=True)

    if csv_export:
        return_df.to_csv("location_data_df.csv")

    # index of returned df should always be datetime column in UTC format
    return return_df


# def mmsi_shipsname_to_df_file(data_dir, data_file, csv_export):
#     # load mmsi and shipsname from file
#     return_df = pd.read_excel(data_dir + data_file, )
#                             #usecols=['alenaAISmessageUTC_str', 'mmsi', 'AIS_lat', 'AIS_lon', 'AIS_course', 'AIS_speed'])
#     #print(return_df.columns)
#
#     if csv_export:
#         return_df.to_csv("mmsi_shipsname_data_df_file.csv")
#
#     return return_df


def mmsi_shipsname_to_df_api(list_of_mmsi, csv_export):
    return_df = pd.DataFrame(columns=['mmsi', 'naam'])

    http_object = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )

    for an_mmsi in list_of_mmsi:
        # print(a_mmsi)
        url = 'https://j3dw753lq3.execute-api.eu-central-1.amazonaws.com/v2/info/mmsi/' + str(an_mmsi)
        req = http_object.request(method='GET',
                                  url=url
                                  )

        values = json.loads(req.data)
        if values["Count"] == 1:
            add_row = {'mmsi': an_mmsi, 'naam': values["Items"][0]['AIS_shipname']['S']}
        elif values["Count"] > 1:
            # use the first item in the list
            add_row = {'mmsi': an_mmsi, 'naam': values["Items"][0]['AIS_shipname']['S']}
        else:
            # mmsi not found in database
            add_row = {'mmsi': an_mmsi, 'naam': "U_" + a_mmsi}

        # print(values["Items"][0]['AIS_shipname']['S'])

        # add_row = {'mmsi': an_mmsi, 'naam': values["Items"][0]['AIS_shipname']['S']}
        return_df = return_df.append(add_row, ignore_index=True)

    if csv_export:
        return_df.to_csv("mmsi_shipsname_data_df_api.csv")
    
    return return_df

####################################################
# DEFINE GENERICALLY USED VARS
####################################################
# set environment
localtz_str = 'Europe/Amsterdam'
tz = pytz.timezone(localtz_str)

mapbox_access_token = "pk.eyJ1IjoicGllcnJldmVlbGVuIiwiYSI6ImNra3V6Z2JhNTFjeXUycHBjdWVkOXUxdDMifQ.tzOHbTKha9Co8-s_AarPJg"  # token from pierre@ipheion.eu


##################################
# START MOMENT
print('Start moment')
start_time_local = test_set[test]["start"]

print('local start moment                :', start_time_local)
naive_dt = datetime.strptime(start_time_local, '%Y-%m-%d %H:%M:%S')
local_dt = tz.normalize(tz.localize(naive_dt))
print('local start moment with timezone  :', local_dt)
print('local start moment timestamp/epoch:', local_dt.timestamp()*1000)
start_epoch_UTC_ms = local_dt.timestamp()*1000

start_dt_utc = local_dt.astimezone(pytz.utc)
start_dt_utc_str = start_dt_utc.strftime('%Y-%m-%dT%H:%M:%S')
print('UTC start moment                  :', start_dt_utc_str)

# END MOMENT
print('End moment')
end_time_local = test_set[test]["end"]

print('local end moment                  :', end_time_local)
naive_dt = datetime.strptime(end_time_local, '%Y-%m-%d %H:%M:%S')
local_dt = tz.normalize(tz.localize(naive_dt))
print('local end moment with timezone    :', local_dt)
print('local end moment timestamp/epoch  :', local_dt.timestamp()*1000)
end_epoch_UTC_ms = local_dt.timestamp()*1000

end_dt_utc = local_dt.astimezone(pytz.utc)
end_dt_utc_str = end_dt_utc.strftime('%Y-%m-%dT%H:%M:%S')
print('UTC end moment                    :', end_dt_utc_str)
####################################################


####################################################
# RETRIEVE SHIPSLOCATIONS DATASET(S)
####################################################
print("retrieving ships location data")
ships_df = locationdata_to_df_file("./00_retrieve/AIS_data_from_DDB_geohash/", 'data_from_ddb.csv', export_to_csv)

print("retrieving ships names")
mmsi_list = list(ships_df['mmsi'].unique()) 
names_df = mmsi_shipsname_to_df_api(mmsi_list, export_to_csv)  # not working yet

# names_df = mmsi_shipsname_to_df_file("./data/final/", "ship_info.xlsx", export_to_csv)

# display(names_df)


####################################################
# FILTER SHIPSLOCATIONS DATASET(S)
####################################################
# filter data based on UTC datetime
print("filtering ships location data")
ships_subset_df = ships_df[(ships_df['balenaAISmessageUTC_str'] >= start_dt_utc_str) & (ships_df['balenaAISmessageUTC_str'] <= end_dt_utc_str)].copy()
# display(ships_subset_df.head(5))

# setting the uniform datetime interval for ships location subset
ships_subset_df = ships_subset_df.groupby('mmsi').resample('10S').mean()
ships_subset_df.drop(columns=['mmsi'], inplace=True)

ships_subset_df.interpolate(method="linear", inplace=True)
ships_subset_df['AIS_speed'] = ships_subset_df['AIS_speed'].round(1)
ships_subset_df['AIS_lat'] = ships_subset_df['AIS_lat'].round(7)
ships_subset_df['AIS_lon'] = ships_subset_df['AIS_lon'].round(7)

# display(ships_subset_df.head(5))

# the inverse of groupby, reset_index
ships_subset_df.reset_index(inplace=True)
# display(ships_subset_df.head(5))

# set timestamp as index again
ships_subset_df.set_index("dt_UTC", inplace=True, drop=True)
# display(ships_subset_df.head(5))

ships_subset_df['dt_local'] = ships_subset_df.index
ships_subset_df['dt_local'] = ships_subset_df['dt_local'].dt.tz_localize('UTC')
ships_subset_df['dt_local_str'] = ships_subset_df['dt_local'].dt.tz_convert(localtz_str).dt.strftime('%Y-%m-%d %h:%m:%s')

# remove added NaN rows 
ships_subset_df.dropna(inplace=True)

# add the ships names
ships_subset_df = ships_subset_df.merge(names_df[['mmsi', 'naam']], how='left', on='mmsi')

# if shipsname not known use U_<mmsi> instead
ships_subset_df.loc[ships_subset_df['naam'].isna(), 'naam'] = "U_" + ships_subset_df['mmsi'].astype(str)

# display(ships_subset_df.head(5))

if export_to_csv:
    ships_subset_df.to_csv("ships_subset_df.csv")


####################################################
# RETRIEVE SENSOR DATASET(S)
####################################################
print("retrieving sensor data")

# add kast_1_radar
# ================
sensor1_radar_df = sensordata_to_df_10S("./00_retrieve/Sensor_data/", "kast_1_radar.json", 1, export_to_csv)

# add kast_2_radar
# ================
sensor2_radar_df = sensordata_to_df_10S("./00_retrieve/Sensor_data/", "kast_2_radar.json", 2, export_to_csv)

# add kast_3_radar
# ================
sensor3_radar_df = sensordata_to_df_10S("./00_retrieve/Sensor_data/", "kast_3_radar.json", 3, export_to_csv)

# add kast_4_radar
# ================
sensor4_radar_df = sensordata_to_df_10S("./00_retrieve/Sensor_data/", "kast_4_radar.json", 4, export_to_csv)

# add kast_5_radar
# ================
sensor5_radar_df = sensordata_to_df_10S("./00_retrieve/Sensor_data/", "kast_5_radar.json", 5, export_to_csv)

# add kast_6_radar
# ================
sensor6_radar_df = sensordata_to_df_10S("./00_retrieve/Sensor_data/", "kast_6_radar.json", 6, export_to_csv)

# add kast_7_radar
# ================
sensor7_radar_df = sensordata_to_df_10S("./00_retrieve/Sensor_data/", "kast_7_radar.json", 7, export_to_csv)

# add kast_8_radar
# ================
sensor8_radar_df = sensordata_to_df_10S("./00_retrieve/Sensor_data/", "kast_8_radar.json", 8, export_to_csv)

# add kast_9_radar
# ================
sensor9_radar_df = sensordata_to_df_10S("./00_retrieve/Sensor_data/", "kast_9_radar.json", 9, export_to_csv)

####################################################
# COMBINE SENSOR DATASET(S)
####################################################
print("combining sensor data")
sensor_data_df = pd.concat([sensor1_radar_df,
                            sensor2_radar_df,
                            sensor3_radar_df,
                            sensor4_radar_df,
                            sensor5_radar_df,
                            sensor6_radar_df,
                            sensor7_radar_df,
                            sensor8_radar_df,
                            sensor9_radar_df], axis=1, join="inner")


print("filtering sensor data")
sensor_data_subset_df = sensor_data_df[(sensor_data_df.index >= start_dt_utc) & (sensor_data_df.index <= end_dt_utc)].copy()

sensor_data_subset_df.sort_index(inplace=True)

if export_to_csv:
    sensor_data_subset_df.to_csv("display_df_filtered.csv")

print("melting dataframes")
df_to_melt = sensor_data_subset_df[['afstand_1', 'afstand_2', 'afstand_3', 'afstand_4', 'afstand_5',
                                    'afstand_6', 'afstand_7', 'afstand_8', 'afstand_9']].copy()
if export_to_csv:
    df_to_melt.to_csv("df_to_melt.csv")

melted_df = df_to_melt.melt(ignore_index=False, var_name='sensor', value_name='afstand')
melted_df.sort_index(inplace=True)

melted_df['dt_local_str'] = melted_df.index.tz_convert(localtz_str).strftime('%Y-%m-%d %h:%m:%s')

melted_df['x'] = melted_df['sensor']
melted_df['x'].replace({'afstand_1': 1,
                        'afstand_2': 2,
                        'afstand_3': 3,
                        'afstand_4': 4,
                        'afstand_5': 5,
                        'afstand_6': 6,
                        'afstand_7': 7,
                        'afstand_8': 8,
                        'afstand_9': 9
                        }, inplace=True)

# set error text in sensor 
melted_df.loc[melted_df['afstand'] == 'error', 'sensor'] = "Measurement Error"
melted_df.loc[melted_df['afstand'] == 'error', 'afstand'] = np.nan  # show nothing in graph

melted_df['afstand'] = melted_df['afstand'].astype(float).round(1)

if export_to_csv:
    melted_df.to_csv("melted_df.csv")


####################################################
# DEFINE GLOBAL VARS FOR GRAPHS
####################################################
# mapbox
# glb_calc_center = {"lon": 5.7799, "lat": 51.0125}  # some decent manualy found values
# glb_calc_zoom = 13.2

# set the zoom level to show all points on the map
glb_calc_zoom, glb_calc_center = geo_mapbox.zoom_center(
    lons=ships_subset_df['AIS_lon'],
    lats=ships_subset_df['AIS_lat']
)

# automated marker
glb_marker_start = 0  # create an empty marker at the start position
glb_marker_end = 1  # and an empty marker at the end (this value is changed at later stage when marker dict is filled)

glb_current_mark_index = 1  # start at this position with the data

# timer interval 
glb_interval_time_ms = 1000  # interval time in mili sec

# ToDo:
# Create datetime marker based on which dataframe? Now using the radarsensors dataset
# Or should we used the first and last date of any dataframe?

marks_items = create_marks_items(melted_df, 'dt_local_str')
glb_marker_end = len(marks_items) + 1  # and an empty marker at the end


####################################################
# ADD VISUALISATION DATA TO SHIPSLOCATIONS DATASET(S)
####################################################

# - set index to numerical instead of datetime
ships_subset_df.reset_index(inplace=True, drop=True)

# # - create a speed colum which will be used for size on the map
# min_size = 3  # min size of point on map in px
# speed_factor = 1 # factor to multiply the AIS speed by
# ships_subset_df["updated_speed"] = ships_subset_df["AIS_speed"] * speed_factor + min_size

# - finaly sort the index
ships_subset_df.sort_index(inplace=True)

# ADD A COLOR TO A MSSI / THE SHIP
# ================================

# https://sashamaps.net/docs/resources/20-colors/
color_list20 = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231',
                '#911eb4', '#216a7a', '#f032e6', '#bfef45', '#fabed4',
                '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000',
                '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9']

ships_subset_df['shipscolor'] = ""

unique_mmsi_list = ships_subset_df['mmsi'].unique()

colorindex = 0
for a_mmsi in unique_mmsi_list:
    if colorindex == len(color_list20):
        colorindex = 0
    ships_subset_df.loc[ships_subset_df['mmsi'] == a_mmsi, 'shipscolor'] = color_list20[colorindex]
    colorindex = colorindex + 1


####################################################
# ADD VISUALISATION DATA TO SENSOR DATASET(S)
####################################################
# - set index to numerical instead of datetime so we can easily get specific datapoint for visualisation
melted_df.reset_index(inplace=True, drop=True)

# - set the alerting levels
melted_df['alert'] = "rest"  # default setting
melted_df.loc[melted_df['afstand'] < 20, 'alert'] = 'no-alert'
melted_df.loc[melted_df['afstand'] < 10, 'alert'] = 'alert'
melted_df.loc[melted_df['afstand'] < 5, 'alert'] = 'major-alert'
melted_df.loc[melted_df['afstand'] == 0, 'alert'] = 'rest'

# - add lat and lon info to df
melted_df['sensor_lat'] = 0
melted_df['sensor_lon'] = 0
melted_df['unit'] = 0

for sensor_location in sensor_locations:
    melted_df.loc[melted_df['sensor'] == sensor_location, 'sensor_lat'] = sensor_locations[sensor_location]['lat']
    melted_df.loc[melted_df['sensor'] == sensor_location, 'sensor_lon'] = sensor_locations[sensor_location]['lon']
    melted_df.loc[melted_df['sensor'] == sensor_location, 'unit'] = sensor_locations[sensor_location]['unit']


# - finaly sort the index
melted_df.sort_index(inplace=True, ignore_index=True)  # #####

if export_to_csv:
    melted_df.to_csv("melted_df_visuals.csv")


####################################################
# APP DEFINITIONS
####################################################
external_stylesheets = [
    # https://bootswatch.com/zephyr/
    dbc.themes.ZEPHYR,
    # For Bootstrap Icons...
    dbc.icons.BOOTSTRAP
]

app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=external_stylesheets,
)
app.title = "Ipheion Demo Dashboard"
app.config['update_title'] = '.. Renewing ..'

# app.config["suppress_callback_exceptions"] = True  # default is False
# suppress_callback_exceptions: check callbacks to ensure referenced IDs exist and props are valid.
# Set to True if your layout is dynamic, to bypass these checks.

if the_hostname != "LEGION-2020":
    server = app.server  # required for Heroku

app.layout = html.Div(
    [
        # CREATE DATA STORE IN WEBBROWSER
        # ===============================
        # IMPORTANT: Data stored is either json formatted or string.
        # ----------
        # Create place to store data used between callbacks
        # https://dash.plotly.com/dash-core-components/store#store-properties
        #
        # storage_type:
        # 'memory': only kept in memory, reset on page refresh
        #
        dcc.Store(id='all-ships-locations-dataset-json',
                  storage_type='memory'),  # only kept in memory, reset on page refresh
        dcc.Store(id='all-sensordata-datasets-json',
                  storage_type='memory'),  # only kept in memory, reset on page refresh

        # TOP ROW / HEADER ROW
        # =======================
        # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
        build_header(
            title_str=strings.HEADER_TITLE,
            version_str=app_version
        ),

        # CENTER ROWS / CONTENT ROWS
        # ==========================
        html.Div(
            [
                rows.settings_slider_for_timinginterval(
                    unique_id_name='set_data_point_interval',
                    interval_ms=glb_interval_time_ms,
                    pre_text="",
                    post_text=""
                ),
            ],
            style={'width': '80%'}

        ),

        html.Div(
            [
                html.P(f"Delay value: {int(glb_interval_time_ms)}" + " mili sec"),
            ],
            id='show-selected-delay-value',
            style={"padding": "20px"}
        ),

        # html.Div(
        #     [
        #         html.P(f"Current Local Date Time: {marks_items[glb_current_mark_index]['label']}"),
        #     ],
        #     id='latest-timestamp',
        #     style={"padding": "20px"}
        # ),

        html.Div(
            [
                rows.updating_images(
                    unique_id_name='images_to_view',
                    img_left='../assets/video_to_pic/BLACKSCREEN.png',
                    img_right='../assets/video_to_pic/BLACKSCREEN.png',
                    pre_text="",
                    post_text=""
                ),
            ],
            style={'width': '100%'}

        ),

        html.Div(
            [
                # dcc.Loading(
                #     id="loading-map",
                #     type="default",
                #     children=[
                        rows.ships_locations_on_map(
                            unique_id_name="my_ships_locations",
                            config_dict=default_modebar(save_to_filename="ships_locations"),
                            figure_dict=mapbox_go_static(ships_df=ships_subset_df,
                                                         sensors_df=melted_df,
                                                         center_value=glb_calc_center,
                                                         zoom_value=glb_calc_zoom,
                                                         map_rotation=-62,
                                                         token=mapbox_access_token
                                                         ),
                            pre_text=f"Current Local Date Time: {marks_items[glb_current_mark_index]['label']}",
                            post_text=""
                        ),
                    # ],
                # ),

            ],
        ),

        html.Div(
            [
                rows.play_buttons(
                    unique_id_name="my_buttons"
                ),

                rows.automated_slider(
                    unique_id_name="my_automation",
                    marker_start=glb_marker_start,
                    marker_end=glb_marker_end,
                    marker_items=marks_items,
                    marker_value=glb_current_mark_index
                ),
            ],
            # https://community.plotly.com/t/slider-height-seems-to-be-zero/6745
            # styling to that markers text can be shown completely
            style={'height': '12em',
                   'width': '100%',
                   'display': 'inline-block'}

        ),

        html.Div(
            [
                rows.radar_distance_in_graph(
                    unique_id_name="radar_sensor_px_static",
                    config_dict=default_modebar(save_to_filename="radar_distance"),
                    figure_dict=radar_sensor_px_static(df=melted_df),  # ToDo with what dataframe to start !!
                    pre_text="",
                    post_text=""
                ),
            ],
        ),

        # BOTTOM ROW / FOOTER ROW
        # ======================
        build_footer(),

        # https://dash.plotly.com/dash-core-components/interval
        # the wait timer
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,
            n_intervals=0,
            disabled=False,
        ),
    ]
)


####################################################
# SET GRAPHS REFRESH RATE
####################################################
@app.callback(
    # Where the results of the function end up
    # =======================================
    Output('interval-component', 'interval'),

    # Changes in (one of) these fires this callback
    # =============================================
    Input('set_data_point_interval', 'value')  # when slider for interval time is changed
)     
def set_graphs_refresh_rate(i_value):
    # updates the interval time
    
    # value is in sec's
    # glb_interval_time_ms is in mili sec's
    global glb_interval_time_ms
    
    glb_interval_time_ms = i_value * 1000 
    
    return glb_interval_time_ms 


####################################################
# PAUSE BUTTON CLICKED
####################################################
@app.callback(
    # Where the results of the function end up
    # =======================================
    Output('interval-component', 'disabled'),
    Output("my_buttons_pause-button", "n_clicks"),
    Output("my_buttons_pause-button", "outline"),

    # Changes in (one of) these fires this callback
    # =============================================
    Input('my_buttons_pause-button', 'n_clicks'),

    # Values passed without firing callback
    # =============================================
    State("my_buttons_pause-button", "outline")  # if outline = True then pause not pressed if false then pause is pressed
)
def pause_button_clicked(i_clicked, s_pause):
    # gets fired when pause button is clicked
    if i_clicked == 1 and s_pause is True:
        return True, 0, False  # disable interval timer, reset pause button clicked value, set outline => clicked
    return False, 0, True  # enable interval timer, reset pause button clicked value, set no outline => not clicked


####################################################
# UPDATE FUNCTIONS GRAPHS
####################################################
@app.callback(
    # Where the results of the function end up
    # =======================================    
    Output('my_ships_locations_pre_txt', 'children'),  # text time as pre text
    Output('show-selected-delay-value', 'children'),  # text delay
    Output('my_automation_auto-changing-slider', 'value'),  # change value of slider index
    Output('my_automation_auto-changing-slider', 'marks'),  #
    Output('radar_sensor_px_static', 'figure'),
    Output('my_ships_locations', 'figure'),
    Output("my_buttons_skip-to-start", "n_clicks"),
    Output("my_buttons_next-button", "n_clicks"),
    Output("my_buttons_prev-button", "n_clicks"),
    Output("images_to_view_left", "src"),
    Output("images_to_view_right", "src"),

    # Changes in (one of) these fires this callback
    # =============================================    
    Input('interval-component', 'n_intervals'),
    Input("my_buttons_skip-to-start", "n_clicks"),
    Input('my_buttons_next-button', 'n_clicks'),
    Input('my_buttons_prev-button', 'n_clicks'),
    
    # Values passed without firing callback
    # =============================================
    State("my_buttons_pause-button", "outline")  # if outline = True then pause button not pressed if False then pause button is pressed
)
def updates_for_graphs(i_interval, skip_to_start_clicked, next_clicked, prev_clicked, pause_not_pressed):
    # call back for updating auto markers and graphs. 
    # gets fired every time xx mili sec's 
    
    global glb_current_mark_index 
    global glb_interval_time_ms
    global glb_marker_start
    global glb_marker_end
    
    interval_time = int(glb_interval_time_ms) 
    
    # ============================== 
    # update automatic slider
    # ==============================
    old_index = glb_current_mark_index
    
    # set old value to black 
    marks_items[glb_current_mark_index]['style']['color'] = "black"
    marks_items[glb_current_mark_index]['style']['font-weight'] = "normal"
    marks_items[glb_current_mark_index]['style']['font-size'] = '10px'

    if pause_not_pressed is True:  # just loopt through the marker items
        glb_current_mark_index = glb_current_mark_index + 1  # get next datapoint
        if glb_current_mark_index == glb_marker_end:  # Last marker has no text value 
            glb_current_mark_index = glb_marker_start + 1  # goto first marker with the data. First marker has no text, so select the next one
    
    else:

        if next_clicked == 1:  # go to next marker
            glb_current_mark_index = glb_current_mark_index + 1  # get next datapoint
            if glb_current_mark_index == glb_marker_end:  # Last marker has no text value 
                glb_current_mark_index = glb_marker_start + 1  # goto first marker with the data. First marker has no text, so select the next one
            
        if prev_clicked == 1:  # go to next marker
            glb_current_mark_index = glb_current_mark_index - 1  # get previous datapoint
            if glb_current_mark_index == glb_marker_start:  # first marker has no text value 
                glb_current_mark_index = glb_marker_end - 1  # goto last marker with the data. Last marker has no text, so select the previous one

    if skip_to_start_clicked == 1:  # skip to start button was clicked 
        glb_current_mark_index = glb_marker_start + 1
        
    # set new value to red
    marks_items[glb_current_mark_index]['style']['color'] = "red"
    marks_items[glb_current_mark_index]['style']['font-weight'] = "bold"
    marks_items[glb_current_mark_index]['style']['font-size'] = '11px'

    # ===========================
    # select data from df's
    # ===========================
    local_dt_to_show = marks_items[glb_current_mark_index]['label']
#    display(local_dt_to_show)

    selected_radar_sensor_df = melted_df[(melted_df['dt_local_str'].str.contains(local_dt_to_show))]
#    display(selected_radar_sensor_df)

    # display(ships_subset_df)
    selected_ships_subset_df = ships_subset_df[(ships_subset_df['dt_local_str'].str.contains(local_dt_to_show))]
    # display(local_dt_to_show)
    # display(selected_ships_subset_df)

    # ===========================
    # update text
    # ===========================
    delay_text = html.P(f"Delay value: {interval_time}" + " mili sec")
    datetime_text = html.H3([f"Current Local Date Time: {local_dt_to_show}"])
    filenamepart = local_dt_to_show.replace(" ", "").replace("-", "").replace(":", "")
    filenamepart = filenamepart[:8] + "T" + filenamepart[-6:]

    # ======================
    # create new fig(s)
    # ======================
    return_radar_fig = radar_sensor_px_static(selected_radar_sensor_df)
    
    # return_shipslocation_fig = mapbox_px_static2(df=selected_ships_subset_df,
    #                                              center_value=glb_calc_center,
    #                                              zoom_value=glb_calc_zoom,
    #                                              map_rotation=-62,
    #                                              token=mapbox_access_token
    #                                              )

    return_shipslocation_fig = mapbox_go_static(ships_df=selected_ships_subset_df,
                                                sensors_df=selected_radar_sensor_df,
                                                center_value=glb_calc_center,
                                                zoom_value=glb_calc_zoom,
                                                map_rotation=-62,
                                                token=mapbox_access_token
                                                )

    # https://dash.plotly.com/dash-enterprise/static-assets
    # https://dash.plotly.com/reference#dash.dash
    assets_folder = app.config['assets_folder']

    img_left = '../assets/video_to_pic/BLACKSCREEN.png'
    if os.path.exists(assets_folder+'/video_to_pic/' + filenamepart + '_NOORD.png'):
        # print(assets_folder+'/video_to_pic/' + filenamepart + '_NOORD.png')
        img_left = '../assets/video_to_pic/' + filenamepart + '_NOORD.png'

    img_right = '../assets/video_to_pic/BLACKSCREEN.png'
    if os.path.exists(assets_folder+'/video_to_pic/' + filenamepart + '_ZUID.png'):
        # print(assets_folder+'/video_to_pic/' + filenamepart + '_ZUID.png')
        img_right = '../assets/video_to_pic/' + filenamepart + '_ZUID.png'

    return datetime_text, delay_text, glb_current_mark_index, marks_items, return_radar_fig, return_shipslocation_fig, 0, 0, 0, img_left, img_right


####################################################
# START THE APP
####################################################
if __name__ == "__main__":
    print("Running on     : " + the_hostname)
    print("Run on env var : " + run_on)
    print("App version    : " + app_version)
    print("Python version : " + python_version)
    print("dash version   : " + dash_version)
    print("plotly version : " + plotly_version)

    # #################################
    # depending on where code is running
    # should be optimized in final version
    # #################################

    # Raspberry Pi on Local network
    if the_hostname == "rpi4-18 ":
        app.run_server(host="192.168.2.18", port=8050, debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter)

    # EC2 instance on AWS
    elif the_hostname == "ip-10-0-1-5":
        app.run_server(host="10.0.1.5", port=8050, debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter)

    # local development machine
    elif the_hostname == "LEGION-2020":
        app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter)

    # on Heroku
    else:
        app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter)
