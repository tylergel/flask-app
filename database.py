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
import main
import os

class Database:
    def __init__(self):
        # host = os.environ.get('host')
        # user = os.environ.get('user')
        # password=os.environ.get('password')
        # db=os.environ.get('db')
        host = "107.180.27.226"
        user = "tylergel"
        password = "tylergel"
        db = "gammification"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
    def insert(self, statement) :
        res = self.cur.execute(statement)
        self.con.commit()
        return res
    def select(self, statement) :
        self.cur.execute(statement)
        result = self.cur.fetchone()
        return result
    def selectall(self, statement) :
        self.cur.execute(statement)
        result = self.cur.fetchall()
        return result
    def userBadges(self, userid):
        self.cur.execute("SELECT * FROM user_badges INNER JOIN badges ON user_badges.badge_id = badges.id WHERE account_id = " + str(userid))
        result = self.cur.fetchall()
        return result
    def getBadges(self):
        self.cur.execute("SELECT * FROM badges")
        result = self.cur.fetchall()
        return result
    def getUser(self, userid):
        self.cur.execute("SELECT * FROM users WHERE id = "+str(userid))
        result = self.cur.fetchall()
        return result
    def getUsers(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        newresult = []
        for user in result :
            newuser = []
            newuser = user
            newuser['badges'] = self.userBadges(user['id'])
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
    def getPoints(self, userid):
        self.cur.execute("SELECT SUM(points) as total FROM user_badges INNER JOIN badges ON user_badges.badge_id = badges.id WHERE account_id = '"+str(userid)+"' AND completed =1")
        result = self.cur.fetchall()
        return result[0]['total']
    def updateUser(self, user, memberid, token) :
        self.cur.execute("INSERT INTO users (name, memberid, token) VALUES ('"+user+"', '"+memberid+"', '"+token+"')")
        self.cur.execute("SELECT * from users WHERE name = '"+user+"'")
        result = self.cur.fetchall()
        return result[0]['id']
    def getBoards(self) :
        self.cur.execute("SELECT url FROM company_boards WHERE 1")
        result = self.cur.fetchall()
        boards = []
        for board in result :
            boards.append(board['url'])
        return boards
