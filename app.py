from flask import Flask, render_template, url_for, flash, redirect

import folium
from folium.plugins import MarkerCluster
import pandas as pd
import math
# Import from forms script
from forms import MapSeachForm

# import from scripts folder
from backend import map_state, data_filter

# data preprocessing

# read from data folder
df_path = "data/usa-hospital-beds_dataset_usa-hospital-beds.csv"

# feature selection
features = ["Y","X","BED_UTILIZATION","HOSPITAL_NAME","HQ_ADDRESS","HQ_CITY","STATE_NAME","HQ_ZIP_CODE"]

# Making data subset
df = data_filter(df_path, features)

# Listing all states
available_states = df['STATE_NAME'].unique()

############ flask app begins ############
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = "78f4d2ca06b3f9af87f963826c69e7e7"

@app.route('/', methods=['GET','POST'])
def index():

    form = MapSeachForm()

    if form.validate_on_submit():
        # Notify user the app is working
        flash(f'Searching for hospitals in {form.state_name.data}', 'success')

        if form.state_name.data in available_states:
            # Make a map of the searched state
            map = map_state(data=df,state=form.state_name.data)
            return redirect(url_for('map'))

        else:
            flash(f'{form.state_name.data} not found or not available. Please try again. Input is case-sensitive.', 'danger')

        # oringinally here
        #return redirect(url_for('map'))
    return render_template('index.html', form=form)

# Create an index url to prevent not found 404 error
@app.route('/map', methods=['GET','POST'])
# Define the function for the route
def map():

    return render_template('map.html')


if __name__ == '__main__':
    app.run(debug=True)
