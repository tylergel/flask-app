from flask import Flask,Blueprint, render_template, request, session, redirect, jsonify, \
    url_for, flash

import requests
import random
import string
import logging
import json
import pymysql
from requests_oauthlib import OAuth2Session
import main
import database
app = Flask(__name__)
app.secret_key = "c8d1532f8550418cf8f334f6e6bb957353c556d6499e973cfb41df821530fd0d"


import auth
app.register_blueprint(auth.bp, url_prefix='/auth')
import profiles
app.register_blueprint(profiles.bp, url_prefix='/profiles')
@app.route('/')
def start():
    return mainRender()

@app.route('/main')
def mainRender():
    cards = main.cardsAssigned(main.getAllCards())
    completed = main.cardsCompleted(cards)
    totalcards = len(cards)
    opencards = totalcards-completed
    db = database.Database()
    badges = db.userBadges(session.get('user_id'))
    userData = db.getUser(session.get('user_id'))
    points = db.getPoints(session.get('user_id'))
    members = main.getAllMembers()
    return render_template('/main/main.html', fff=session, members=members, points = points, users = userData, badges=badges, cards=cards, completed=completed, totalcards=totalcards, opencards=opencards, username=session.get('user'))

# @app.route('/login')
# def login():
#     github = OAuth2Session('a1b402ff2cc40ab7a947993eb3a08d25')
#     authorization_url, state = github.authorization_url('https://trello.com/1/authorize?callback_method=callback&return_url=localhost/loggedin&expiration=never&name=TrelloGamification&response_type=token&key=a1b402ff2cc40ab7a947993eb3a08d25')
#     session['oauth_state'] = state
#     return redirect('https://trello.com/1/authorize?callback_method=callback&return_url=localhost/loggedin/&expiration=never&name=TrelloGamification&response_type=token&key=a1b402ff2cc40ab7a947993eb3a08d25')

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

@app.route('/admin')
def adminRender():
    db = database.Database()
    badges = db.getBadges()
    userData = db.getUser(session.get('user_id'))
    users = db.getUsers()
    points = db.getPoints(session.get('user_id'))
    return render_template('/admin/admin.html', badges=badges, users=userData, allusers=users, points=points)

@app.route('/profile')
def profileRender():
    return render_template('/profile/profile.html')

@app.route('/deletebadge')
def deleteBadge():
    db = database.Database()
    badge_id = request.args.get('data', 0, type=str)
    db.deleteBadge(badge_id)
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

@app.route('/addbadgetouser')
def addBadgeToUser():
    db = database.Database()
    userid = request.args.get('userid')
    badgeid = request.args.get('badgeid')
    db.addBadgeToUser(userid, badgeid)
    return adminRender()
