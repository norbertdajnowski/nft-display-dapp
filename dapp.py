"""
Decentralized Application
"""
# Flask requirements
from flask import render_template, request, Flask, redirect, url_for
from flask_jwt_extended import JWTManager
import jinja2

# DAPP Requirements
from hexbytes import HexBytes
from models.deploy import deployContract
import random
import string

app = Flask(__name__,static_url_path='/static')

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = ''.join(random.choice(string.ascii_lowercase) for i in range(22))
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
jwt = JWTManager(app)
clientContract = deployContract('http://127.0.0.1:8545')
mintContract = clientContract.compileDeploy("FactoryNFT")

# Application routes
@app.route("/")
def home():
    return render_template('getMeta.html', clientAddress = clientContract.clientAddress)

@app.route("/update", methods = ['POST'])
def updateAddress():
    clientAddress = request.form.get("wallet_address")
    clientContract.clientAddress = clientAddress
    tx_hash = mintContract.functions.createNFT("https://i.pinimg.com/564x/59/95/18/5995186a3da28eef8906f5d3878c76c2.jpg").transact()
    tx_receipt = clientContract.web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)
    #Get URI from the newly minted token
    print(mintContract.functions.tokenURI(0x0000000000000000000000000000000000000000000000000000000000000001).call())
    return redirect(url_for('home'))

@app.route("/mint", methods = ['GET'])
def mint_url():
    pass

@app.route("/minted", methods = ['POST'])
def mint_nft():
    #collect meta data from post form and mint the nft (IPFS Pinata)
    pass

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
