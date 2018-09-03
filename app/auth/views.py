# app/auth/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

from . import auth
from .forms import LoginForm, RegistrationForm, EditForm
from .. import db
from ..models import UserAccount

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)
		
@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an UserAccount to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        userAccount = UserAccount(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # add UserAccount to the database
        db.session.add(userAccount)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an UserAccount in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

         # check whether userAccount exists in the database and whether
        # the password entered matches the password in the database
        userAccount = UserAccount.query.filter_by(email=form.email.data).first()
        if userAccount is not None and userAccount.verify_password(
                form.password.data):
            # log userAccount in
            login_user(userAccount)

            # redirect to the appropriate dashboard page
            if userAccount.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')
    # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an UserAccount out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))
@auth.route('/edits', methods=['GET', 'POST'])
@login_required
def list_user():
    """
    List all books
    """
    check_admin()
    useraccount = UserAccount.query.all()

    return render_template('/auth/edits.html',
                           useraccount=useraccount, title="User")
@auth.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_user():
    """
    Edit information
    """
    useraccount = UserAccount.query.get_or_404(current_user.id)
    form = EditForm(obj=useraccount)
    
    if form.validate_on_submit():
	    #userAccount = UserAccount.query.filter_by(email=form.email.data).first()
	    if useraccount.verify_password(form.password.data):
             useraccount.first_name = form.first_name.data
             useraccount.last_name = form.last_name.data
             db.session.commit()
             flash('Changes have been saved.')

        # redirect to the dashboard
             return redirect(url_for('home.dashboard'))
	    else:
             flash('Incorrect Password!')
    form.first_name.data = useraccount.first_name
    form.last_name.data = useraccount.last_name
    return render_template('auth/edit.html', form=form, title='Edit Account')
@auth.route('/admin_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_other_user(id):
    """
    Edit information
    """
    useraccount = UserAccount.query.get_or_404(id)
    form = EditForm(obj=useraccount)
    
    if form.validate_on_submit():
	    #userAccount = UserAccount.query.filter_by(email=form.email.data).first()
	    if useraccount.verify_password(form.password.data):
             useraccount.first_name = form.first_name.data
             useraccount.last_name = form.last_name.data
             db.session.commit()
             flash('Changes have been saved.')
        # redirect to the dashboard
             return redirect(url_for('auth.list_user'))
	    else:
             flash('Incorrect Password!')
    form.first_name.data = useraccount.first_name
    form.last_name.data = useraccount.last_name
    return render_template('auth/edit.html', form=form, title='Edit Account')