# récuperer la balance d'un compte mainet => ok
# récuperer la balance d'un compte sepolia => ok
# interagir via un call() avec un contrat sur Sepolia (getBalance, getMessage) => ok
# interagir via un send() avec un contrat sur Sepolia (getBalance, setMessage) => ok
# envoyer de l'éther au contrat => ok
# retirer de l'éther => ok
# envoyer de l'éther à une autre adresse => ok


import json
from web3 import Web3, EthereumTesterProvider

contract_address = "0x872b4D48d26D32c386663C06d7Ce4CdD2254dd47"
account_address1 = "0xb45ffab0BC9fE072D6d6043B340D0710665b614D"
account_address2 = "0xaD2DEd70031d932348C0e07D18F35203EB737f6d"
private_key1="48ed524460ce625b6fa837b24c736641e9d0d17027ea81d00e41a2f8da892c75"

def load_abi(path):
    with open(path, 'r') as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # get the contract ABI
        return contract_abi


def init_web3(network):
    if network == "sepolia":
        url="https://sepolia.infura.io/v3/3049312db5734d259b76f5ca05ed75d5"
    if network == "mainnet":
        url="https://mainnet.infura.io/v3/3049312db5734d259b76f5ca05ed75d5"
    if network == "ganache":
        url="http://127.0.0.1/:8545"
    if network == "test":
        url="http://127.0.0.1/:8545"
    if network != "test":     
        w3 = Web3(Web3.HTTPProvider(url))
    else:
        w3 = Web3(EthereumTesterProvider())
    return w3

def setup_account_from_private_key1(w3):    
    return w3.eth.account.from_key(private_key1)
    
#########################################################################
# function to wrap the building, signing and sending of a transation to 
# execute a state changing function in a contract
#########################################################################
def send_transaction(w3,contract, function_name, function_args, account):
    
    if function_args != []:
        func = contract.functions.__getattribute__(function_name)(*function_args)
    else:
        func = contract.functions.__getattribute__(function_name)()
    
    txn = func.build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 210000,
        'gasPrice': w3.eth.gas_price,
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=account._private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return w3.eth.wait_for_transaction_receipt(txn_hash)
 


#########################################################################
# function to wrap the building, signing and sending of a transation to 
# send eth to a contract
#########################################################################
def sentEth(amount,account):

    amount_in_wei = w3.to_wei(amount, 'ether')   
    txn = {
        'to': contract_address,
        'from': account.address,
        'value': amount_in_wei,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 210000,  
        'gasPrice': w3.eth.gas_price,
    }
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=account._private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return w3.eth.wait_for_transaction_receipt(txn_hash)
 



w3=init_web3("sepolia")
account1 = setup_account_from_private_key1(w3)

contract_abi = load_abi("../solidity/build/contracts/HelloWorld.json")
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

print(f"message is {contract.functions.getMessage().call()}")
print(f"balance is {w3.from_wei(contract.functions.getBalance().call(),'ether')}")

send_transaction(w3,contract,"setMessage",["toto"],account1)

print(f"message is {contract.functions.getMessage().call()}")
print(f"balance is {w3.from_wei(contract.functions.getBalance().call(),'ether')}")

sentEth(1,account1)

print(f"message is {contract.functions.getMessage().call()}")
print(f"balance is {w3.from_wei(contract.functions.getBalance().call(),'ether')}")

amount =int(1e9/2)
print(f"sending {amount} gwei")
send_transaction(w3,contract,"sendEther",[account_address2,amount],account1)
print(f"eth envoyés à {account_address2}")
print(f"message is {contract.functions.getMessage().call()}")
print(f"balance is {w3.from_wei(contract.functions.getBalance().call(),'ether')}")


send_transaction(w3,contract,"emptyWallet",[account1.address],account1)

print(f"message is {contract.functions.getMessage().call()}")
print(f"balance is {w3.from_wei(contract.functions.getBalance().call(),'ether')}")


 

