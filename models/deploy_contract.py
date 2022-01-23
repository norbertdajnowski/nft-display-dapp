"""
Deploy Solidity Contract to Ganache-CLI
"""
# Import required libraries for compiling and deploying a smart contract
from solcx import compile_source
from web3 import Web3, HTTPProvider
from models.contract_collection import contracts

class deployContract:

    def __init__(self, HTTPProviderURI) -> None:
        self.clientAddress = ""
        self.contractsObj = contracts()
        self.web3 = Web3(HTTPProvider(HTTPProviderURI))

    def compileDeploy(self, contractName):
        compiled_contract = compile_source(self.contractsObj.getContract(contractName))
        contract_interface = compiled_contract['<stdin>:FactoryNFT']

        StorageContract = self.web3.eth.contract(
            abi = contract_interface['abi'],
            bytecode = contract_interface['bin'])

        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
        tx_hash = StorageContract.constructor().transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

        contract = self.web3.eth.contract(
            address=tx_receipt.contractAddress,
            abi= contract_interface['abi'],
        )

        return contract
