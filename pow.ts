import crypto from "crypto";

export interface PowInput {
  index: number;
  previousHash: string;
  timestamp: number;
  data: string;
  nonce: number;
}

export function sha256(value: string): string {
  return crypto.createHash("sha256").update(value).digest("hex");
}

export function calculatePowHash(input: PowInput): string {
  return sha256(
    `${input.index}|${input.previousHash}|${input.timestamp}|${input.data}|${input.nonce}`
  );
}

export function isValidPow(hash: string, difficulty: number): boolean {
  if (difficulty < 0) return false;
  return hash.startsWith("0".repeat(difficulty));
}

export function mineProofOfWork(
  payload: Omit<PowInput, "nonce">,
  difficulty: number,
  maxIterations = 5_000_000
): { nonce: number; hash: string; iterations: number } {
  let nonce = 0;

  while (nonce < maxIterations) {
    const hash = calculatePowHash({ ...payload, nonce });
    if (isValidPow(hash, difficulty)) {
      return { nonce, hash, iterations: nonce + 1 };
    }
    nonce += 1;
  }

  throw new Error(
    `Unable to find valid nonce within maxIterations=${maxIterations}`
  );
}
