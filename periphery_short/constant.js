// const DAI_ADDRESS = '0xad6d458402f60fd3bd25163575031acdce07538d'
const DAI_ADDRESS = '0x3ac1c6ff50007ee705f36e40F7Dc6f393b1bc5e7'

const TOKENS = {
  dai: {
    address: DAI_ADDRESS,
    amountDesired: (500 * 10 ** 18).toString(),
    amountMin: (300 * 10 ** 18).toString(),
    amountETHMin: (1 * 10 ** 18).toString(),
  },
};

const SWAP_EXACT_ETH_FOR_TOKENS = {
  dai: {
    address: DAI_ADDRESS,
    amountETH: (0.1 * 10 ** 18).toString(),
  },
};

const WETH = '0xc778417E063141139Fce010982780140Aa0cD5Ab';
const DEADLINE = '2000000000';

module.exports = { TOKENS, WETH, DEADLINE, SWAP_EXACT_ETH_FOR_TOKENS };
