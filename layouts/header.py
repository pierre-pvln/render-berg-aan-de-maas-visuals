# ############################################################################
#
# GEEN FUNCTIES/LOGICA UITVOEREN IN DIT BESTAND.
# ENKEL BEDOELD OM EEN LAYOUT ELEMENT TE DEFINIEREN
#
# @version    v0.0.5  2022-11-17
# @author     pierre@ipheion.eu
# @copyright  (C) 2020-2022 Pierre Veelen
# 
# ############################################################################
#
# - styling in .\assets\styles.css
#                 python <-> css
#                tagname <-> tagname
#             id=some-id <-> #some-id
#   className=some-class <-> .some-class
#
# ############################################################################

import dash_bootstrap_components as dbc
from dash import html


# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
def build_header(title_str, version_str):
    """
    Returns a HTML Header element for the application Header.

    :return: HTML Header
    """
    return html.Header(
        children=[
            header_row_top(),
            header_row_center(title_str, version_str),
            header_row_bottom(),
        ]
    )


def header_row_top():
    return dbc.Row(
        children=[],
        id="header-row-top"
    )


def header_row_center(header_title, current_version):
    return dbc.Row(
        children=[
            dbc.Col(
                [
                    html.A(
                        html.Img(
                            [],
                            #src="../assets/img/ipheion_logo_2020.png",
                            src="./assets/img/Slide5_grid_transparent.png",

                            height=60,
                            style={  # "textAlign": "center"
                                "display": "block",
                                "marginLeft": "auto",
                                "marginRight": "auto",
                                # "width": "50%"
                            },
                        ),
                        href="https://ipheion.eu/de-aanpak-van/data-analytics-data-visualisatie/",
                        target="new",
                    ),
                ]
            ),
            dbc.Col(
                [
                    html.H1(
                        [header_title],
                        style={"textAlign": "center", "color": "#263473"},
                    ),
                        
                ],
                width=6,
            ),
            dbc.Col([html.P(["version: " + current_version], style={"color": "#263473"},)]),
            dbc.Col(
                [
                    # html.A(
                    #     html.Img(
                    #         [],
                    #         src="../assets/img/logo-client0.png",
                    #         height=60,
                    #         style={  # "textAlign": "center"
                    #             "display": "block",
                    #             "marginLeft": "auto",
                    #             "marginRight": "auto",
                    #             # "width": "50%"
                    #         },
                    #     ),
                    #     href="https://example.com/",
                    #     target="new",
                    # ),
                ]
            ),
        ],
        id="header_row_center",
        style={
            "background": "#D5E8F5",
            "borderBottom": "solid",
            "borderColor": "#9BC552",
        },
    )


def header_row_bottom():
    return dbc.Row(
        children=[],
        id="header-row-bottom",
        style={"background": "#D5E8F5", "paddingTop": "10px"},
    )
