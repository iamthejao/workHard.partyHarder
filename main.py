#!/usr/bin/env python
# -*- coding: utf-8 -*-

import facebook
import datetime as dt
import pandas as pd
import fbUtils
import time

# Here you place a token generated in developers.facebook.com with PUBLISH_ACTIONS access
token = "USER_TOKEN"
graph = facebook.GraphAPI(access_token=token, version = 2.7)

# House Name : house identification (from page URL)
houses = {"Fosfobox": "fosfoboxbarclub",
          "Matriz": "casadamatriz",
          "1007": "1007Rio",
          "Odisseia": "teatroodisseia"}

friends = [u"João Pedro Augusto", "Roberto Bandeira", "Ulisses Figueiredo",
           "Christiano Lo Bianco Clementino", "Cristian Ghiel", "Robson Tavares"]

args = {"message" : "\n".join(friends)}

# This function does not require a token with publish_actions permission.
events = fbUtils.eventScrapper(houses, graph)
for iEvent in events.index:
    event = events.iloc[iEvent]
    mural = event['Mural?']
    if mural:
        _id = event['Id']
        print(u"Posting and attending to {0} in {1}".format(event["Name"], event["House"]))
        # ? does facebook consider it spamming? lets add a timer here
        time.sleep(120)
        # Code is commented because there is no control here, we should not be posting
        # more than one time to each event feed. TODO: Post control.
        # fbUtils.attendToEvent(eventId, graph)
        # This function REQUIRES publish_actions permission
        # fbUtils.postToEvent(eventId, graph, args)

    
    
    