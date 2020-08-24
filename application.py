from flask import Flask, render_template, url_for, flash, redirect, session

import folium
from folium.plugins import MarkerCluster
import pandas as pd
import math
# Import from forms script
from forms import MapSeachForm

# import from scripts folder
from backend import map_location, data_filter, capacity_mapping

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

    form = MapSeachForm()

    if form.validate_on_submit():

        # When searching by city
        flash(f'Searching for hospitals in {form.city_name.data}', 'success')

        if form.city_name.data in available_cities:

            # Save query string and location level (state or city) in flask session
            session["query"] = form.city_name.data
            session["level"] = "city"

            return redirect(url_for('map'))
        else:
            flash(f'{form.city_name.data} not found or not available. Please try again. Input is case-sensitive.', 'danger')

        # When searching by state
        flash(f'Searching for hospitals in {form.state_name.data}', 'success')

        if form.state_name.data in available_states:

            # Save query string and location level (state or city) in flask session
            session["query"] = form.state_name.data
            session["level"] = "state"

            return redirect(url_for('map'))
        else:
            flash(f'{form.state_name.data} not found or not available. Please try again. Input is case-sensitive.', 'danger')

    return render_template('index.html', form=form)

# Create an index url to prevent not found 404 error
@app.route('/map', methods=['GET','POST'])
# Define the function for the route
def map():

    folium_map = map_location(data=df,location=session["query"], level=session["level"])

    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
