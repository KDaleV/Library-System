# app/admin/forms.py

# update imports
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from ..models import BookOrder

# existing code remains

class BookOrderForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    books_name = QuerySelectField(query_factory=lambda: Books.query.all(),
                                  get_label="name")
    amount = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')