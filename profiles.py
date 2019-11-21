import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import database

bp = Blueprint('profiles', __name__, url_prefix='/bio')


@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    db = database.Database()
    apps = db.selectall(
        "SELECT * from apps"
    )
    user = db.selectall(
        "SELECT * FROM users WHERE id = '{}'".format(session.get('user_id'))
    )
    tokenlist = {}
    for app in apps :
        tokenlist[app['app']] =session.get(app['app'])
    if request.method == 'POST':
        for app in apps :
            if  request.form[app['app']]:
                checkrecord = db.select(
                    "SELECT 1 FROM user_tokens WHERE app_id='{}' and user_id = '{}'".format(app['id'], session.get('user_id'))
                )
                if checkrecord is None :
                    db.insert(
                        "INSERT INTO user_tokens (token, app_id, user_id) VALUES ('{}', '{}', '{}')".format(request.form[app['app']], app['id'], session.get('user_id'))
                    )
                else :
                    db.insert(
                        "UPDATE user_tokens SET token = '{}' WHERE app_id ='{}' and user_id='{}'".format(request.form[app['app']], app['id'], session.get('user_id'))
                    )


        return render_template('profiles/profile.html',tokenlist=tokenlist, apps=apps,  user=user)


    return render_template('profiles/profile.html',tokenlist=tokenlist, apps=apps,  user=user)
