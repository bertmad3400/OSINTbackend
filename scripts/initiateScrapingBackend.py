#!/usr/bin/python3

# Used for creating a connection to the database
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import os
from pathlib import Path
import requests
import json
# For decompressing the geckodriver that comes compressed in the .tar.gz format when downloading it
import tarfile

from OSINTmodules import OSINTdatabase

postgresqlPassword = ""

def createFolder(folderName, purpose):
    if not os.path.isdir(Path("./" + folderName)):
        try:
            os.mkdir(Path("./" + folderName))
        except:
            raise Exception("The folder needed for {} couldn't be created, exiting".format(purpose))

def extractDriverURL():
    driverDetails = json.loads(requests.get("https://api.github.com/repos/mozilla/geckodriver/releases/latest").text)

    for platformRelease in driverDetails['assets']:
        if platformRelease['name'].endswith("linux64.tar.gz"):
            return platformRelease['browser_download_url']

def downloadDriver(driverURL):
    driverContents = requests.get(driverURL, stream=True)
    with tarfile.open(fileobj=driverContents.raw, mode='r|gz') as driverFile:
        driverFile.extractall(path=Path("./tools/"))

def main():

    downloadDriver(extractDriverURL())

    createFolder('articles', 'storing the markdown files representing the articles')
    createFolder('logs', 'storing the logs')
    
    # Connecting to the database
    conn = psycopg2.connect("user=postgres password=" + postgresqlPassword)
    
    # Needed ass create database cannot be run within transaction
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    # Creating a new database
    with conn.cursor() as cur:
        try:
            cur.execute("CREATE DATABASE osinter;")
        except psycopg2.errors.DuplicateDatabase:
            print("Database already exists, skipping")
    
    conn.close()
    
    # Connecting to the newly created database
    conn = psycopg2.connect("dbname=osinter user=postgres password=" + postgresqlPassword)
    
    print("Creating the needed table...")
    # Making sure the database has gotten the needed table(s)
    OSINTdatabase.initiateArticleTable(conn)

if __name__ == "__main__":
    main()