import { mineBlock, validateChain, type Block } from "./blockchain";

const difficulty = 2;

const genesis: Block = mineBlock(
  {
    index: 0,
    previousHash: "0".repeat(64),
    timestamp: Date.now(),
    transactions: [{ from: "network", to: "minerA", amount: 50 }],
  },
  difficulty
);

const second = mineBlock(
  {
    index: 1,
    previousHash: genesis.hash,
    timestamp: Date.now() + 1,
    transactions: [
      { from: "minerA", to: "walletB", amount: 3 },
      { from: "walletC", to: "walletA", amount: 5 },
    ],
  },
  difficulty
);

const result = validateChain([genesis, second], difficulty);
if (!result.valid) {
  throw new Error(`Chain validation failed at ${result.failedAt}: ${result.reason}`);
}

console.log(
  JSON.stringify(
    {
      difficulty,
      genesis: { index: genesis.index, hash: genesis.hash, nonce: genesis.nonce },
      second: { index: second.index, hash: second.hash, nonce: second.nonce },
      validation: result,
    },
    null,
    2
  )
);
