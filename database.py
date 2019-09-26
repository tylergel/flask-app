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
import main

class Database:
    def __init__(self):
        host = config.host
        user = config.user
        password=config.password
        db=config.db
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
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
    def userBadges(self):
        self.cur.execute("SELECT * FROM user_badges INNER JOIN badges ON user_badges.badge_id = badges.id WHERE account_id = 1")
        result = self.cur.fetchall()
        return result
    def getBadges(self):
        self.cur.execute("SELECT * FROM badges")
        result = self.cur.fetchall()
        return result
    def getUser(self):
        self.cur.execute("SELECT * FROM users WHERE id = 1")
        result = self.cur.fetchall()
        return result
    def getUsers(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        newresult = []
        for user in result :
            newuser = []
            newuser = user
            newuser['badges'] = self.userBadges()
            newresult.append(newuser)
        return newresult
    def getChallenges(self):
        self.cur.execute("SELECT * FROM challenges WHERE id = 1")
        result = self.cur.fetchall()
        return result
    def deleteBadge(self, badge_id):
        self.cur.execute("DELETE FROM badges WHERE ID = "+badge_id)
        return ""
    def addBadge(self, icon, name, points, description):
        self.cur.execute("INSERT INTO badges (icon, name, points, description) VALUES ('"+icon+"', '"+name+"', '"+points+"', '"+description+"')")
        return ""
    def addBadgeToUser(self, userid, badgeid):
        self.cur.execute("INSERT INTO user_badges (account_id, badge_id, completed) VALUES ('"+userid+"', '"+badgeid+"', 1)")
        return ""
    def getPoints(self):
        self.cur.execute("SELECT SUM(points) as total FROM user_badges INNER JOIN badges ON user_badges.badge_id = badges.id WHERE account_id = 1 AND completed =1")
        result = self.cur.fetchall()
        return result[0]['total']
