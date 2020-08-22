from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Optional, Length

class MapSeachForm(FlaskForm):
    #STATE_NAME feature from dataset
    # DataRequired means it can't be empty
    state_name = StringField('STATE_NAME',
                    validators=[Optional(), Length(min=4, max=20)])
    #HQ_CITY feature from dataset
    city_name =  StringField('HQ_CITY',
                    validators=[Optional(), Length(min=4, max=20)])
    #HQ_ZIP_CODE
    # Currently not used
    zip_code = StringField('HQ_ZIP_CODE',
                    validators=[Optional(), Length(min=5, max=5)])
    #COUNTY_NAME
    # Not implemented yet
    county_name = StringField('COUNTY_NAME',
                    validators=[Optional(), Length(min=4, max=20)])

    submit = SubmitField("Search")

#HOSPITAL_TYPE # Not sure about this one
