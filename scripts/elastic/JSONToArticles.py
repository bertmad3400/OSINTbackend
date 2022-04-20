#!/usr/bin/python3

import json
from datetime import datetime

from OSINTmodules import *

from scripts import configOptions

def main(fileName):
    with open(fileName, "r") as exportFile:
        articles = json.load(exportFile)

    for article in articles:
        for timeValue in ["publish_date", "inserted_at"]:
            article[timeValue] = datetime.strptime(article[timeValue], "%Y-%m-%dT%H:%M:%S%z")

        currentArticleObject = OSINTobjects.Article(**article)
        if not configOptions.esArticleClient.existsInDB(currentArticleObject.url):
            configOptions.esArticleClient.saveDocument(currentArticleObject)
