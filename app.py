from flask import Flask, render_template, url_for, flash, redirect
import folium
from folium.plugins import MarkerCluster
import pandas as pd
import math
# Import from forms script
from forms import MapSeachForm

# import from scripts folder
from backend import map_state

############ flask app begins ############
app = Flask(__name__)

app.config['SECRET_KEY'] = "78f4d2ca06b3f9af87f963826c69e7e7"

@app.route('/', methods=['GET','POST'])
def index():
    form = MapSeachForm()
    if form.validate_on_submit():
        flash(f'Searching for hospitals in {form.state_name.data}')
        map_state(form.state_name.data)
        return redirect(url_for('map'))
    return render_template('index.html', form=form)
    #form.state_name

    # ORIGINAL BEGINS... not working
    #search = MapSeachForm(request.form)
    #if request.method == 'POST':
    #    return search_results(search)
    #return render_template('index.html', form=search)
    #return "This will be a search bar"
    # ORIGINAL ENDS... not working

# Create an index url to prevent not found 404 error
@app.route('/map', methods=['GET','POST'])
# Define the function for the route
def map():

    render_template('map.html')

    #return map._repr_html_()

    #return my_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
