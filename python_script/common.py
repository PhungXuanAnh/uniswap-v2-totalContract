import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

INFURA_PROJECT_ID = os.getenv('INFURA_PROJECT_ID')
OPERATOR_PRIVATE_KEY = os.getenv('OPERATOR_PRIVATE_KEY')
OPERATOR_ADDRESS = os.getenv('OPERATOR_ADDRESS')
ETH_GAS_LIMIT = os.getenv('ETH_GAS_LIMIT')

INFURA_URL = 'https://ropsten.infura.io/v3/' + INFURA_PROJECT_ID
DAI_ADDRESS = '0x3ac1c6ff50007ee705f36e40F7Dc6f393b1bc5e7'
WETH = '0xc778417E063141139Fce010982780140Aa0cD5Ab'

import json
from web3 import Web3
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
print('is connected: {}'.format(w3.isConnected()))
