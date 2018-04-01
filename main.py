#!/usr/bin/env python
# -*- coding: utf-8 -*-

import facebook
import datetime as dt
import pandas as pd
import time
import scrapper

# Here you place a token generated in developers.facebook.com with PUBLISH_ACTIONS access
token = ""

# House Name : house identification (from page URL)
houses = {"Fosfobox": "fosfoboxbarclub"}
#          "Matriz": "casadamatriz"}

friends = ["You", "Friend 1", "Friend 2", "Friend 3"]

message = "\n".join(friends)

# This function does not require a token with publish_actions permission.
scrapper = scrapper.eventScrapper(token)
scrapper.setHouses(houses)
events = scrapper.getEvents(upToWeeks=1)

# Comment this line to post in ALL event walls  (no filter yolo)
events = scrapper.addFriendListColumn(events)

print events
raw_input("Continue?")

scrapper.doTheMagic(events, message)