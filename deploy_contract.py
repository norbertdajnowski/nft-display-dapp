"""
Deploy Solidity Contract to Ganache-CLI
"""
# Import required libraries for compiling and deploying a smart contract
from solcx import compile_source
from web3 import Web3, HTTPProvider
from contract_collection import contracts

contractsObj = contracts()
web3 = Web3(HTTPProvider('http://127.0.0.1:8545'))

compiled_contract = compile_source(contractsObj.getContract("storageContract"))
contract_interface = compiled_contract['<stdin>:StorageContract']

StorageContract = web3.eth.contract(
    abi = contract_interface['abi'],
    bytecode = contract_interface['bin'])

web3.eth.defaultAccount = web3.eth.accounts[0]
tx_hash = StorageContract.constructor().transact()
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

contract = web3.eth.contract(
    address=tx_receipt.contractAddress,
    abi= contract_interface['abi'],
)
