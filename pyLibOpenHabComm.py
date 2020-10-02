import requests
import logging
import json

__version__ = 2.1.0

# Create Logger. Name will be the filename 'pyOpenHabComm'
OHLogger = logging.getLogger(__name__)
OHLogger.setLevel(logging.DEBUG) # default level

class OPENHABCOMM():
    def __init__(self, url=None, user=None, pw=None, datatype=str):
        if url is None:
            raise "Must supply a URL"
        self.url = url
        self.user = user
        self.pw = pw
        self.datatype = datatype

    def sendItemCommand(self, item, data):
        OHLogger.debug ("Sending %r type %r to item %r (auto converting to str)" % (data, type(data), item))

        # Send activity to server
        try:
            myresponce = requests.post(self.url + 'items/' + item, str(data), auth=(self.user,self.pw), timeout=3.0)
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

    def getItemStatus(self, item):
        try:
            myresponce = requests.get(self.url + 'items/' + item, auth=(self.user,self.pw), timeout=3.0)
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
