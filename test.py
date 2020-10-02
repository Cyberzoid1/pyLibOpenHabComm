import sys
from time import sleep
import logging
from envparse import env
import pyLibOpenHabComm

# Create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # default level
logger.info("pyOPenHabComm test script started")

# Create formatter
formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] - %(message)s')

# Logger: create console handle
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)     # set logging level for consol
ch.setFormatter(formatter)
logger.addHandler(ch)

# Load .env file
try:
    env.read_envfile('.env')
except:
    logger.error("Error loading .env file")
    sys.exit(1)

try:
    U = env('RestURL')
    I = env('OHItem')
    h = pyLibOpenHabComm.OPENHABCOMM(U, env('User'), env('Password'))
except Exception as e:
    print ("Error loading environment variables")
    print(e)
    sys.exit(2)

responce = []
h.sendItemCommand(I,"ON")  # Turn on
sleep(.250)
responce.append(h.getItemStatus(I))
logger.info(responce[0])
sleep(1.250)
h.sendItemCommand(I,"OFF") # Turn off
sleep(.250)
responce.append(h.getItemStatus(I))
logger.info(responce[1])

# logic testing
if responce[0]['state'] == 'ON' and responce[1]['state'] == 'OFF':
    print ("Test seems successful")
else:
    print ("Status state error")