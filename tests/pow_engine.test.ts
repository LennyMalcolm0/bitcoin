import { ProofOfWork } from '../pow_engine';
import { expect, test, describe } from 'vitest';

describe('ProofOfWork Logic Audit', () => {
    test('Should satisfy basic mining difficulty', () => {
        const difficulty = 2;
        const result = ProofOfWork.mine(1, 'prev_hash', Date.now(), 'tx_data', difficulty);
        
        expect(result.hash.startsWith('00')).toBe(true);
        expect(result.nonce).toBeGreaterThanOrEqual(0);
    });

    test('Verification logic should correctly validate hashes', () => {
        expect(ProofOfWork.verify('000abc', 3)).toBe(true);
        expect(ProofOfWork.verify('00abc', 3)).toBe(false);
    });

    test('Should handle zero difficulty instantly', () => {
        const result = ProofOfWork.mine(0, '', 0, '', 0);
        expect(result.nonce).toBe(0);
    });
});
