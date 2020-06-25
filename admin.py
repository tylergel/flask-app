import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import database
import requests
import json
import main
bp = Blueprint('admin', __name__, url_prefix='/admin')

# https://flask.palletsprojects.com/en/1.1.x/tutorial/views/ Used some boilerplate code from here


@bp.route('/', methods=('GET', 'POST'))
def adminRender():
    if session.get('user_id') is None:
        return redirect(url_for("auth.login"))
    if session.get('trello') == "" or session.get('trello') is None:
        return redirect(url_for("profiles.profile"))
    user = session.get('user')
    if user['admin'] == 0 :
        return redirect(url_for("profiles.profile"))
    db = database.Database()
    badges = db.getBadges()
    # Header stuff
    notifications = main.getNotifications()
    messages = main.getMessages()
    userData = db.getUser(session.get('user_id'))
    users=db.getUsers()
    #End header stuff
    points = 0
    try :
        points = db.getPointsOfUser(session.get('user_id'))
    except :
        print("")
    boards = db.getBoards()
    lists = main.getLists()
    completed_lists = db.getCompletedLists()
    points_distribution = []
    try :
        points_distribution = db.getPointsDistribution()
    except:
        print("")
    currentuser = []
    user_id = request.args.get('user_id')
    for user in users :
        if user_id == str(user['id']) :
            currentuser = user
    return render_template('/admin/admin.html', messages=messages, notifications=notifications, points_distribution=points_distribution, currentuser=currentuser, completed_lists=completed_lists, lists=lists, boards=boards,trellousername=session.get('trellousername'), badges=badges, users=userData, allusers=users, points=points)
