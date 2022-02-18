import json
from common import w3, DAI_ADDRESS, WETH, amount_ETH_for_swap_exact_DAI

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
    
result = router_contract.functions.getAmountOut(amount_ETH_for_swap_exact_DAI, reverse_ETH, reverse_DAI).call()
# print(reverse_ETH)
# print(reverse_DAI)
# print(amount_ETH_for_swap_exact_DAI)
print(result)
    