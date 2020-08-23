from flask import Flask, render_template, url_for, flash, redirect

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
df_path = "data/usa-hospital-beds_dataset_usa-hospital-beds.csv"

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
            # Make a map of the searched cities
            map = map_location(data=df,location=form.city_name.data, level="city")
            return redirect(url_for('map'))
        else:
            flash(f'{form.city_name.data} not found or not available. Please try again. Input is case-sensitive.', 'danger')

        # When searching by state
        flash(f'Searching for hospitals in {form.state_name.data}', 'success')

        if form.state_name.data in available_states:
            # Make a map of the searched state
            map = map_location(data=df,location=form.state_name.data, level="state")
            return redirect(url_for('map'))
        else:
            flash(f'{form.state_name.data} not found or not available. Please try again. Input is case-sensitive.', 'danger')

    return render_template('index.html', form=form)

# Create an index url to prevent not found 404 error
@app.route('/map', methods=['GET','POST'])
# Define the function for the route
def map():

    return render_template('map.html')


if __name__ == '__main__':
    app.run(debug=True)
