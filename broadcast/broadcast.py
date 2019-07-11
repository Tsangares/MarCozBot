from flask import Flask, request, jsonify
from flask_restful import Resource,Api
from multiprocessing import Pool
from requests.exceptions import ConnectionError
from itertools import repeat
import os,random,requests
import json
app=Flask(__name__)
api=Api(app)

DEFAULT_PORT=2000
ADDRESSES=['localhost',]

''' INSTRUCTIONS
Put all of your computers local ip addresses into the variable ADDRESSES above.
Run this code on all of the computers.
When you run the function broadcast (or go to the url localhost:2000/broadcast)
 this code will send the message {'should_i_click': True} to all the computers
 in the list of ADDRESSES.

Replace the code in arbitray_function_name() to do your bidding when broadcast is called.
Then on your coodinating computer write code like that in example.py to broadcast 
 on specific intervals.
''' 
def getIPList():
    return ADDRESSES

def emit(ip,endpoint,message,port=DEFAULT_PORT):
    if '/' == endpoint[0]: endpoint=endpoint[1:] #Stripping / just in case
    url='http://{}:{}/{}'.format(ip,str(port),endpoint)
    print("Submitting a reques to the url",url)
    try:
        #Submit network request
        return requests.post(url,data=message,timeout=5).text
    except ConnectionError as e:
        print("Could not find destination", endpoint,ip)
        return None
    
@app.route('/broadcast', methods=['GET'])
def broadcast(endpoint='/recieve'):
    message={'should_i_click': True}
    ips=getIPList()
    #Pool uses multiprocessing so you dont have to wait.
    with Pool(len(ips)) as pool:
        args=zip(ips,repeat(endpoint),repeat(message))
        res=pool.starmap(emit,args)
    print("Broadcast finished.",res)
    return "Broadcast Finished"


@app.route('/recieve', methods=['POST'])
def arbitray_function_name():
    shouldClick=request.values.get('should_i_click')
    if shouldClick:
        print("Click!",shouldClick)
    else:
        print("Dont CLICK!",shouldClick)
    return "Success"

if __name__=="__main__":
    app.run(host='0.0.0.0',port=DEFAULT_PORT,debug=False)

