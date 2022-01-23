"""
Decentralized Application
"""
# Flask requirements
from flask import render_template, request, Flask, redirect, url_for
from flask_jwt_extended import JWTManager
import jinja2

# DAPP Requirements
from hexbytes import HexBytes
from models.deploy_contract import deployContract
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

# Application routes
@app.route("/")
def home():
    return render_template('getMeta.html', clientAddress = clientContract.clientAddress)

@app.route("/update", methods = ['POST'])
def updateAddress():
    clientAddress = request.form.get("wallet_address")
    clientContract.clientAddress = clientAddress
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
