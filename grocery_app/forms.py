from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from grocery_app.models import GroceryStore

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    title = StringField("Title",validators=[DataRequired(message="You Must Enter a Store Name!")])
    address = StringField("Address",validators=[DataRequired(message="You Must Enter an Address")])
    submit = SubmitField("Submit")
    

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField("name",validators=[DataRequired(),Length(min=2,max=50,message="The name must be between 2 and 50 characters.")])
    price = FloatField('price',validators=[DataRequired()])
    category = SelectField("category",choices=[
        ('PRODUCE','Produce'),
        ('DELI','Deli'),
        ('BAKERY','Bakery'),
        ('PANTRY','Pantry'),
        ('FROZEN','Frozen'),
        ('OTHER','Other')])
    photo_url = StringField("photo_url",validators=[URL(message="Must be a URL")])
    store = QuerySelectField("store",query_factory=lambda: GroceryStore.query, get_label='title')
    submit = SubmitField("Submit")
