from flask import Flask,Blueprint, render_template, request, session, redirect, jsonify, \
    url_for, flash

import requests
import random
import string
import logging
import json
import pymysql
import main
import database
app = Flask(__name__)
app.secret_key = "c8d1532f8550418cf8f334f6e6bb957353c556d6499e973cfb41df821530fd0d"


import auth
app.register_blueprint(auth.bp, url_prefix='/auth')

import profiles
app.register_blueprint(profiles.bp, url_prefix='/profiles')

import admin
app.register_blueprint(admin.bp, url_prefix='/admin')

@app.route('/')
def start():
    if session.get('user_id') is None:
        return redirect(url_for("auth.login"))
    if session.get('trello') == "" or session.get('trello') is None:
        return redirect(url_for("profiles.profile"))
    return mainRender()

@app.route('/main')
def mainRender():

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
    points = 0
    try :
        points = db.getPointsOfUser(session.get('user_id'))
    except :
        print("")
    users=db.getUsers()
    recentCompletedCards = main.cardsCompletedList(allcards)
    weeklycards, dates = main.getWeeklyCards(recentCompletedCards)
    recentCompletedCards.sort(key = lambda recentCompletedCards: recentCompletedCards['dateLastActivity'])
    recentCompletedBadges = db.getRecentBadges()
    totallist= list(recentCompletedCards) + list(recentCompletedBadges)
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

    return render_template('/main/index.html', users = userData,  messages=messages,notifications=notifications, dates=dates, weeklycards=weeklycards,feed=feed,test=totallist, allusers=users, members=members, points = points, badges=badges, cards=cards, completed=completed, totalcards=totalcards, opencards=opencards, username=session.get('user'))

@app.route('/cards')
def cards():
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

    card_type = request.args.get('card_type', default='', type=str)

    cards_return = []
    allcards = main.getAllCards()
    allcards = main.cardsAssigned(allcards)
    if card_type == 'total' :
        cards_return = allcards
    elif card_type == 'completed' :
        cards_return = main.cardsCompletedList(allcards)
    elif card_type == 'open' :
        cards_return = main.getOpenCards(allcards)



    users=db.getUsers()
    recentCompletedCards = main.cardsCompletedList(allcards)
    weeklycards, dates = main.getWeeklyCards(recentCompletedCards)

    return render_template('/main/cards.html', card_type=card_type, users = userData,  messages=messages,notifications=notifications, dates=dates, weeklycards=weeklycards, allusers=users, cards=cards_return, username=session.get('user'))

@app.route('/')
def mainRenderHome():
    return mainRender()

@app.route('/leaderboards')
def leaderboards() :
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

    for index, user in enumerate(users) :
        users[index]['rank'] = (index + 1)


    return render_template('/main/leaderboards.html', users = userData, notifications=notifications, messages=messages, allusers=users)


@app.route('/challenges')
def challengesRender():
    db = database.Database()
    badges = db.userBadges(session.get('user_id'))
    challenges = db.getChallenges()
    userData = db.getUser(session.get('user_id'))
    return render_template('/challenges/challenges.html', badges=badges, users=userData)

@app.route('/deletebadge')
def deleteBadge():
    db = database.Database()
    badge_id = request.args.get('data', 0, type=str)
    db.deleteBadge(badge_id)
    return redirect('/admin')

@app.route('/deleteboard')
def deleteBoard():
    db = database.Database()
    board_id = request.args.get('data', 0, type=str)
    db.deleteBoard(board_id)
    return redirect('/admin')

@app.route('/deletelist')
def deleteList():
    db = database.Database()
    list_id = request.args.get('data', 0, type=str)
    db.deleteList(list_id)
    return redirect('/admin')

@app.route('/clearuserbadges')
def clearBadgesFromUser():
    db = database.Database()
    userid = request.args.get('user_id')
    db.clearBadgesFromUser(userid)
    return redirect('/admin')

@app.route('/addbadge')
def addBadge():
    db = database.Database()
    icon = request.args.get('icon')
    name = request.args.get('name')
    points = request.args.get('points')
    description = request.args.get('description')
    color = request.args.get('color')
    db.addBadge(icon, name, points, description, color)
    return redirect('/admin')

@app.route('/addlist')
def addList():
    db = database.Database()
    listname = request.args.get('listname')
    listid = request.args.get('listid')
    db.addList(listname, listid)
    return redirect('/admin')

@app.route('/addpointsdist')
def addPointsDist():
    db = database.Database()
    ppc = request.args.get('ppc')
    db.addPointsDist(ppc)
    return redirect('/admin')

@app.route('/addboard')
def addBoard():
    db = database.Database()
    boardid = request.args.get('boardid')
    db.addBoard(boardid)
    return redirect('/admin')


@app.route('/addbadgetouser')
def addBadgeToUser():
    db = database.Database()
    userid = request.args.get('userid')
    badgeid = request.args.get('badgeid')
    db.addBadgeToUser(userid, badgeid)
    return redirect('/admin?user_id='+userid)
