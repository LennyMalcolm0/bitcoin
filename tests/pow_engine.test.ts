import { ProofOfWork } from '../pow_engine';
import { expect, test, describe } from 'vitest';

describe('ProofOfWork V3.1 Audit (Zero-Defect Protocol)', () => {
    test('Async mining should satisfy difficulty', async () => {
        const difficulty = 2;
        const result = await ProofOfWork.mine(1, 'prev_hash', Date.now(), 'tx_data', difficulty);
        
        expect(result.hash.startsWith('00')).toBe(true);
        expect(result.nonce).toBeGreaterThanOrEqual(0);
    });

    test('Full Integrity Verification should work', async () => {
        const index = 1;
        const prev = '000';
        const ts = Date.now();
        const data = 'block_data';
        const diff = 2;
        
        const { hash, nonce } = await ProofOfWork.mine(index, prev, ts, data, diff);
        
        // Correct verification
        expect(ProofOfWork.verify(index, prev, ts, data, nonce, diff, hash)).toBe(true);
        
        // Tampered data should fail
        expect(ProofOfWork.verify(index, prev, ts, 'TAMPERED', nonce, diff, hash)).toBe(false);
    });

    test('Collision resistance check (Delimiters)', () => {
        const hash1 = ProofOfWork.calculateHash(1, '23', 0, '', 0);
        const hash2 = ProofOfWork.calculateHash(12, '3', 0, '', 0);
        expect(hash1).not.toBe(hash2);
    });
});
