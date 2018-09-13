# app/home/views.py

from flask import abort, render_template,flash, redirect, url_for
from flask_login import current_user, login_required
from .. import db
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
# update imports
#from forms import BookOrderForm
from ..models import BookOrder, Books
from . import home

class BookOrderForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    books_name = QuerySelectField(query_factory=lambda: Books.query,
                                  get_label="name",get_pk=lambda x: x.id)
    amount = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')
@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")
# add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")
def edit_account():
    """
    Edit account
    """
    useraccount = UserAccount.query.get_or_404(id)
    form = RegistrationForm(obj=useraccount)
    if form.validate_on_submit():
        useraccount.email = form.email.data
        useraccount.first_name = form.first_name.data
        useraccount.last_name = form.last_name.data
        useraccount.password = form.password.data
        useraccount.confirm_password = form.confirm_password.data
        db.session.commit()
        flash('Edit Success.')

        # redirect to the books page
        return redirect(url_for('dashboard'))

    form.email.data = useraccount.email
    form.first_name.data = useraccount.first_name
    form.last_name.data = useraccount.last_name
    form.password.data =  useraccount.password
    useraccount.confirm_password = form.confirm_password.data
    return render_template('dashboard.html')
@home.route('/bookorders', methods=['GET', 'POST'])
@login_required
def book_orders():
    form = BookOrderForm()
    if form.validate_on_submit():
        
        bookorder = BookOrder(books_name=form.books_name.data.name, books_id=form.books_name.data.id,
							userAccount_username=current_user.username, userAccount_id=current_user.id,
							amount=form.amount.data)
        db.session.add(bookorder)
        db.session.commit()
        flash('You have successfully ordered the book.')
        return redirect(url_for('home.dashboard'))
    return render_template('home/bookorders.html', form=form,
                           title='Borrow Books')