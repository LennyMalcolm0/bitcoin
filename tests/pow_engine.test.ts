import { ProofOfWork } from '../pow_engine';

const describe = (global as any).describe;
const test = (global as any).test;
const expect = (global as any).expect;

describe('ProofOfWork Engine', () => {
    test('calculateHash returns a valid SHA-256 string', () => {
        const hash = ProofOfWork.calculateHash(0, "0", 12345, "data", 0);
        expect(hash).toHaveLength(64);
        expect(hash).toMatch(/^[a-f0-9]+$/);
    });

    test('verify returns true for a valid hash and nonce', async () => {
        const difficulty = 2;
        const result = await ProofOfWork.mine(0, "0", 12345, "data", difficulty);
        const isValid = ProofOfWork.verify(0, "0", 12345, "data", result.nonce, difficulty, result.hash);
        expect(isValid).toBe(true);
    });

    test('verify returns false for an invalid hash', () => {
        const isValid = ProofOfWork.verify(0, "0", 12345, "data", 999, 2, "invalid-hash");
        expect(isValid).toBe(false);
    });
});
