# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
# update imports
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Books, BookOrder


class BooksForm(FlaskForm):
    """
    Form for admin to add or edit a book
    """
    name = StringField('Name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    stock =  IntegerField('Number of Books', validators=[DataRequired()])
    submit = SubmitField('Submit')
class BookAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    books = QuerySelectField(query_factory=lambda: Books.query.all(),
                                  get_label="name")
    submit = SubmitField('Submit')