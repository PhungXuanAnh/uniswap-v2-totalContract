import json
from common import (
    w3, DAI_ADDRESS,
    OPERATOR_ADDRESS,
    OPERATOR_PRIVATE_KEY,
    ETH_GAS_LIMIT,
    amount_DAI_min,
    amount_ETH_min,
    amount_DAI_desired,
    DEADLINE,
    BlockchainDataJsonEncoder
)

# get router
router_built_file = open('../periphery_short/build/contracts/UniswapV2Router02.json', "r")
router_built_content = json.load(router_built_file)
router_contract_address = router_built_content['networks']["3"]["address"]
router_abi = router_built_content["abi"]
router_contract = w3.eth.contract(address=router_contract_address, abi=router_abi)

# get DAI instance
ERC20_token_built_file = open('../periphery_short/build/contracts/ERC20.json', "r")
ERC20_token_built_content = json.load(ERC20_token_built_file)
ERC20_token_abi = ERC20_token_built_content["abi"]
DAI = w3.eth.contract(address=DAI_ADDRESS, abi=ERC20_token_abi)

# check Operator give allowance router how many DAI
DAI_allowance = DAI.functions.allowance(OPERATOR_ADDRESS, router_contract_address).call()
DAI_allowance = DAI_allowance / 10**18
print("Operator have gave router {} DAI ".format(DAI_allowance))

# import) sys
# sys.exit(0

# add operator account to default account of web3

operator_account = w3.eth.account.from_key(OPERATOR_PRIVATE_KEY)
w3.eth.default_account = operator_account.address

# ------------ approve to router spend amount of desired DAI: here is 500 DAI

transaction = DAI.functions.approve(router_contract.address, amount_DAI_desired).buildTransaction()
transaction.update({ 'nonce' : w3.eth.get_transaction_count(OPERATOR_ADDRESS) })
signed_tx = w3.eth.account.sign_transaction(transaction, OPERATOR_PRIVATE_KEY)
txn_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print(json.dumps(txn_receipt, indent=4, sort_keys=True, cls=BlockchainDataJsonEncoder))

# --------- check again Operator give allowance router how many DAI

DAI_allowance = DAI.functions.allowance(OPERATOR_ADDRESS, router_contract_address).call()
DAI_allowance = DAI_allowance / 10**18
print("Operator have gave router {} DAI ".format(DAI_allowance))

# ---------- add liquidity through router

add_liquidity_ETH_trans = router_contract.functions.addLiquidityETH(
    DAI_ADDRESS,
    amount_DAI_desired,
    amount_DAI_min,
    amount_ETH_min,
    OPERATOR_ADDRESS,
    DEADLINE
).buildTransaction({
    'from': OPERATOR_ADDRESS,   # You are not specifying the from, so the default account is used. 
                                # Make sure that's what you want and that the account has enough funds and that its private key is the one you are using to sign.
    'value': amount_ETH_min,  # NOTE: missing this, it's will raise error: UniswapV2Library: INSUFFICIENT_AMOUNT
    # 'gasPrice': w3.toWei('100', 'gwei'), 
    'gasPrice': w3.eth.gas_price
    # 'to': '0x6Bc272FCFcf89C14cebFC57B8f1543F5137F97dE',
    # 'data': '0x7cf5dab00000000000000000000000000000000000000000000000000000000000000005',
    # 'gas': 43242,
    # 'maxFeePerGas': 2000000000,
    # 'maxPriorityFeePerGas': 1000000000,
    # 'chainId': 1  # network_id
    #  'maxFeePerGas': w3.toWei('2', 'gwei'),
    #  'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
})
add_liquidity_ETH_trans.update({ 'nonce' : w3.eth.get_transaction_count(OPERATOR_ADDRESS) })
signed_tx = w3.eth.account.sign_transaction(add_liquidity_ETH_trans, OPERATOR_PRIVATE_KEY)
txn_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print(json.dumps(txn_receipt, indent=4, sort_keys=True, cls=BlockchainDataJsonEncoder))
