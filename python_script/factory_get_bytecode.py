import json
from common import w3

pair_built_file = open('../factory/build/contracts/UniswapV2Pair.json', "r")
pair_built_content = json.load(pair_built_file)

byte_code = pair_built_content['bytecode']
print(w3.toHex(w3.solidityKeccak(['bytes'], [byte_code]))[2:])

