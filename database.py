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
    def getRecentBadges(self):
        self.cur.execute("SELECT * FROM user_badges INNER JOIN badges ON user_badges.badge_id INNER JOIN users on user_badges.account_id=users.id Order by user_badges.dateLastActivity DESC")
        result = self.cur.fetchall()
        return result
    def getUser(self, userid):
        self.cur.execute("SELECT * FROM users WHERE id = "+str(userid))
        result = self.cur.fetchall()
        return result
    def getUsers(self):
        self.cur.execute("SELECT * FROM users order by points DESC")
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
        self.cur.execute("DELETE FROM badges WHERE ID = "+str(badge_id))
        self.cur.execute("DELETE FROM user_badges WHERE badge_id = "+str(badge_id))
        return ""
    def deleteBoard(self, board_id):
        self.cur.execute("DELETE FROM company_boards WHERE id = "+board_id)
        return ""
    def deleteList(self, list_id):
        self.cur.execute("DELETE FROM completed_lists WHERE id = "+list_id)
        return ""
    def clearBadgesFromUser(self, userid):
        self.cur.execute("DELETE FROM user_badges WHERE account_id = "+userid)
        return ""
    def addBadge(self, icon, name, points, description, color):
        self.cur.execute("INSERT INTO badges (icon, name, points, description, color) VALUES ('"+icon+"', '"+name+"', '"+points+"', '"+description+"', '"+color+"')")
        return ""
    def addList(self, name, list_id):
        self.cur.execute("INSERT INTO completed_lists (name, list_id) VALUES ('"+name+"', '"+list_id+"')")
        return ""
    def addBoard(self, board):
        self.cur.execute("INSERT INTO company_boards (url) VALUES ('"+board+"')")
        return ""
    def addPointsDist(self, ppc):
        self.cur.execute("INSERT INTO points_distribution (ppc) VALUES ('"+ppc+"')")
        return ""
    def addBadgeToUser(self, userid, badgeid):
        self.cur.execute("INSERT INTO user_badges (account_id, badge_id, completed) VALUES ('"+userid+"', '"+badgeid+"', 1)")
        return ""
    def getPointsDistribution(self):
        self.cur.execute("SELECT * FROM points_distribution order by id DESC")
        result = self.cur.fetchall()
        return result[0]

    def getBoards(self) :
        self.cur.execute("SELECT * FROM company_boards WHERE 1")
        result = self.cur.fetchall()
        boards = []
        for board in result :
            board_array = []
            board_array.append(board['id'])
            board_array.append(board['url'])
            boards.append(board_array)
        return boards
    def getTrelloToken(self, user_id) :
        rows = self.cur.execute("SELECT * from user_tokens where app_id='{}' and user_id='{}'".format('1', user_id))
        result = self.cur.fetchall()
        if rows < 1 :
            return ""
        return result[0]['token']
    def getCompletedLists(self) :
        self.cur.execute("SELECT * from completed_lists")
        result = self.cur.fetchall()
        return result
    def getNotifications(self, user_id) :
        self.cur.execute("SELECT * from notifications WHERE user_id = '"+str(user_id)+"'")
        result = self.cur.fetchall()
        return result

    def getMessages(self, user_id) :
        self.cur.execute("SELECT * from messages WHERE user_id = '"+str(user_id)+"'")
        result = self.cur.fetchall()
        return result

    def getMessages(self, user_id) :
        self.cur.execute("SELECT * from messages WHERE user_id = '"+str(user_id)+"'")
        result = self.cur.fetchall()
        return result
    def getPointsOfUser(self, userid) :
        self.cur.execute("SELECT SUM(points) as total FROM user_badges INNER JOIN badges ON user_badges.badge_id = badges.id WHERE account_id = '"+str(userid)+"' AND completed =1")
        result = self.cur.fetchall()
        user_badges_points = result[0]['total']
        completed = main.cardsCompleted(main.cardsAssigned(main.getAllCards()))
        points_distribution = Database().getPointsDistribution()
        if completed is None :
            completed = 0
        if user_badges_points is None :
            user_badges_points = 0
        if points_distribution['ppc'] is None :
            points_distribution['ppc'] = 0
        completed_points = int(points_distribution['ppc']) * int(completed)
        total_points = int(completed_points) + int(user_badges_points)
        self.cur.execute("UPDATE users SET points= "+str(total_points)+" WHERE id = '"+str(userid)+"'")
        return total_points
