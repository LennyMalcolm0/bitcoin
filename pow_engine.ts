import crypto from 'crypto';

/**
 * SOVEREIGN CRYPTO ENGINE: Proof of Work Implementation
 * Compliant with Tier-1 Standards (Performance & Security)
 */
export class ProofOfWork {
    /**
     * Internal hashing using Node.js crypto (High Performance)
     */
    static calculateHash(index: number, previousHash: string, timestamp: number, data: string, nonce: number): string {
        const payload = `${index}${previousHash}${timestamp}${data}${nonce}`;
        return crypto.createHash('sha256').update(payload).digest('hex');
    }

    /**
     * Mining Loop with Micro-optimization (Tier-1 Standard)
     */
    static mine(index: number, previousHash: string, timestamp: number, data: string, difficulty: number): { hash: string, nonce: number } {
        let nonce = 0;
        const target = '0'.repeat(difficulty);
        
        while (true) {
            const hash = this.calculateHash(index, previousHash, timestamp, data, nonce);
            if (hash.startsWith(target)) {
                return { hash, nonce };
            }
            nonce++;
            
            // Safety break for simulation (Optional in Mainnet)
            if (nonce > 10000000) throw new Error("Mining timeout: Difficulty too high for CPU");
        }
    }

    /**
     * Statutory Validation Check
     */
    static verify(hash: string, difficulty: number): boolean {
        if (!hash || difficulty < 0) return false;
        return hash.startsWith('0'.repeat(difficulty));
    }
}
