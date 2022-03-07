"""
Decentralized Application
"""
# Flask requirements
from http import client
from datetime import datetime
from flask import render_template, request, Flask, redirect, url_for
from flask_jwt_extended import JWTManager
import jinja2
from web3 import Web3, HTTPProvider

# DAPP Requirements
from hexbytes import HexBytes
from models.deploy import web3Connect
import random
import string

app = Flask(__name__,static_url_path='/static')

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = ''.join(random.choice(string.ascii_lowercase) for i in range(22))
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
jwt = JWTManager(app)
web3Interface = web3Connect('http://192.168.1.107:8545')
contract = web3Interface.deployContract("Factory")

# Application routes
@app.route("/")
def home():
    print(web3Interface.clientAddress)
    print(contract.address)
    imgSourceList = []
    displayNodeList = []
    try:
        numOfTokens = contract.functions.balanceOf(web3Interface.clientAddress).call()
        numOfDisplayNodes = contract.functions.displayNumber().call()
        for i in range(numOfTokens):
            tokenId = contract.functions.tokenOfOwnerByIndex(web3Interface.clientAddress, i).call()
            imgSourceList.append(contract.functions.tokenURI(tokenId).call())
        for x in range(numOfDisplayNodes):
            if (contract.functions.getDisplayStatus(x).call() == 0):
                displayNodeList.append(x)
    except Exception as e:
        print("Exception has occured: " , e)
    return render_template('getMeta.html', clientAddress = web3Interface.clientAddress, imgSourceList = imgSourceList, displayNodeList = displayNodeList)

@app.route("/mint", methods = ['GET'])
def mint():
    #test mint
    tx_hash = contract.functions.createNFT("https://images.pexels.com/photos/10346451/pexels-photo-10346451.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260").transact()
    tx_receipt = web3Interface.web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)
    return redirect(url_for('home'))

@app.route("/upload", methods = ['POST'])
def upload():
    token = int(request.form.get('nftInput')[4:])
    display = 0 #int(request.form.get('nodeInput')[8:])
    timeout = int(datetime.now().strftime("%Y%m%d%H%M")) + 3
    tx_hash = contract.functions.displayTokenUpload(display, token, timeout).transact()
    tx_receipt = web3Interface.web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
