# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class UserAccount(UserMixin, db.Model):
    """
    Create an UserAccount table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'userAccount'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

	#Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return UserAccount.query.get(int(user_id))
class Books(db.Model):
    """
    Create a Books table
    """

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    author = db.Column(db.String(200))
    isbn = db.Column(db.String(200))
    stock = db.Column(db.Integer)
def __repr__(self):
        return '<books: {}>'.format(self.name)
class BookOrder(db.Model):
	"""
	Create a BookOrder Table
	"""
	
	__tablename__= 'bookOrder'
	id = db.Column(db.Integer, primary_key=True)
	books_id = db.Column(db.Integer, db.ForeignKey('books.id'))
	books_name = db.Column(db.String(200), db.ForeignKey('books.name'))
	userAccount_id = db.Column(db.Integer, db.ForeignKey('userAccount.id'))
	userAccount_username = db.Column(db.String(200), db.ForeignKey('userAccount.username'))
	amount = db.Column(db.Integer)
def __repr__(self):
		return '<orders: {}>'.format(self.name)