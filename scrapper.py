#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 16:20:16 2018

@author: joaoaugusto
"""

import facebook
import datetime as dt
import pandas as pd
import os
import pickle

class eventScrapper(facebook.GraphAPI):
    
    def __init__(self, accessToken, houses={}):
        
        facebook.GraphAPI.__init__(self, accessToken)
        self.houses = houses
        self.defaultVipKeywords = ["mural", "vip", "lista amiga"]
    
    def setHouses(self, houses):
        
        """
        type: dict
        format: {'your label':'pagename'}
        ie. https://www.facebook.com/pagename/
        return: None
        """
        
        self.houses = houses
    
    #TODO: Exception Handling 
    def attendToEvent(self, eventId):
        ans = self.request('/{0}/attending'.format(eventId), method='POST')
        return ans['success']
    
    #TODO: Exception Handling
    def postToEvent(self, eventId, messageStr):
        args = {"message" : messageStr}
        self.request('/{0}/feed/'.format(eventId), method='POST', args = args)
    
    def getEvents(self, fromDate=dt.date.today(), upToWeeks=1):
        
        week = fromDate.isocalendar()[1]
        eventFrame = pd.DataFrame(columns = ["Date","House", "Name", "Id", "Description"])
        for house in self.houses.keys():
            
            pageId = self.houses[house]
            events = self.request("/{0}/events/".format(pageId))['data']
            
            for event in events:
                
                startTime = dt.datetime.strptime(event['start_time'], "%Y-%m-%dT%H:%M:%S-%f")
                eventWeek = startTime.date().isocalendar()[1]
                includeCondition = (startTime.date() > fromDate) and (eventWeek - week) <= upToWeeks
                
                if includeCondition:
                    
                    eventBuilder = eventFrame[0:0].copy()
                    eventBuilder['Date'] = [startTime]
                    eventBuilder['House'] = [house]
                    eventBuilder['Name'] = [event['name']]
                    eventBuilder['Id'] = [event['id']]
                    eventBuilder['Description'] = [event['description'].replace('\r', ' ').replace('\n', ' ').upper()]
                    eventFrame = eventFrame.append(eventBuilder)
        
        eventFrame.reset_index(inplace=True, drop = True)
        eventFrame = eventFrame.sort_values(['House', 'Date'])
        eventFrame['Link'] = eventFrame['Description'].apply(self.getURLs)
        return eventFrame
    
    def addFriendListColumn(self, eventFrame, keywords=[]):
        eventFrame['FriendList?'] = eventFrame['Description'].apply(lambda desc: self.acceptFriendsList(desc,
                  self.defaultVipKeywords+keywords))
        return eventFrame
    
    @staticmethod
    #TODO: this is kinda a shitty way to do it
    def getURLs(bigString):
        
        bigString = bigString.upper()
        tokenized = bigString.split(" ")
        urls = []
        for token in tokenized:
            if ("HTTP" in token) or (".COM" in token and "@" not in token):
                urls.append(token)
        return ",".join(urls)
    
    @staticmethod
    def acceptFriendsList(bigString, keywords):
        bigString = bigString.upper()
        for keyword in keywords:
            if keyword.upper() in bigString:
                return True
        return False
    
    #TODO: Exception handling, too broad
    def doTheMagic(self, eventFrame, message, wait=5):
        
        savedFile = os.path.exists('eventlog.pkl')
        logDict = {}
        if savedFile:
            logDict = pickle.load(file('eventlog.pkl','r'))
        
        for i in eventFrame.index:
            event = eventFrame.iloc[i]
            if event['Id'] in logDict.keys():
                print(u"You have already posted to {0} in {1}".format(event["Name"], event["House"]))
            else:
                post = True
                if ('FriendList?' in event.index):
                    post = event['FriendList?']
                # Too broad exception handling
                try:
                    # Only evaluates attendToEvent is post is True
                    if post and self.attendToEvent(event['Id']):
                        self.postToEvent(event['Id'], message)
                        print(u"Posted and attended to {0} in {1}".format(event["Name"], event["House"]))
                        logDict[event['Id']] = {'name': event['Name'],
                                                'where': event['House'],
                                                'when': event['Date'].to_pydatetime().strftime("%Y-%m-%dT%H:%M:%s"),
                                                'posted': dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%s")
                                                }
                except:
                    print(u"Error: Could not post to {0} in {1}".format(event["Name"], event["House"]))
                pickle.dump(logDict, file('eventlog.pkl', 'w'))
                    
                
        
        
    
    
                
    
        