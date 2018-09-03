# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

from . import admin
from .forms import BooksForm, BookAssignForm
from .. import db
from ..models import Books, BookOrder

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# Book Views


@admin.route('/books', methods=['GET', 'POST'])
@login_required
def list_books():
    """
    List all books
    """
    check_admin()

    books = Books.query.all()

    return render_template('/admin/books/books.html',
                           books=books, title="Books")


@admin.route('/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    """
    Add a book to the database
    """
    check_admin()

    add_book = True

    form = BooksForm()
    if form.validate_on_submit():
        books = Books(name=form.name.data, author=form.author.data,
				stock=form.stock.data)
        try:
            # add book to the database
            db.session.add(books)
            db.session.commit()
            flash('You have successfully added a new book.')
        except:
            # in case book name already exists
            flash('Error: book name already exists.')

        # redirect to books page
        return redirect(url_for('admin.list_books'))

    # load book template
    return render_template('admin/books/book.html', action="Add",
                           add_book=add_book, form=form,
                           title="Add Book")


@admin.route('/books/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    """
    Edit a book
    """
    check_admin()

    add_book = False

    book = Books.query.get_or_404(id)
    form = BooksForm(obj=book)
    if form.validate_on_submit():
        book.name = form.name.data
        book.author = form.author.data
        book.stock = form.stock.data
        db.session.commit()
        flash('You have successfully edited the book.')

        # redirect to the books page
        return redirect(url_for('admin.list_books'))

    form.name.data = book.name
    form.author.data = book.author
    form.stock.data = book.stock
    return render_template('admin/books/book.html', action="Edit",
                           add_book=add_book, form=form,
                           book=book, title="Edit Book")


@admin.route('/books/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_book(id):
    """
    Delete a book from the database
    """
    check_admin()

    book = Books.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('You have successfully deleted a book.')

    # redirect to the books page
    return redirect(url_for('admin.list_books'))

    return render_template(title="Delete Book")
# Employee Views

@admin.route('/useraccounts')
@login_required
def list_useraccounts():
    """
    List all user
    """
    check_admin()

    useraccount = UserAccount.query.all()
    return render_template('admin/useraccounts/useraccounts.html',  #reminder
                           useraccount=useraccount, title='Users')
#BookOrder View
@admin.route('/bookorders')
@login_required
def list_bookorders():
    """
    List all user
    """
    check_admin()
    books = Books.query.all()
    bookorder = BookOrder.query.all()
    return render_template('admin/bookorder/bookorders.html',  #reminder
                           bookorder=bookorder, books = books, title='Transactions')