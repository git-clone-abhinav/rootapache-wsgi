#! /home/pi/WOL_API/venv/bin/python3

# write a basic most basic flask server

from flask import Flask, jsonify
import wakeonlan
import socket
from dotenv import load_dotenv
from flask_cors import CORS
import os
import logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv('/home/pi/WOL_API/.env')
serverIP = os.environ.get("serverIP")
serverPort = int(os.environ.get("serverPort"))
macAddress= os.environ.get("macAddress")


app = Flask(__name__)
CORS(app)



@app.route('/checkonline')
def checkonline():
    """Check if the server is online"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((serverIP,serverPort))
    if result == 0:
        return jsonify({"status":True}), 200
    else:
        return jsonify({"status":False}), 200
    
@app.route('/sendWOLPacket')
def sendWOLPacket():
    """Send Wake on Lan packet to the server"""
    try:
        wakeonlan.send_magic_packet(macAddress,ip_address=serverIP)
        return jsonify({"status":True}), 200
    except Exception as e:
        print(e)
        return jsonify({"status":False}), 200

@app.route('/')
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run('192.168.1.84', port=80, debug=True)
