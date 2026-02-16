import crypto from "crypto";

export interface Transaction {
  from: string;
  to: string;
  amount: number;
}

export interface Block {
  index: number;
  previousHash: string;
  timestamp: number;
  transactions: Transaction[];
  nonce: number;
  hash: string;
}

export function sha256(value: string): string {
  return crypto.createHash("sha256").update(value).digest("hex");
}

export function calculateBlockHash(input: Omit<Block, "hash">): string {
  return sha256(
    `${input.index}|${input.previousHash}|${input.timestamp}|${JSON.stringify(
      input.transactions
    )}|${input.nonce}`
  );
}

export function mineBlock(
  base: Omit<Block, "nonce" | "hash">,
  difficulty = 2,
  maxIterations = 2_000_000
): Block {
  let nonce = 0;

  while (nonce < maxIterations) {
    const candidate = { ...base, nonce };
    const hash = calculateBlockHash(candidate);
    if (hash.startsWith("0".repeat(difficulty))) {
      return { ...candidate, hash };
    }
    nonce += 1;
  }

  throw new Error(
    `Unable to mine block within maxIterations=${maxIterations} (difficulty=${difficulty})`
  );
}

export function validateBlock(
  block: Block,
  previousBlock: Block,
  difficulty = 2
): { valid: boolean; reason?: string } {
  if (block.index !== previousBlock.index + 1) {
    return { valid: false, reason: "invalid_index" };
  }

  if (block.previousHash !== previousBlock.hash) {
    return { valid: false, reason: "previous_hash_mismatch" };
  }

  const expectedHash = calculateBlockHash({
    index: block.index,
    previousHash: block.previousHash,
    timestamp: block.timestamp,
    transactions: block.transactions,
    nonce: block.nonce,
  });

  if (block.hash !== expectedHash) {
    return { valid: false, reason: "hash_mismatch" };
  }

  if (!block.hash.startsWith("0".repeat(difficulty))) {
    return { valid: false, reason: "difficulty_not_met" };
  }

  return { valid: true };
}

export function validateChain(
  chain: Block[],
  difficulty = 2
): { valid: boolean; failedAt?: number; reason?: string } {
  if (chain.length === 0) {
    return { valid: false, failedAt: 0, reason: "empty_chain" };
  }

  for (let i = 1; i < chain.length; i += 1) {
    const result = validateBlock(chain[i], chain[i - 1], difficulty);
    if (!result.valid) {
      return { valid: false, failedAt: i, reason: result.reason };
    }
  }

  return { valid: true };
}
