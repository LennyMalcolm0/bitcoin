import { mineProofOfWork, isValidPow } from "./pow";

const difficulty = 3;
const payload = {
  index: 1,
  previousHash: "0".repeat(64),
  timestamp: Date.now(),
  data: "genesis-transaction",
};

const result = mineProofOfWork(payload, difficulty);

if (!isValidPow(result.hash, difficulty)) {
  throw new Error("PoW validation failed");
}

console.log(JSON.stringify({ difficulty, ...result }, null, 2));
