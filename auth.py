import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import database

bp = Blueprint('auth', __name__, url_prefix='/auth')

# https://flask.palletsprojects.com/en/1.1.x/tutorial/views/ Used some boilerplate code from here


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmPass']
        db = database.Database()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not password == confirm_password:
            error = 'Passwords do not match'
        elif db.select(
            "SELECT id FROM users WHERE username = '{}'".format(username)
        ) is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.insert(
                "INSERT INTO users (username, password) VALUES ('"+username+"', '"+generate_password_hash(password)+"')"
            )
            # come back to this; db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('/auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = database.Database()
        error = None
        user = db.select(
            "SELECT * FROM users WHERE username = '{}'".format(username)
        )

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()  # stores user data into an encrypted cookie
            session['user_id'] = user['id']
            return redirect(url_for('main'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request # will run every time a new url is loaded
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = database.Database().select(
            "SELECT * FROM users WHERE id = '{}'".format(user_id)
        )


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homePages.homePage'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
