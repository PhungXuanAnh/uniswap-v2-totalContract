import json
from common import w3, DAI_ADDRESS, WETH

# get router
router_built_file = open('../periphery_short/build/contracts/UniswapV2Router02.json', "r")
router_built_content = json.load(router_built_file)
router_contract_address = router_built_content['networks']["3"]["address"]
router_abi = router_built_content["abi"]
router_contract = w3.eth.contract(address=router_contract_address, abi=router_abi)

result = router_contract.functions.getPairFor(DAI_ADDRESS, WETH).call()
print(result)
