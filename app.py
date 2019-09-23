from flask import Flask, render_template, request, redirect, jsonify, \
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
import config
app = Flask(__name__)


# Connect to database and create database session
# engine = create_engine('sqlite:///flaskstarter.db')
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()


# Display all things
@app.route('/')
def showMain():
    return render_template('')

@app.route('/main')
def main():
    cards = getAllCards()
    completed = cardsCompleted(cards)
    totalcards = len(cards)
    opencards = totalcards-completed
    db = Database()
    leaderboards = db.leaderboards()

    return render_template('/main/main.html', cards=cards, completed=completed, totalcards=totalcards, opencards=opencards, leaderboards=leaderboards, user = "tylergel")


def getAllCards() :
    boards = requests.get("https://api.trello.com/1/members/me/boards?key=a1b402ff2cc40ab7a947993eb3a08d25&token=c8d1532f8550418cf8f334f6e6bb957353c556d6499e973cfb41df821530fd0d")
    todos = json.loads(boards.text)
    boardids = []
    for todo in todos:
        boardids.append(todo['id'])
    cards = [];
    for b_id in boardids :
        url = "https://api.trello.com/1/boards/"+str(b_id)+"/cards?key=a1b402ff2cc40ab7a947993eb3a08d25&token=c8d1532f8550418cf8f334f6e6bb957353c556d6499e973cfb41df821530fd0d"
        allCards = requests.get(url)
        allCards = json.loads(allCards.text)
        for card in allCards  :
            cards.append(card)
    return cards


def cardsCompleted(cards)  :
     completed  = 0;
     for card in cards :
         if card['dueComplete']  :
             completed += 1
     return(completed);


class Database:
    def __init__(self):

        self.con = pymysql.connect(host=config.host, user=config.user, password=config.password, db=config.db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
    def leaderboards(self):
        self.cur.execute("SELECT * FROM leaderboards ORDER BY cardsCompleted DESC")
        result = self.cur.fetchall()
        index = -1
        newlist = []
        for rank in result :
            index = index + 1
            if rank['name'] == 'tylergel' :
                newlist.append(result[index-1])
                newlist.append(result[index])
                newlist.append(result[index+1])

        return newlist