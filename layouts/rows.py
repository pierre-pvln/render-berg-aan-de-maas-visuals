from dash import dcc, html
import dash_bootstrap_components as dbc

def ships_speed_in_graph(unique_id_name, config_dict, figure_dict, pre_text="", post_text=""):
    return dbc.Row(
        # row with graph
        [
            # pre-column; mostly empty
            dbc.Col([], width=1, ),

            # col with graph
            dbc.Col(
                [
                    html.Center(
                        [html.H3(
                            [pre_text]
                        )
                        ],
                        id=unique_id_name + "_pre_txt"
                    ),
                    # https://dash.plotly.com/dash-core-components/graph
                    dcc.Graph(
                        id=unique_id_name,
                        figure=figure_dict,
                        config=config_dict,
                        # set the style for this element
                        style={
                            "height": "400px",
                            "width": "90%"
                        },
                    ),
                    html.Center(
                        [html.H3(
                            [post_text]
                        )
                        ],
                        id=unique_id_name + "_post_txt"
                    ),
                ],
                width=10,
            ),

            # post-column; mostly empty
            dbc.Col([], width=1, ),
        ],
        # set the style for this container
        style={"paddingTop": "10px"},
    )


def radar_distance_in_graph(unique_id_name, config_dict, figure_dict, pre_text="", post_text=""):
    return dbc.Row(
        # row with graph
        [
            # pre-column; mostly empty
            dbc.Col([], width=1, ),

            # col with graph
            dbc.Col(
                [
                    html.Center(
                        [html.H3(
                            [pre_text]
                        )
                        ],
                        id=unique_id_name + "_pre_txt"
                    ),
                    # https://dash.plotly.com/dash-core-components/graph
                    dcc.Graph(
                        id=unique_id_name,
                        figure=figure_dict,
                        config=config_dict,
                        # set the style for this element
                        style={
                            "height": "400px",
                            "width": "90%"
                        },
                    ),
                    html.Center(
                        [html.H3(
                            [post_text]
                        )
                        ],
                        id=unique_id_name + "_post_txt"
                    ),
                ],
                width=10,
            ),

            # post-column; mostly empty
            dbc.Col([], width=1, ),
        ],
        # set the style for this container
        style={"paddingTop": "10px"},
    )

def settings_slider_for_timinginterval(unique_id_name,interval_ms, pre_text="", post_text=""):
    return dbc.Row(
        # row with graph
        [
            # pre-column; mostly empty
            dbc.Col([], width=1, ),

            # col with graph
            dbc.Col(
                [
                    html.Center(
                        [html.H3(
                            [pre_text]
                        )
                        ],
                        id=unique_id_name + "_pre_txt"
                    ),
                    
                    # https://dash.plotly.com/dash-core-components/slider
                    dcc.Slider(
                        id=unique_id_name,
                        min=0, 
                        max=5,
                        #step=0.05,
                        step=0.1,
                        value=interval_ms/1000
                    ),
                    
                    html.Center(
                        [html.H3(
                            [post_text]
                        )
                        ],
                        id=unique_id_name + "_post_txt"
                    ),
                ],
                width=10,
            ),

            # post-column; mostly empty
            dbc.Col([], width=1, ),
        ],
        # set the style for this container
        style={"paddingTop": "10px"},
    )

def ships_locations_on_map(unique_id_name, config_dict, figure_dict, pre_text="", post_text=""):
    return dbc.Row(
        [
            # pre-column; mostly empty
            dbc.Col([], width=1, ),

            # col with graph
            dbc.Col(
                [
                html.Center(
                    [html.H3(
                        [pre_text]
                     )
                     ],
                    id=unique_id_name + "_pre_txt"
                ),
                # https://dash.plotly.com/dash-core-components/graph
                dcc.Graph(
                    id=unique_id_name,
                    figure=figure_dict,
                    config=config_dict,
                    style={
                        "height": "300px",
                        "width": "100%"
                    }
                ),
                html.Center(
                    [html.H3([post_text])],
                    id=unique_id_name + "_post_txt"
                ),
                ],
                width=10,
            ),

            # post-column; mostly empty
            dbc.Col([], width=1, ),
        ],
        # set the style for this container
        style={"paddingTop": "10px"},
    )


def automated_slider(unique_id_name, marker_start, marker_end, marker_items, marker_value):
    return dbc.Row(
        [
            # pre-column; mostly empty
            dbc.Col([], width=1, ),

            # col with slider
            dbc.Col(
                [
                # slider that is changing
                dcc.Slider(min=marker_start,
                           max=marker_end,
                           #step=100,
                           step=None,
                           marks=marker_items,
                           value=marker_value,
                           disabled=True, # handles can't be moved

                           # sets slider vertical
                           #vertical=True,
                           #verticalHeight=1600,
                           id=unique_id_name + "_auto-changing-slider",
                           ),
                ],
                style={"paddingTop": "0.5rem"},
                #width=8,
            ),

            # post-column; mostly empty
            dbc.Col([], width=1, ),

        ],
        style={"paddingTop": "10px",
               "paddingLeft": "25px"}

    )

def play_buttons(unique_id_name):
    return dbc.Row(
        [
        # pre-column; mostly empty
        dbc.Col([], width=4, ),

        # column with buttons
        dbc.Col(
            [
                dbc.Button("",
                           outline=True,
                           color="primary",
                           id=unique_id_name + "_skip-to-start",
                           class_name="bi bi-skip-start px-1 py-0",
                           # set margin https://www.w3schools.com/bootstrap5/bootstrap_utilities.php
                           # set button https://icons.getbootstrap.com/
                           n_clicks=0,
                           style={"font-size": "1rem"}
                          ),

                dbc.Button("",
                           outline=True,
                           color="primary",
                           id=unique_id_name + "_prev-button",
                           class_name="bi bi-caret-left px-1 py-0",
                           # set margin https://www.w3schools.com/bootstrap5/bootstrap_utilities.php
                           # set button https://icons.getbootstrap.com/
                           n_clicks=0,
                           style={"font-size": "1rem"}
                          ),

                dbc.Button("",
                           outline=True, # if false then button was clicked.
                           color="primary",
                           id=unique_id_name + "_pause-button",
                           class_name="bi bi-pause px-1 py-0",
                           # set margin https://www.w3schools.com/bootstrap5/bootstrap_utilities.php
                           # set button https://icons.getbootstrap.com/
                           n_clicks=0,
                           style={"font-size": "1rem"}
                          ),

                dbc.Button("",
                           outline=True,
                           color="primary",
                           id=unique_id_name + "_next-button",
                           class_name="bi bi-caret-right px-1 py-0",
                           # set margin https://www.w3schools.com/bootstrap5/bootstrap_utilities.php
                           # set button https://icons.getbootstrap.com/
                           n_clicks=0,
                           style={"font-size": "1rem"}
                           ),
            ],
            #style={"padding-left": "20px"},
            width=4,
        ),

        # post-column; mostly empty
        dbc.Col([], width=4, ),

        ],
        style={"paddingTop": "10px",
               "paddingLeft": "25px"}

    )

def updating_images(unique_id_name, img_left, img_right, pre_text="", post_text=""):
    return dbc.Row(
        # row with 2 images
        [
            # pre-column; mostly empty
            dbc.Col([], width=1, ),

            # left col with image
            dbc.Col(
                [
                    html.Center(
                        [html.H4(
                            ['North location = South facing camera']
                        )
                        ],
                        id=unique_id_name + "_left_pre_txt"
                    ),

                    html.Img(
                        [],
                        src=img_left,
                        height=180,
                        style={  # "textAlign": "center"
                                 "display": "block",
                                 "marginLeft": "auto",
                                 "marginRight": "auto",
                                 # "width": "50%"
                        },
                        id=unique_id_name + "_left"
                    ),

                    html.Center(
                        [html.H3(
                            [post_text]
                        )
                        ],
                        id=unique_id_name + "left_post_txt"
                    ),
                ],
                width=4,
            ),

            # center-column; mostly empty
            dbc.Col([], width=1, ),


            # right col with image
            dbc.Col(
                [
                    html.Center(
                        [html.H4(
                            ['South location = North facing camera']
                        )
                        ],
                        id=unique_id_name + "_right_pre_txt"
                    ),

                    html.Img(
                        [],
                        src=img_right,
                        height=180,
                        style={  # "textAlign": "center"
                            "display": "block",
                            "marginLeft": "auto",
                            "marginRight": "auto",
                            # "width": "50%"
                        },
                        id=unique_id_name + "_right"
                    ),

                    html.Center(
                        [html.H3(
                            [post_text]
                        )
                        ],
                        id=unique_id_name + "_right_post_txt"
                    ),
                ],
                width=4,
            ),

            # post-column; mostly empty
            dbc.Col([], width=1, ),
        ],
        # set the style for this container
        style={"paddingTop": "10px"},
    )

