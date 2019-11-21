from flask import Flask, render_template, request, redirect, session, jsonify, \
    url_for, flash

import requests
import json
import database

def getBoardIdsList() :
    boards_list = database.Database().getBoards()
    boards_list_url = []
    for boards_ in boards_list :
        boards_list_url.append(boards_[1])
    boards = requests.get("https://api.trello.com/1/members/me/boards?key=a1b402ff2cc40ab7a947993eb3a08d25&token="+session.get('trello'))
    todos = json.loads(boards.text)
    boardids = []
    for todo in todos:
        if todo['url'] in boards_list_url :
            boardids.append(todo['id'])
    return boardids

def getAllMembers() :
    boardids = getBoardIdsList()
    membersList = []
    for b_id in boardids :
        members_call = requests.get("https://api.trello.com/1/boards/"+str(b_id)+"/members?key=a1b402ff2cc40ab7a947993eb3a08d25&token="+session.get('trello'))
        members = json.loads(members_call.text)
        for member in members :
            membersList.append(member)
    return membersList

def getAllCards() :
 boardids = getBoardIdsList()
 cards = [];
 for b_id in boardids :
     url = "https://api.trello.com/1/boards/"+str(b_id)+"/cards?key=a1b402ff2cc40ab7a947993eb3a08d25&token="+session.get('trello')
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

def getLists() :
    boardids = getBoardIdsList()
    lists = []
    for b_id in boardids :
        lists_call = requests.get("https://api.trello.com/1/boards/"+str(b_id)+"/lists?key=a1b402ff2cc40ab7a947993eb3a08d25&token="+session.get('trello'))
        thelists = json.loads(lists_call.text)
        for list in thelists :
            lists.append(list)
    return lists

def cardsCompleted(cards)  :
  completed  = 0;
  lists = database.Database().getCompletedLists()
  completed_lists = []
  for completed_list in lists :
      completed_lists.append(completed_list['list_id'])
  for card in cards :
      if card['dueComplete']  :
          completed += 1
      elif card['idList'] in completed_lists :
          completed += 1

  return(completed);
