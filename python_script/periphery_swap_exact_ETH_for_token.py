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
    WETH,
    amount_ETH_for_swap_exact_DAI,
    BlockchainDataJsonEncoder
)

# get router
router_built_file = open('../periphery_short/build/contracts/UniswapV2Router02.json', "r")
router_built_content = json.load(router_built_file)
router_contract_address = router_built_content['networks']["3"]["address"]
router_abi = router_built_content["abi"]
router_contract = w3.eth.contract(address=router_contract_address, abi=router_abi)

# get pair address
pair_address = router_contract.functions.getPairFor(DAI_ADDRESS, WETH).call()
# print(pair_address)

# get pair instance, it's a instance of UniswapV2Pair contract
# UniswapV2Pair is deploy in real time
pair_built_file = open('../factory/build/contracts/UniswapV2Pair.json', "r")
pair_built_content = json.load(pair_built_file)
pair_abi = pair_built_content["abi"]
pair_contract = w3.eth.contract(address=pair_address, abi=pair_abi)

# get reverses of pair
reverses = pair_contract.functions.getReserves().call()
# print(reverses)

if WETH < DAI_ADDRESS:
    reverse_ETH = reverses[0]
    reverse_DAI = reverses[1]
else:
    reverse_ETH = reverses[1]
    reverse_DAI = reverses[0]

# add operator account to default account of web3

operator_account = w3.eth.account.from_key(OPERATOR_PRIVATE_KEY)
w3.eth.default_account = operator_account.address

DAI_amount_min = router_contract.functions.getAmountOut(amount_ETH_for_swap_exact_DAI, reverse_ETH, reverse_DAI).call()
# print(DAI_amount_min)

# ---------- add liquidity through router

swap_exact_ETH_for_tokens_trans = router_contract.functions.swapExactETHForTokens(
    DAI_amount_min,
    [WETH, DAI_ADDRESS],
    OPERATOR_ADDRESS,
    DEADLINE
).buildTransaction({
    'from': OPERATOR_ADDRESS,   # You are not specifying the from, so the default account is used. 
                                # Make sure that's what you want and that the account has enough funds and that its private key is the one you are using to sign.
    'value': amount_ETH_for_swap_exact_DAI,  # NOTE: missing this, it's will raise error: UniswapV2Library: INSUFFICIENT_AMOUNT
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
swap_exact_ETH_for_tokens_trans.update({ 'nonce' : w3.eth.get_transaction_count(OPERATOR_ADDRESS) })
signed_tx = w3.eth.account.sign_transaction(swap_exact_ETH_for_tokens_trans, OPERATOR_PRIVATE_KEY)
txn_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print(json.dumps(txn_receipt, indent=4, sort_keys=True, cls=BlockchainDataJsonEncoder))
