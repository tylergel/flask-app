from flask import Flask, render_template, request, redirect, session, jsonify, \
    url_for, flash

import requests
import json
import database

def getBoardIdsList() :
    boards_list = database.Database().getBoards()
    boards = requests.get("https://api.trello.com/1/members/me/boards?key=a1b402ff2cc40ab7a947993eb3a08d25&token="+session.get('trellotoken'))
    todos = json.loads(boards.text)
    boardids = []
    for todo in todos:
        if todo['url'] in boards_list :
            boardids.append(todo['id'])
    return boardids

def getAllMembers() :
    boardids = getBoardIdsList()
    membersList = []
    for b_id in boardids :
        members_call = requests.get("https://api.trello.com/1/boards/ixJgFgCW/members?key=a1b402ff2cc40ab7a947993eb3a08d25&token="+session.get('trellotoken'))
        members = json.loads(members_call.text)
        for member in members :
            membersList.append(member)
    return membersList

def getAllCards() :
 boardids = getBoardIdsList()
 cards = [];
 for b_id in boardids :
     url = "https://api.trello.com/1/boards/"+str(b_id)+"/cards?key=a1b402ff2cc40ab7a947993eb3a08d25&token="+session.get('trellotoken')
     allCards = requests.get(url)
     allCards = json.loads(allCards.text)
     for card in allCards  :
         cards.append(card)
 return cards

def cardsAssigned(cards) :
  cardsAssigned = [];
  for card in cards :
      if session.get('id') in card['idMembers'] :
        cardsAssigned.append(card)
  return cardsAssigned


def cardsCompleted(cards)  :
  completed  = 0;
  for card in cards :
      if card['dueComplete']  :
          completed += 1
  return(completed);
