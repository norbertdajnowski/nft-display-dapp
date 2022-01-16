"""
Decentralized Application
"""
# Flask requirements
from flask import render_template, request, Flask
from flask_jwt_extended import JWTManager

# DAPP Requirements
from hexbytes import HexBytes
from models.deploy_contract import contract, web3
import random
import string

app = Flask(__name__,static_url_path='/static')

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = ''.join(random.choice(string.ascii_lowercase) for i in range(22))
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
jwt = JWTManager(app)

# Application routes
@app.route("/")
def home():
    return render_template('getMeta.html')

@app.route("/update_address", methods = ['POST'])
def updateAddress():
    contract.clientAddress = request.form.get("wallet_address")
    #fetch existing NFTs from this client address
    return render_template('getMeta.html', clientAddress = contract.clientAddress)

@app.route("/mint", methods = ['GET'])
def mint_url():
    return render_template('minter.html', clientAddress = contract.clientAddress)

@app.route("/minted", methods = ['POST'])
def mint_nft():
    #collect meta data from post form and mint the nft (IPFS Pinata)
    return render_template('getMeta.html', clientAddress = contract.clientAddress)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
