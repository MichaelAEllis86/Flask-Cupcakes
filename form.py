from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired,Optional,NumberRange,URL, AnyOf


class AddCupcakeForm(FlaskForm):
    """form model to add a new cupcake"""

    flavor=StringField("Flavor", validators=[InputRequired(message="This field is required, please add a flavor")])
    image=StringField("Photo url",validators=[InputRequired(message="This field is required, please add an image"), URL(require_tld=False, message="please enter a valid URL for your Cupcake photo")])
    size=StringField("Size",validators=[InputRequired(message="This field is required, please add a size of small, medium, or large"), AnyOf(values=["small","medium","large"],message="Size must be small medium or large. We are so VERY selective")])
    rating=FloatField("Rating", validators=[NumberRange(min=1, max=10, message="Rating this Cupcake from 1.0 to 10.0,")])


