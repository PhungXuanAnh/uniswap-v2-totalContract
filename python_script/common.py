import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

INFURA_PROJECT_ID = os.getenv('INFURA_PROJECT_ID')
OPERATOR_PRIVATE_KEY = os.getenv('OPERATOR_PRIVATE_KEY')
OPERATOR_ADDRESS = os.getenv('OPERATOR_ADDRESS')
ETH_GAS_LIMIT = os.getenv('ETH_GAS_LIMIT')

INFURA_URL = 'https://ropsten.infura.io/v3/' + INFURA_PROJECT_ID
WETH = '0xc778417E063141139Fce010982780140Aa0cD5Ab'

DAI_ADDRESS = '0x3ac1c6ff50007ee705f36e40F7Dc6f393b1bc5e7'
AMOUNT_DAI_FOR_SWAP_EXACT_ETH = int(0.1 * 10 ** 18)

# these constances are parameter in method add liquidity DAI-ETH
amount_DAI_desired = 500 * 10 ** 18
amount_DAI_min = 300 * 10 ** 18
amount_ETH_min = 1 * 10 ** 18
DEADLINE = 2000000000

import json
from web3 import Web3
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
print('is connected: {}'.format(w3.isConnected()))


from web3.datastructures import AttributeDict
from hexbytes import HexBytes
class BlockchainDataJsonEncoder(json.JSONEncoder):
    """
        from web3._utils.events import get_event_data
        from web3.datastructures import AttributeDict
        from web3.types import EventData
    """
    def default(self, obj):
        if isinstance(obj, AttributeDict):
            return obj.__dict__
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj) 