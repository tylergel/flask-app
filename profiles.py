import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import database
import main
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

    # Header stuff
    notifications = main.getNotifications()
    messages = main.getMessages()
    userData = db.getUser(session.get('user_id'))
    users=db.getUsers()
    #End header stuff
    return render_template('profiles/profile.html',notifications=notifications, messages=messages, users=userData, tokenlist=tokenlist, apps=apps,  user=user[0])

@bp.route('/activity', methods=['GET', 'POST'])
def activity() :
    if session.get('user_id') is None:
        return redirect(url_for("auth.login"))
    if session.get('trello') == "" or session.get('trello') is None:
        return redirect(url_for("profiles.profile"))

    db = database.Database()
    # Header stuff
    notifications = main.getNotifications()
    messages = main.getMessages()
    userData = db.getUser(session.get('user_id'))
    users=db.getUsers()
    #End header stuff

    allcards = main.getAllCards()
    cards = main.cardsAssigned(allcards)
    completed = main.cardsCompleted(cards)
    totalcards = len(cards)
    opencards = totalcards-completed
    badges = db.userBadges(session.get('user_id'))
    points = db.getPointsOfUser(session.get('user_id'))
    recentCompletedCards = main.cardsCompletedList(allcards)
    recentCompletedCards.sort(key = lambda recentCompletedCards: recentCompletedCards['dateLastActivity'])
    recentCompletedBadges = db.getRecentBadges()
    totallist=recentCompletedCards + recentCompletedBadges
    totallist.sort(key = lambda totallist: totallist['dateLastActivity'])
    feed = []
    i = 0
    members = main.getAllMembers()
    totallist.reverse()
    for item in totallist :
        i = i + 1
        if i > 25 :
            break
        newitem = []
        newitem.append(item['name'])
        if 'username' in item :
            newitem.append(item['username'])
        else :
            this_username = ""
            for trellomember in item['idMembers'] :
                for member in members :
                    if trellomember == member['id'] :
                        this_username = this_username + member['username'] +", "
            this_username = this_username[:-3]
            newitem.append(this_username)
        newitem.append(item['dateLastActivity'])
        feed.append(newitem)
    for index, user in enumerate(users) :
        users[index]['rank'] = (index + 1)

    return render_template('/profiles/activity.html', users = userData, notifications=notifications, messages=messages, feed=feed,test=totallist, allusers=users, members=members, points = points, badges=badges, cards=cards, completed=completed, totalcards=totalcards, opencards=opencards, username=session.get('user'))

