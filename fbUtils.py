#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 21:20:29 2018

@author: joaoaugusto
"""

import datetime as dt
import pandas as pd

def attendToEvent(eventId, graph):
    ans = graph.request('/{0}/attending'.format(eventId), method='POST')
    return ans['success']

def postToEvent(eventId, graph, args):
    graph.request('/{0}/feed/'.format(eventId), method='POST', args = args)


def eventScrapper(houses, graph, upToWeeks = 1, vipKeys=["mural", "vip", "lista amiga"]):
    
    today = dt.date.today()
    currentWeek = today.isocalendar()[1]
    eventFrame = pd.DataFrame(columns = ["Date","House", "Name", "Id", "Mural?", "Links"])
    
    for house in houses.keys():
        
        print("Checking {0}".format(house))
        
        pageId = houses[house]
        request = graph.request("/{0}/events/".format(pageId))
        events = request['data']
        
        for event in events:
            
            start_time = dt.datetime.strptime(event['start_time'], "%Y-%m-%dT%H:%M:%S-%f")
            eventWeek = start_time.date().isocalendar()[1]
            
            if (eventWeek - currentWeek) >= 0 and (eventWeek - currentWeek) <= upToWeeks:
                
                mural = False
                antecipado = False
                description = event['description'].replace('\r', ' ').replace('\n', ' ').upper()
                
                # Checking for vipKeys and Antecipado
                for keyword in vipKeys:
                    
                    if keyword.upper() in description:
                        mural = True
                        
                    if "antecipado".upper() in description:
                        tokenized = description.split(" ")
                        links = []
                        for token in tokenized:
                            if "HTTP" in token or (".COM" in token and "@" not in token):
                                links.append(token)
                        antecipado = ", ".join(links)
                                
                eventBuilder = eventFrame[0:0].copy()
                eventBuilder['Date'] = [start_time]
                eventBuilder['House'] = [house]
                eventBuilder['Name'] = [event['name']]
                eventBuilder['Id'] = [event['id']]
                eventBuilder['Mural?'] = [mural]
                eventBuilder['Links'] = [antecipado]
                eventFrame = eventFrame.append(eventBuilder)
                
    eventFrame.reset_index(inplace=True, drop = True)
    return eventFrame