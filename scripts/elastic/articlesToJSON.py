#!/usr/bin/python3

import json

from OSINTmodules import *

from scripts import configOptions

def main(fileName):
    articles = configOptions.esArticleClient.queryDocuments(OSINTelastic.searchQuery(limit = 10_000, complete = True))

    articleDicts = []

    for article in articles["documents"]:
        articleDicts.append(article.as_dict())

    with open(fileName, "w") as exportFile:
        json.dump(articleDicts, exportFile)
