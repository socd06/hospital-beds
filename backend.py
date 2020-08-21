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


def map_state(data, state):
    '''
    returns a subset dataframe of the original with the selected features

    Parameters:

    data (pandas.dataframe): Path to the original dataframe

    query (string): location to return hospitals
    '''

    # Filter dataframe by state
    is_state = data["STATE_NAME"] == state

    # Make chosen state dataframe
    state_df = data[is_state].reset_index(drop=True)

    # Coordinates are read [Y, X] AKA [latitute, longitude]
    center_coords = [state_df["Y"].mean(),state_df["X"].mean()]

    my_map = folium.Map(location = center_coords, zoom_start = 7.5)

    for i in range(len(state_df)):

        # Make a string of what will be added to the folium marker
        popup_str1 = "<b>" + state_df.loc[i, "HOSPITAL_NAME"] + "</b><br>"
        popup_str2 = state_df.loc[i, "HQ_ADDRESS"] + ", " + state_df.loc[i, "HQ_CITY"] + ", "
        popup_str3 = str(state_df.loc[i, "HQ_ZIP_CODE"]) + "<br>" + state_df.loc[i, "STATE_NAME"]

        popup_string = popup_str1 + popup_str2 + popup_str3

        pp = folium.Html(popup_string, script=True)
        popup = folium.Popup(pp, max_width=2560)

        tooltip_string = "Beds "

        # Iterate through dataframe and round the bed capacity for display
        cap = 100*(1-state_df.loc[i, "BED_UTILIZATION"])

        if cap > 66:
            color_mapping = "green"
        elif cap > 33:
            color_mapping = "orange"
        else:
            color_mapping = "red"

        if int(math.isnan(cap)):
            tooltip_string += "Data Not Available"
            color_mapping = "gray"
        else:
            tooltip_string += f'{cap:.2f}' +"% Available"

        # Obtain marker coordinates from dataframe
        marker_coords = [state_df.loc[i, "Y"], state_df.loc[i, "X"]]

        # Add everything to the markers and add the markers to the map
        # run help(folium.Icon) for further customization
        # see available icons at https://fontawesome.com/v4.7.0/icons/
        folium.Marker(marker_coords,popup=popup, tooltip=tooltip_string,
        icon=folium.Icon(color=color_mapping,icon='hospital-o', prefix='fa')).add_to(my_map)

        # Save rendering and then display
        my_map.save("templates/map.html")

    #return my_map
