from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Optional, Length
import re

def process_input(user_input):
    '''
    Returns the processed user input string where the first letter of every
    word is always a capital letter so it matches the dataset
    Parameters:
    user_input (string): user input location search
    '''

    # Return None when there is no input

    lower_input = user_input.lower()

    input_list = re.split(r'\s',lower_input)

    output_str = ""

    # White spaces should be 1 less than how many words
    ws_qty = len(input_list) - 1
    ws_count = 0

    if len(input_list) > 1:

        for elem in input_list:

            # Make capital only the first letter of every word
            output_str += elem[0].upper()

            # Concatenate the rest of the word
            output_str += elem[1::]

            # Add a whitepace to the string if not in the last word of the list
            if ws_count < ws_qty:
                output_str += " "
                ws_count+= 1
    else:
        output_str = lower_input[0].upper() + lower_input[1::]

    return output_str


class MapSearchForm(FlaskForm):
    #STATE_NAME feature from dataset
    # DataRequired means it can't be empty
    state_name = StringField('STATE_NAME',
                    validators=[Optional(), Length(min=4, max=20)])

    #HQ_CITY feature from dataset
    city_name =  StringField('HQ_CITY',
                    validators=[Optional(), Length(min=4, max=20)])

    #HQ_ZIP_CODE
    zip_code = StringField('HQ_ZIP_CODE',
                    validators=[Optional(), Length(min=5, max=5)])
    #COUNTY_NAME
    # Not implemented yet
    county_name = StringField('COUNTY_NAME',
                    validators=[Optional(), Length(min=4, max=20)])

    submit = SubmitField("Search")

#HOSPITAL_TYPE # Not sure about this one
