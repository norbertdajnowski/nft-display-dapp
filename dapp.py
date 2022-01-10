"""
Decentralized Application
"""
# Flask requirements
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired

# DAPP Requirements
from hexbytes import HexBytes
from deploy_contract import contract, web3

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'TempSecretKey'


# Registration Form for the application
class RegisterForm(FlaskForm):
    """
    Drop down form field for choosing the ethereum address.
    SelectField specifies that this will be a drop down field.
    'Ethereum Address' is the label we'll give to this drop down field
    # A text input field for the form.
    """
    ethereum_address = SelectField('Ethereum Address', choices=[])
    some_string = StringField('Some String', [InputRequired()])

# Application routes
@app.route("/")
def home():
    return render_template('home.html', contractaddress = contract.address)
    
@app.route("/register", methods=['GET'])
def register():

    # Calling the registration form class
    # List personal accounts.
    # Using n+1 to number each ethereum account
    # return the register.html template
    # pass the register form to the register.html template
    # pass the contract address to the register.html template

    form = RegisterForm()
    form.ethereum_address.choices = []
    minus_one = -1
    for account in web3.eth.accounts:
        minus_one += 1
        form.ethereum_address.choices += [(minus_one, account)]
    return render_template('register.html', registerform=form, contractaddress = contract.address)

@app.route("/registered", methods=['POST'])
def registered():
    """
    Calling a contract function and interact with it using the data from the input
    provided previously.
    """
    call_contract_function = contract.functions.setRegistration(
        request.form['some_string'],
        web3.eth.accounts[int(request.form['ethereum_address'])]).transact() # create the transaction
    
    transaction_info = web3.eth.getTransaction(call_contract_function)
    return render_template(
        'registered.html',
        # pass these variables to the html template
        reg_ethaddress = web3.eth.accounts[int(request.form['ethereum_address'])],
        reg_serial = request.form['some_string'],
        reg_accountnumber = request.form['ethereum_address'],
        reg_receipt = web3.eth.getTransactionReceipt(call_contract_function),
        reg_txhash = HexBytes.hex(transaction_info['hash']),
        reg_txdata = HexBytes(transaction_info['input']),
        contractaddress = contract.address
    )

# Wrapper
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
