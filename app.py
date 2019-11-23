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
    cards = main.cardsAssigned(main.getAllCards())
    completed = main.cardsCompleted(cards)
    totalcards = len(cards)
    opencards = totalcards-completed
    db = database.Database()
    badges = db.userBadges(session.get('user_id'))
    userData = db.getUser(session.get('user_id'))
    points = db.getPointsOfUser(session.get('user_id'))
    users=db.getUsers()
    for index, user in enumerate(users) :
        users[index]['rank'] = (index + 1)
    members = main.getAllMembers()
    return render_template('/main/main.html', allusers=users, members=members, points = points, users = userData, badges=badges, cards=cards, completed=completed, totalcards=totalcards, opencards=opencards, username=session.get('user'))

@app.route('/')
def mainRenderHome():
    return mainRender()

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
    return redirect(url_for('delete'))

@app.route('/deleteboard')
def deleteBoard():
    db = database.Database()
    board_id = request.args.get('data', 0, type=str)
    db.deleteBoard(board_id)
    return redirect(url_for('delete'))

@app.route('/deletelist')
def deleteList():
    db = database.Database()
    list_id = request.args.get('data', 0, type=str)
    db.deleteList(list_id)
    return redirect(url_for('delete'))

@app.route('/addbadge')
def addBadge():
    db = database.Database()
    icon = request.args.get('icon')
    name = request.args.get('name')
    points = request.args.get('points')
    description = request.args.get('description')
    db.addBadge(icon, name, points, description)
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
    return redirect('/admin')
