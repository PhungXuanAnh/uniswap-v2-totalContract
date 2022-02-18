import json
from common import w3, DAI_ADDRESS, OPERATOR_ADDRESS

# get ERC20_token
ERC20_token_built_file = open('../periphery_short/build/contracts/ERC20.json', "r")
ERC20_token_built_content = json.load(ERC20_token_built_file)
ERC20_token_abi = ERC20_token_built_content["abi"]
DAI = w3.eth.contract(address=DAI_ADDRESS, abi=ERC20_token_abi)

result = DAI.functions.balanceOf(OPERATOR_ADDRESS).call()
print(result)
