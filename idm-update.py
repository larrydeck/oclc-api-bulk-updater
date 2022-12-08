#!/usr/bin/env python3

import json
from base64 import b64encode
from os.path import exists
import sys
import pyjq
import requests
from dotenv import dotenv_values

if exists('.env'):
    config = dotenv_values('.env')
else:
    sys.exit('.env file not found, exiting')

try:
    WSKEY   = config['WSKEY']
    SECRET  = config['SECRET']
    INSTID  = config['INSTID']
except KeyError:
    sys.exit('one or more of the expected variables not found in .env file, exiting')

combo       = WSKEY+':'+SECRET
auth        = combo.encode()
authenc     = b64encode(auth)
authheader  = { 'Authorization' : 'Basic %s' %  authenc.decode() }
url         = "https://oauth.oclc.org/token?grant_type=client_credentials&scope=SCIM"

def getToken():

    try:
        r = requests.post(url, headers=authheader)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return r.json()['access_token']


def searchPatron(patronBarcode, authtoken):

    search  = '''
        {
            "schemas": [ "urn:ietf:params:scim:api:messages:2.0:SearchRequest" ]
            , "filter": "External_ID eq \\"%s\\"" 
        }
        ''' % patronBarcode

    searchheaders = { 
        'Authorization' : 'Bearer %s' % authtoken
        , 'Content-Type' : 'application/scim+json'
        , 'Accept' : 'application/scim+json' 
    }

    try:
        s = requests.post(SEARCHURL, headers=searchheaders, data=search)
        s.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if s.status_code == 401:
            raise ValueError('Token expired')
        else:
            SystemExit(err)

    return pyjq.first('.Resources[0].id', s.json())


def readPatron(userId, authtoken):

    readurl = BASEURL + '/Users/%s' % userId

    readheaders = {
        'Authorization' : 'Bearer %s' % authtoken
        , 'Accept' : 'application/scim+json' 
    }

    try:
        read = requests.get(readurl, headers=readheaders)
        read.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if read.status_code == 401:
            raise ValueError('Token expired')
        else:
            SystemExit(err)
        
    return read

def updatePatron(userId, moddedRecord, etag, authtoken):

    updateUrl = BASEURL + '/Users/%s' % userId

    updateheaders =  {
        'Authorization' : 'Bearer %s' % authtoken
        , 'Accept' : 'application/scim+json' 
        , 'Content-Type' : 'application/scim+json' 
        , 'If-Match' : etag
    }

    try:
        update = requests.put(updateUrl, headers=updateheaders, data=moddedRecord)
        update.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if update.status_code == 401:
            raise ValueError('Token expired')
        else:
            SystemExit(err)

    return update

# Read mod.jq for modifier

with open('mod.jq', 'r') as file:
    MODJQ = file.read()

BASEURL = "https://42886.share.worldcat.org/idaas/scim/v2"

SEARCHURL = BASEURL + '/Users/.search'

TOKEN = getToken()


# LOOP
# take identifiers from stdin

for line in sys.stdin:
    barcode = line.strip()

    # find patron's PPID using barcode
    try:
        ppid =  searchPatron(barcode, TOKEN)
    except ValueError:
        # token has expired, get a fresh token and redo search
        print('getting new token')
        TOKEN = getToken()
        ppid =  searchPatron(barcode, TOKEN)

    try:
        patron = readPatron(ppid, TOKEN)
        # for debugging
        patronJson = json.dumps(patron.json(), ensure_ascii=False)
    except ValueError:
        # token has expired, get a fresh token and redo read
        print('getting new token')
        TOKEN = getToken()
        patron = readPatron(ppid, TOKEN)

    # Extract ETag for safe update
    ETag = patron.headers['ETag']

    # Create modded record with MODJQ
    modded = json.dumps(pyjq.one(MODJQ, patron.json()), ensure_ascii=False)

    # Update patron record
    try:
        update = updatePatron(ppid, modded, ETag, TOKEN)
        # print simple confirmation
        print(str(barcode) + "\t" + str(update.status_code))
    except ValueError:
        # token has expired, get a fresh token and redo update
        print('update getting new token')
        TOKEN = getToken()
        update = updatePatron(ppid, modded, ETag, TOKEN)