# This script contains the functions to interact with the Google Assistant Relay.
#
# The code for the Google Assistant Relay can be found on Github in the repository below.
# It can be loaded and run on the same Raspberry Pi as the tracker script.
# https://github.com/greghesp/assistant-relay

# Import libraries
import urllib.request
import json      

# Load json configuration file
with open('config.json', 'r') as f:
    config = json.load(f)

# Setup connection string
url = f'http://{config["SERVER"]}:{config["PORT"]}/assistant'

# Function to turn on lights
def turnOnLights(change):
    # Define command statement
    body = {'command':f'turn {change} {config["LIGHT_GROUP"]}','user':config["USER"]}
    
    # Initiate request
    req = urllib.request.Request(url)
    body_json = json.dumps(body).encode('utf-8')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', len(body_json))
    res = urllib.request.urlopen(req, body_json)
    
    # Check for errors
    if res.status == 200:
        print(f'Response: {res.reason}')
    else:
        print(f'Error: {res.reason}')

# Function to broadcast warning over the Google Home speaker
def broadcastWarning():
    # Define command statement
    body = {'command':f'{config["CHILD"]} is on the loose!','user':'{config["USER"]}','broadcast':'true'}
    
    # Initiate request
    req = urllib.request.Request(url)
    body_json = json.dumps(body).encode('utf-8')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', len(body_json))
    res = urllib.request.urlopen(req, body_json)
    
    # Check for errors
    if res.status == 200:
        print(f'Response: {res.reason}')
    else:
        print(f'Error: {res.reason}')
