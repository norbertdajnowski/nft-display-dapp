"""
Deploy Solidity Contract to Ganache-CLI
"""
# Import required libraries for compiling and deploying a smart contract
import os
import json
from solcx import compile_source
from web3 import Web3, HTTPProvider
from models.contract_collection import contracts
from dotenv import load_dotenv

class web3Connect:

    load_dotenv()

    def __init__(self, HTTPProviderURI) -> None:
        self.contractsObj = contracts()
        self.web3 = Web3(HTTPProvider(HTTPProviderURI))
        self.clientAddress = self.web3.eth.accounts[0]
        self.web3.eth.defaultAccount = self.clientAddress

    def deployContract(self, contractName):
        compiled_contract = compile_source(self.contractsObj.getContract(contractName))
        contract_interface = compiled_contract['<stdin>:' + contractName]
        with open('abi.json', 'w') as file:
            json.dump(contract_interface['abi'], file)

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
