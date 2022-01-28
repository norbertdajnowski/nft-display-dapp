"""
Deploy Solidity Contract to Ganache-CLI
"""
# Import required libraries for compiling and deploying a smart contract
import os
from solcx import compile_source
from web3 import Web3, HTTPProvider
from models.contract_collection import contracts
from dotenv import load_dotenv

class deployContract:

    load_dotenv()

    def __init__(self, HTTPProviderURI) -> None:
        self.clientAddress = ""
        self.contractsObj = contracts()
        self.web3 = Web3(HTTPProvider(HTTPProviderURI))
        #HTTPProviderURI = os.getenv("ropsten_uri")
        #self.ropsten_secret = os.getenv("infura_ropsten_secret")

    def compileDeploy(self, contractName):
        compiled_contract = compile_source(self.contractsObj.getContract(contractName))
        contract_interface = compiled_contract['<stdin>:' + contractName]

        StorageContract = self.web3.eth.contract(
            abi = contract_interface['abi'],
            bytecode = contract_interface['bin'])

        self.web3.eth.defaultAccount = self.web3.eth.accounts[0] 
        tx_hash = StorageContract.constructor().transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

        contract = self.web3.eth.contract(
            address = tx_receipt.contractAddress,
            abi = contract_interface['abi'],
        )

        return contract
