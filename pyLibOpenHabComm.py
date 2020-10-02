import requests
import logging
import json

__version__ = 2.02

# Create Logger. Name will be the filename 'pyOpenHabComm'
OHLogger = logging.getLogger(__name__)
OHLogger.setLevel(logging.DEBUG) # default level

class OPENHABCOMM():
    def __init__(self, url=None, user=None, pw=None):
        if url is None:
            raise "Must supply a URL"
        if user is None:
            raise "Must supply a username"
        if pw is None:
            raise "Must supply a password"
        self.url = url
        self.user = user
        self.pw = pw
        self.buildSession()
    
    def buildSession(self):
        self.session = requests.Session()
        self.session.auth = (self.user, self.pw)
        self.timeout = 3.0

    def sendItemCommand(self, item, data):
        # Convert bool data to ON & OFF values
        if type(data) == bool:
            if x == True: # if
                data = 'ON'
                OHLogger.debug("Converting bool %b to ON value")
            elif x == False:
                data = 'OFF'
                OHLogger.debug("Converting bool %b to OFF value")
        OHLogger.debug ("Sending %r type %r to item %r" % (data, type(data), item))

        # Send activity to server
        try:
            #myresponce = requests.post(self.url + 'items/' + item, str(data), auth=(self.user,self.pw), timeout=3.0)  # Old non session method
            myresponce = self.session.post(self.url + 'items/' + item, str(data))
            OHLogger.debug("Return value: %r" % myresponce.text)
        except (requests.ConnectTimeout, requests.ConnectionError) as e:
            OHLogger.error ("Connection error")
            OHLogger.error(str(e))
        except (requests.ReadTimeout, requests.Timeout) as e:
            OHLogger.error ("Request Timedout")
            OHLogger.error(str(e))
        except requests.RequestException as e:
            OHLogger.error ("Request: General Error")
            OHLogger.error (str(e))
        #return (myresponce.status_code, myresponce.json())

    def getItemStatus(self, item):
        try:
            # myresponce = requests.get(self.url + 'items/' + item, auth=(self.user,self.pw), timeout=3.0)             # Old non session method
            myresponce = self.session.get(self.url + 'items/' + item)
            OHLogger.debug("Item value: %r" % myresponce.text)
            return myresponce.json()
        except (requests.ConnectTimeout, requests.ConnectionError) as e:
            OHLogger.error ("Connection error")
            OHLogger.error(str(e))
        except (requests.ReadTimeout, requests.Timeout) as e:
            OHLogger.error ("Request Timedout")
            OHLogger.error(str(e))
        except requests.RequestException as e:
            OHLogger.error ("Request: General Error")
            OHLogger.error (str(e))
