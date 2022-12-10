# https://plotly.com/python/graph-objects/
# https://plotly.com/python/figure-structure/
import os

import plotly.express as px


def update_mmsi_data_dict_list(inputdf, markermode, verbosity=False):
    verbosity = True

    if verbosity:
        print('update_mmsi_data_dict_list')
        print(inputdf.head())
        print(inputdf.dtypes)

    inputdf['customtext'] =   "MMSI     : " + inputdf['mmsi'].astype('str') + '<br>' \
                            + "Speed    : " + inputdf['AIS_speed'].astype('str') + '<br>' \
                            + "UTC Tijd : " + inputdf['balenaAISmessageUTC_str'] + '<br>'

    this_mmsi_data_dict_list = []
    this_unique_mmsi_list = inputdf['mmsi'].unique()

    # print(this_unique_mmsi_list)

    for the_mmsi in this_unique_mmsi_list:
        print(the_mmsi)

        # select only current mmsi
        subsetdf = inputdf.loc[inputdf['mmsi'] == the_mmsi].copy()
        color_to_use = subsetdf['shipscolor'].unique()[0]

        # create a new dict for every mmsi -> creates a new curveNumber for every unique mmsi
        this_mmsi_data_dict = dict(
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-type
            type="scattermapbox",

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-name
            name=the_mmsi,  # should then be MMSI or shipsname

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-showlegend
            showlegend=False,  # do not show this dataset in legend

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lat
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lon
            # where to show the markers
            lat=subsetdf['AIS_lat'],
            lon=subsetdf['AIS_lon'],

            line=dict(
                color=color_to_use,
                width=2
            ),

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-mode
            # show markers + text on the map
            mode=markermode,
            # mode="markers+text",

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertext
            # show hovertext if not defined
            # show the text
            hovertext=subsetdf["mmsi"],

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-customdata
            customdata=subsetdf['customtext'],

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hoverinfo
            hoverinfo="name+text",
            # hoverinfo="name",

            # https://plotly.com/AIS_ javascript/reference/scattermapbox/#scattermapbox-hovertemplate
            hovertemplate="<b>%{hovertext}</b><br>" +
                          "%{customdata}<br>" +
                          "<extra>Ships</extra>",

            # Set marker colors based on values
            # https://stackoverflow.com/questions/61686382/change-the-text-color-of-cells-in-plotly-table-based-on-value-string
            marker=dict(
                symbol="circle",  # name of icon in icon set or "circle"
                # size=subsetdf["ais_speed"] * 1 + 3,
                size=subsetdf["AIS_speed"] * 2 + 3,
                # sizemin=4,
                sizemode="diameter",
                color=color_to_use,
                opacity=0.5
            ),
        )
        this_mmsi_data_dict_list += [this_mmsi_data_dict]  # a += b => a = a + b

    if len(this_mmsi_data_dict_list) == 0:
        # if no entries in list, no map is shown
        # so create an empty list with minimum info

        this_mmsi_data_dict_list = [dict(
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-type
            type="scattermapbox",
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-showlegend
            showlegend=False,  # do not show this dataset in legend
            )
        ]

    return this_mmsi_data_dict_list  # returns a list of mmsi traces with a circle being speed


def update_mmsi_data_dict_list2(inputdf, markermode, verbosity=False):
    #verbosity = True

    inputdf = inputdf.copy() # to prevent "settingWithCopyWarning" message
    
    if verbosity:
        print('update_mmsi_data_dict_list2')
        print(inputdf.head())
        print(inputdf.dtypes)

    inputdf['customtext'] =   "MMSI      : " + inputdf['mmsi'].astype('str') + '<br>' \
                            + "Speed     : " + inputdf['AIS_speed'].astype('str') + '<br>' \
                            + "LocalTime : " + inputdf['dt_local_str'] + '<br>' \
                            + "Lat       : " + inputdf['AIS_lat'].astype('str') + '<br>' \
                            + "Lon       : " + inputdf['AIS_lon'].astype('str') + '<br>'

    this_mmsi_data_dict_list = []
    this_unique_mmsi_list = inputdf['mmsi'].unique()

    # print(this_unique_mmsi_list)

    for the_mmsi in this_unique_mmsi_list:
        #print(the_mmsi)

        # select only current mmsi
        subsetdf = inputdf.loc[inputdf['mmsi'] == the_mmsi].copy()
        color_to_use = subsetdf['shipscolor'].unique()[0]
        
        # name_in_legend = the_mmsi
        name_in_legend = subsetdf['naam'].unique()[0]

        # create a new dict for every mmsi -> creates a new curveNumber for every unique mmsi
        this_mmsi_data_dict = dict(
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-type
            type="scattermapbox",

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-name
            name=name_in_legend,  # should then be MMSI or shipsname

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-showlegend
            showlegend=False,  # do not show this dataset in legend

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lat
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lon
            # where to show the markers
            lat=subsetdf['AIS_lat'],
            lon=subsetdf['AIS_lon'],

            line=dict(
                color=color_to_use,
                width=2
            ),

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-mode
            # show markers + text on the map
            mode=markermode,
            # mode="markers+text",

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertext
            # show hovertext if not defined
            # show the text
            hovertext=subsetdf["naam"],

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-customdata
            customdata=subsetdf['customtext'],

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hoverinfo
            hoverinfo="name+text",
            # hoverinfo="name",

            # https://plotly.com/AIS_ javascript/reference/scattermapbox/#scattermapbox-hovertemplate
            hovertemplate="<b>%{hovertext}</b><br>" +
                          "%{customdata}<br>" +
                          "<extra>Ships</extra>",

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-text
            text=name_in_legend,
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-textposition
            textposition="top-center",

            # Set marker colors based on values
            # https://stackoverflow.com/questions/61686382/change-the-text-color-of-cells-in-plotly-table-based-on-value-string
            marker=dict(
                symbol="circle",  # name of icon in icon set or "circle"
                # size=subsetdf["ais_speed"] * 1 + 3,
                size=subsetdf["AIS_speed"] * 4 + 4,
                # sizemin=4,
                sizemode="diameter",
                color=color_to_use,
                opacity=0.5
            ),
        )
        this_mmsi_data_dict_list += [this_mmsi_data_dict]  # a += b => a = a + b

    if len(this_mmsi_data_dict_list) == 0:
        # if no entries in list, no map is shown
        # so create an empty list with minimum info

        this_mmsi_data_dict_list = [dict(
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-type
            type="scattermapbox",
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-showlegend
            showlegend=False,  # do not show this dataset in legend
            )
        ]

    return this_mmsi_data_dict_list  # returns a list of mmsi traces with a circle being speed


def update_sensor_data_dict_list(inputdf, markermode, verbosity=False):
    #verbosity = True

    inputdf = inputdf.copy()  # to prevent "settingWithCopyWarning" message
    
    if verbosity:
        print('update_sensor_data_dict_list2')
        print(inputdf.head())
        print(inputdf.dtypes)

    inputdf['customtext'] = "Sensor     : " + inputdf['sensor'].astype('str') + '<br>' \
                            + "Distance    : " + inputdf['afstand'].astype('str') + '<br>' \
                            + "LocalTime : " + inputdf['dt_local_str'] + '<br>'

    this_sensor_data_dict_list = []
    this_unique_sensor_list = inputdf['sensor'].unique()

    # print(this_unique_mmsi_list)

    for the_sensor in this_unique_sensor_list:
        # select only current sensor
        subsetdf = inputdf.loc[inputdf['sensor'] == the_sensor].copy()

        color_discrete_map = {'rest': 'rgb(0,0,255)',
                              'no-alert': 'rgb(0,255,0)',
                              'alert': 'rgb(255,127,0)',
                              'major-alert': 'rgb(255,0,0)'
                              }

        color_to_use = color_discrete_map.get(subsetdf['alert'].unique()[0], 'rgb(128,128,128)')
        # use color from colormap, otherwise set it to grey

        # name_in_legend = unit
        name_in_legend = subsetdf['unit'].unique()[0]
        # ##### text_at_marker = subsetdf['afstand'].unique()[0]

        # create a new dict for every sensor -> creates a new curveNumber for every unique sensor
        this_sensor_data_dict = dict(
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-type
            type="scattermapbox",

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-name
            name=name_in_legend,  # should then be unit name

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-showlegend
            showlegend=False,  # do not show this dataset in legend

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lat
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lon
            # where to show the markers
            lat=subsetdf['sensor_lat'],
            lon=subsetdf['sensor_lon'],

            line=dict(
                color=color_to_use,
                width=2
            ),

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-mode
            # show markers + text on the map
            mode=markermode,
            # mode="markers+text",

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertext
            # show hovertext if not defined
            # show the text
            hovertext=subsetdf["unit"],

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-customdata
            customdata=subsetdf['customtext'],

            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hoverinfo
            hoverinfo="name+text",
            # hoverinfo="name",

            # https://plotly.com/AIS_ javascript/reference/scattermapbox/#scattermapbox-hovertemplate
            hovertemplate="<b>%{hovertext}</b><br>" +
                          "%{customdata}<br>" +
                          "<extra>Sensors</extra>",

            # #### https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-text
            # #### text="22",
            # #### text=text_at_marker,
            # #### https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-textposition
            # #### textposition="top-center",

            # Set marker colors based on values
            # https://stackoverflow.com/questions/61686382/change-the-text-color-of-cells-in-plotly-table-based-on-value-string
            marker=dict(
                symbol="circle",  # name of icon in icon set or "circle"
                # size=subsetdf["ais_speed"] * 1 + 3,
                #size=subsetdf["afstand"] * 4 + 4,
                #size=6,
                # sizemin=4,
                size=[
                    8
                    if x == "no-alert"
                    else 6
                    if x == "rest"
                    else 10
                    if x == "alert"
                    else 12
                    if x == "major-alert"
                    else 6
                    for x in list(subsetdf['alert'])
                ],

                sizemode="diameter",
                color=color_to_use,
                opacity=1
            ),
        )
        this_sensor_data_dict_list += [this_sensor_data_dict]  # a += b => a = a + b

    if len(this_sensor_data_dict_list) == 0:
        # if no entries in list, no map is shown
        # so create an empty list with minimum info

        this_sensor_data_dict_list = [dict(
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-type
            type="scattermapbox",
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-showlegend
            showlegend=False,  # do not show this dataset in legend
            )
        ]

    return this_sensor_data_dict_list  # returns a list of sensor traces with a circle being speed


####################################################
# MAPBOX GRAPHS
####################################################
def mapbox_static(df, center_value, zoom_value, map_rotation, token):
    data_dict_list = update_mmsi_data_dict_list(df, "markers+text+lines", verbosity=False)

    fig = {
        "data": data_dict_list,
        "layout": dict(autosize=True,
                       hovermode="closest",
                       margin=dict(l=0, r=0, t=0, b=0),
                       clickmode="event+select",

                       # https://plotly.com/python/reference/layout/mapbox/
                       mapbox=dict(accesstoken=token,
                                   bearing=map_rotation,
                                   # center={"lon": 5.764278, "lat": 50.986729}, Stein
                                   center=center_value,
                                   style="outdoors",
                                   pitch=0,
                                   # zoom=13.97,
                                   zoom=zoom_value,
                                   # layers=update_layers_list(glb_geozone_list)
                                   ),
                       ),
    }

    return fig


def mapbox_px_animated(df, center_value, zoom_value, map_rotation, token):
    # https://plotly.com/python-api-reference/generated/plotly.express.set_mapbox_access_token.html
    px.set_mapbox_access_token(token)

    # https://plotly.github.io/plotly.py-docs/generated/plotly.express.scatter_mapbox.html
    fig = px.scatter_mapbox(df,
                            lat="AIS_lat",
                            lon="AIS_lon",
                            animation_frame='dt_local_str',
                            # animation_group='Country',
                            color="shipscolor",
                            size="updated_speed",
                            # color_continuous_scale=px.colors.cyclical.IceFire,
                            # size_max=10,
                            zoom=zoom_value,
                            center=center_value,
                            hover_name='mmsi',
                            mapbox_style="outdoors",
                            height=400,
                            # title = "my title",
                            )

    # https://plotly.com/python/reference/layout/mapbox/
    fig.update_mapboxes(bearing=map_rotation)

    return fig

def mapbox_px_static(df, center_value, zoom_value, map_rotation, token):
    # https://plotly.com/python-api-reference/generated/plotly.express.set_mapbox_access_token.html
    px.set_mapbox_access_token(token)

    # https://plotly.github.io/plotly.py-docs/generated/plotly.express.scatter_mapbox.html
    fig = px.scatter_mapbox(df,
                            lat="AIS_lat",
                            lon="AIS_lon",
                            #animation_frame='dt_local_str',
                            # animation_group='Country',
                            color="mmsi",
                            size="updated_speed",
                            # color_continuous_scale=px.colors.cyclical.IceFire,
                            # size_max=10,
                            zoom=zoom_value,
                            center=center_value,
                            hover_name='mmsi',
                            mapbox_style="outdoors",
                            height=400,
                            # title = "my title",
                            )

    # https://plotly.com/python/reference/layout/mapbox/
    fig.update_mapboxes(bearing=map_rotation)

    # https://plotly.com/python/legend/
    fig.update_layout(showlegend=False)
    
    return fig

def mapbox_px_static2(df, center_value, zoom_value, map_rotation, token):
    
    data_dict_list = update_mmsi_data_dict_list2(df, "markers+text", verbosity=False)

    fig = {
        "data": data_dict_list,
        "layout": dict(autosize=True,
                       hovermode="closest",
                       margin=dict(l=0, r=0, t=0, b=0),
                       clickmode="event+select",

                       # https://plotly.com/python/reference/layout/mapbox/
                       mapbox=dict(accesstoken=token,
                                   bearing=map_rotation,
                                   # center={"lon": 5.764278, "lat": 50.986729}, Stein
                                   center=center_value,
                                   style="outdoors",
                                   pitch=0,
                                   # zoom=13.97,
                                   zoom=zoom_value,
                                   # layers=update_layers_list(glb_geozone_list)
                                   ),
                       ),
    }

    return fig


def mapbox_go_static(ships_df, sensors_df, center_value, zoom_value, map_rotation, token):

    data_dict_list = []
    data_dict_list += update_mmsi_data_dict_list2(ships_df, "markers+text", verbosity=False)  # a += b => a = a + b
    data_dict_list += update_sensor_data_dict_list(sensors_df, "markers+text", verbosity=False)  # a += b => a = a + b

    fig = {
        "data": data_dict_list,
        "layout": dict(
            autosize=True,
            hovermode="closest",
            margin=dict(l=0, r=0, t=0, b=0),
            clickmode="event+select",

            # https://plotly.com/python/reference/layout/mapbox/
            mapbox=dict(
                accesstoken=token,
                bearing=map_rotation,
                # center={"lon": 5.764278, "lat": 50.986729}, Stein
                center=center_value,
                style="outdoors",
                pitch=0,
                # zoom=13.97,
                zoom=zoom_value,
                # layers=update_layers_list(glb_geozone_list)
                ),
            ),
    }

    return fig


####################################################
# BAR GRAPHS
####################################################
def radar_sensor_px_animated(df):
    # https://plotly.com/python-api-reference/generated/plotly.express.bar.html
    fig = px.bar(df,
                 x="x",
                 y="afstand",
                 color="sensor",
                 animation_frame="dt_local_str",
                 # animation_group="sensor",
                 hover_name="sensor",
                 range_x=[1, 10],
                 range_y=[-20, 80],
                 # width=2000,
                 # height=600
                 )

    # https://plotly.com/python/reference/layout/xaxis/
    fig.update_xaxes(tickangle=0, title_text="sensoren")

    # https://plotly.com/python/reference/layout/yaxis/
    fig.update_yaxes(tickangle=0, title_text="gemeten afstand")

    # https://stackoverflow.com/questions/61731161/increasing-speed-on-plotly-animation
    # https://plotly.com/python/reference/layout/#layout-transition
    fig.update_layout(transition={'duration': 1000})

    # # https://plotly.com/python-api-reference/generated/plotly.io.write_json.html
    # print("writing fig info to json file")
    # fig.write_json(file="./radar_sensor_px_animated_log.json", pretty=True)

    return fig

def radar_sensor_px_static(df):
    # https://plotly.com/python-api-reference/generated/plotly.express.bar.html
    fig = px.bar(df,
                 x="x",
                 y="afstand",
                 
                 color="alert",
                 color_discrete_map={'rest': 'rgb(0,0,255)',
                                     'no-alert': 'rgb(0,255,0)',
                                     'alert': 'rgb(255,127,0)',
                                     'major-alert': 'rgb(255,0,0)'
                                     },

                 category_orders={"alert": ["rest", "no-alert", "alert", "major-alert"]
                                  },
                                  
                 # animation_frame="dt_local_str",
                 # animation_group="sensor",
                 hover_name="sensor",
                 range_x=[0, 10],
                 range_y=[-10, 30],
                 # width=2000,
                 # height=600
                 )

    # https://plotly.com/python/reference/layout/xaxis/
    fig.update_xaxes(tickangle=0, 
                     title_text="sensoren",
                     
                     tickmode='array',
                     ticktext=df['sensor'],
                     tickvals=df['x']
                    )

    # https://plotly.com/python/reference/layout/yaxis/
    fig.update_yaxes(tickangle=0, title_text="gemeten afstand (m)")
    
    # https://plotly.com/python/legend/
    fig.update_layout(showlegend=False)
    
#     # https://plotly.com/python-api-reference/generated/plotly.io.write_json.html
#     print("writing fig info to json file")
#     fig.write_json(file="./radar_sensor_px_animated_log.json", pretty=True)

    return fig
