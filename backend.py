import folium
import pandas as pd
import math

df = pd.read_csv("data/usa-hospital-beds_dataset_usa-hospital-beds.csv")

# Make a dataframe with only the features to display in the map
# Choosing features
features = ["Y","X","BED_UTILIZATION","HOSPITAL_NAME","HQ_ADDRESS","HQ_CITY","STATE_NAME","HQ_ZIP_CODE"]

# make the sub-dataframe
sub_df = df[features]

def map_state(state_name):

    # Filter dataframe by state
    is_state = sub_df["STATE_NAME"] == state_name

    # Make chosen state dataframe
    state_df = sub_df[is_state].reset_index(drop=True)

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

        tooltip_string = "Beds Available: "

        # Iterate through dataframe and round the bed capacity for display
        cap = state_df.loc[i, "BED_UTILIZATION"]

        if int(math.isnan(cap)):
            tooltip_string += "Data Not Available"
        else:
            # Use an f-string to calculate bed availability percentage and round the result in a single line
            #tooltip_string += f'{1-cap:.2f}' +"%"
            tooltip_string += f'{100*(1-cap):.2f}' +"%"

        # Obtain marker coordinates from dataframe
        marker_coords = [state_df.loc[i, "Y"], state_df.loc[i, "X"]]

        # Add everything to the markers and add the markers to the map
        folium.Marker(marker_coords,popup=popup, tooltip=tooltip_string).add_to(my_map)

        # Save rendering and then display
        my_map.save("map.html")

    #return my_map
