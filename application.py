from flask import Flask, render_template, url_for, flash, redirect, session

import folium
from folium.plugins import MarkerCluster
import pandas as pd
import math
# Import from forms script
from forms import MapSearchForm, process_input

# import from scripts folder
from backend import map_location, data_filter, capacity_mapping

import pgeocode

# data preprocessing
# read from data folder
df_path = "data/usa-hospital-beds.csv"

# feature selection
features = ["Y","X","BED_UTILIZATION","HOSPITAL_NAME","HQ_ADDRESS",
"HQ_CITY","STATE_NAME","HQ_ZIP_CODE","NUM_STAFFED_BEDS","ADULT_ICU_BEDS","PEDI_ICU_BEDS"]

# Making data subset
df = data_filter(df_path, features)

# Listing all states
available_states = df['STATE_NAME'].unique()

# Listing all states
available_cities = df['HQ_CITY'].unique()

############ flask app begins ############
# double equal sign for AWS
application = app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = "78f4d2ca06b3f9af87f963826c69e7e7"

@app.route('/', methods=['GET','POST'])
def index():

    # Initialize pgeocode

    country_init = pgeocode.Nominatim("us")

    form = MapSearchForm()

    if form.validate_on_submit():

        if len(form.zip_code.data)> 0:

            try:
                # When searching by zip code
                flash(f'Searching for hospitals around {form.zip_code.data} zip code.', 'success')

                # Get city and center_coords with pgeocode
                zip_query = country_init.query_postal_code(form.zip_code.data)

                if pd.isna(zip_query.place_name) != True:

                    # and saving the city and center coordinates for further use
                    session["query"] = zip_query.place_name
                    session["level"] = "zip"

                    # Save center coordinates in the session to use with the mapping function
                    session["zip_coords"] = [zip_query.latitude, zip_query.longitude]

                    return redirect(url_for('map'))
                else:
                    flash(f'{form.zip_code.data} zip code not found or not available. Please try again.', 'danger')

            except:
                pass

        # When searching by city

        if len(form.city_name.data)> 0:
            try:
                form.city_name.data = process_input(form.city_name.data)

                flash(f'Searching for hospitals in {form.city_name.data} city', 'success')

                if form.city_name.data in available_cities:

                    # Save query string and location level (state or city) in flask session
                    session["query"] = form.city_name.data
                    session["level"] = "city"

                    return redirect(url_for('map'))

                else:
                    flash(f'{form.city_name.data} city not found or not available. Please try again.', 'danger')
            except:
                pass


        if len(form.state_name.data)> 0:
            try:
                form.state_name.data = process_input(form.state_name.data)

                # When searching by state
                flash(f'Searching for hospitals in {form.state_name.data} state', 'success')

                if form.state_name.data in available_states:

                    # Save query string and location level (state or city) in flask session
                    session["query"] = form.state_name.data
                    session["level"] = "state"

                    return redirect(url_for('map'))
                else:
                    flash(f'{form.state_name.data} state not found or not available. Please try again.', 'danger')
            except:
                pass

    return render_template('index.html', form=form)

# Create an index url to prevent not found 404 error
@app.route('/map', methods=['GET','POST'])
# Define the function for the route
def map():

    folium_map = map_location(data=df,location=session["query"], level=session["level"])

    return folium_map._repr_html_()

if __name__ == '__main__':
    app.run(debug=False)
