import json
from common import w3, DAI_ADDRESS, WETH

factory_built_file = open('../factory/build/contracts/UniswapV2Factory.json', "r")
factory_built_content = json.load(factory_built_file)

factory_address = factory_built_content['networks']["3"]["address"]
factory_abi = factory_built_content["abi"]
factory = w3.eth.contract(address=factory_address, abi=factory_abi)
pair = factory.functions.getPair(DAI_ADDRESS, WETH).call()
print(pair)
