from flask import Flask, render_template, request, session, redirect, jsonify, \
    url_for, flash

# from sqlalchemy import create_engine, asc, desc, \
#     func, distinct
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.serializer import loads, dumps

# from database_setup import Base, Things
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
# Connect to database and create database session
# engine = create_engine('sqlite:///flaskstarter.db')
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()


# Display all things

@app.route('/main')
def mainRender():
    cards = main.getAllCards()
    completed = main.cardsCompleted(cards)
    totalcards = len(cards)
    opencards = totalcards-completed
    db = database.Database()
    leaderboards = db.leaderboards()
    badges = db.userBadges()
    userData = db.getUser()
    points = db.getPoints()
    members = main.getAllMembers()
    return render_template('/main/main.html',members=members, points = points, users = userData, badges=badges, cards=cards, completed=completed, totalcards=totalcards, opencards=opencards, leaderboards=leaderboards, user = "tylergel")





@app.route('/login')
def login():
    github = OAuth2Session('a1b402ff2cc40ab7a947993eb3a08d25')
    authorization_url, state = github.authorization_url('https://trello.com/1/authorize?callback_method=callback&return_url=https://python-app-flask.herokuapp.com/callback&expiration=never&name=TrelloGamification&response_type=token&key=a1b402ff2cc40ab7a947993eb3a08d25')

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect('https://trello.com/1/authorize?callback_method=callback&return_url=https://python-app-flask.herokuapp.com/callback&expiration=never&name=TrelloGamification&response_type=token&key=a1b402ff2cc40ab7a947993eb3a08d25')

@app.route('/callback')
def callback():
    return render_template('/main/loggedin.html', url=request.path, url2=request.url_rule)


@app.route('/')
def mainRenderHome():
    return mainRender()

@app.route('/challenges')
def challengesRender():
    db = database.Database()
    badges = db.userBadges()
    challenges = db.getChallenges()
    userData = db.getUser()
    return render_template('/challenges/challenges.html', badges=badges, users=userData)

@app.route('/admin')
def adminRender():
    db = database.Database()
    badges = db.getBadges()
    userData = db.getUser()
    users = db.getUsers()
    points = db.getPoints()
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
