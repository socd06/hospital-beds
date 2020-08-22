import pandas as pd
import folium
from folium import plugins
import math

def data_filter(dataframe_path, features):
    '''
    Returns a subset dataframe of the original with the selected features

    Parameters:

    dataframe_path (string): Path to the original dataframe

    features (list of strings): Dataframe columns to use in application
    '''

    df = pd.read_csv(dataframe_path)

    sub_dataframe = df[features]

    return sub_dataframe

def capacity_mapping(capacity):
    '''
    Sets the color of the map marker depending on the bed capacity

    Parameters:
    capacity (float): Bed Capacity extracted from dataframe

    returns:
    color (string): green for hospitals with over 66% capacity,
                    orange for over 33%, red for over 0% and gray when
                    data is not available.
    '''

    if capacity > 66:
        color = "green"
    elif capacity > 33:
        color = "orange"
    elif capacity > 0:
        color = "red"
    else:
        color = "gray"

    return color

def map_location(data, location, level):
    '''
    returns a subset dataframe of the original with the selected features

    Parameters:

    data (pandas.dataframe): Path to the original dataframe

    location (string): location to return hospitals

    level (string): "state" if location is a state name or "city" if it's a city
    '''

    if level == "state":

        # Filter dataframe by state
        is_state = data["STATE_NAME"] == location

        # Make chosen state dataframe
        df = data[is_state].reset_index(drop=True)

        zoom = 7

    if level == "city":

        # Filter dataframe by city
        is_city = data["HQ_CITY"] == location

        # Make chosen state dataframe
        df = data[is_city].reset_index(drop=True)

        zoom = 12

    # Coordinates are read [Y, X] AKA [latitute, longitude]
    center_coords = [df["Y"].mean(),df["X"].mean()]

    my_map = folium.Map(location = center_coords, zoom_start = zoom)

    for i in range(len(df)):

        # Make a html string of what will be added to the folium marker
        popup_str1 = "<b>" + df.loc[i, "HOSPITAL_NAME"] + "</b><br>"
        popup_str2 = df.loc[i, "HQ_ADDRESS"] + ", " + df.loc[i, "HQ_CITY"] + ", "
        popup_str3 = str(df.loc[i, "HQ_ZIP_CODE"]) + "<br>" + df.loc[i, "STATE_NAME"]

        popup_string = popup_str1 + popup_str2 + popup_str3

        pp = folium.Html(popup_string, script=True)
        popup = folium.Popup(pp, max_width=2560)

        # Iterate through dataframe and round the bed capacity for display
        cap = 100*(1-df.loc[i, "BED_UTILIZATION"])

        if int(math.isnan(cap)):
            tooltip_string = "Bed Data Not Available"
        else:
            tooltip_str1 = f' <b>{cap:.2f}' +"%</b> Beds Available <br>"
            tooltip_str2 = f' <b>{df.loc[i, "NUM_STAFFED_BEDS"]:.0f} </b> Total <br>'
            tooltip_str3 = f' <b>{df.loc[i, "PEDI_ICU_BEDS"]:.0f} </b> Pediatric ICU <br>'
            tooltip_str4 = f' <b>{df.loc[i, "ADULT_ICU_BEDS"]:.0f} </b> Adult ICU <br>'

            tooltip_string = tooltip_str1 + tooltip_str2 + tooltip_str3 + tooltip_str4

        # Obtain marker coordinates from dataframe
        marker_coords = [df.loc[i, "Y"], df.loc[i, "X"]]

        # Add everything to the markers and add the markers to the map
        # run help(folium.Icon) for further customization
        # see available icons at https://fontawesome.com/v4.7.0/icons/
        folium.Marker(marker_coords,popup=popup, tooltip=tooltip_string,
        icon=folium.Icon(color=capacity_mapping(cap),icon='hospital-o', prefix='fa')).add_to(my_map)

        # Save rendering and then display
        my_map.save("templates/map.html")

    #return my_map
