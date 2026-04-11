import crypto from 'crypto';

/**
 * SOVEREIGN CRYPTO ENGINE: Proof of Work Implementation (V3.3)
 * Hardened against Timing Attacks & fully optimized for production.
 */
export class ProofOfWork {
    /**
     * Internal hashing using Node.js crypto (High Performance).
     */
    static calculateHash(index: number, previousHash: string, timestamp: number, data: string, nonce: number): string {
        const payload = `${index}:${previousHash}:${timestamp}:${data}:${nonce}`;
        return crypto.createHash('sha256').update(payload).digest('hex');
    }

    /**
     * ASYNCHRONOUS Mining Loop (Non-blocking).
     */
    static async mine(index: number, previousHash: string, timestamp: number, data: string, difficulty: number, maxNonce: number = 10000000): Promise<{ hash: string, nonce: number }> {
        let nonce = 0;
        const target = '0'.repeat(difficulty);
        
        while (true) {
            const hash = this.calculateHash(index, previousHash, timestamp, data, nonce);
            if (hash.startsWith(target)) {
                return { hash, nonce };
            }
            nonce++;

            if (nonce % 10000 === 0) {
                await new Promise(resolve => setImmediate(resolve));
            }
            
            if (nonce > maxNonce) throw new Error("Mining timeout: Difficulty too high for local environment");
        }
    }

    /**
     * FULL INTEGRITY VERIFICATION (V3.3 Fix)
     * Implements crypto.timingSafeEqual for genuine protection against timing attacks.
     */
    static verify(index: number, previousHash: string, timestamp: number, data: string, nonce: number, difficulty: number, providedHash: string): boolean {
        if (!providedHash || difficulty < 0) return false;
        
        if (!providedHash.startsWith('0'.repeat(difficulty))) return false;
        
        const calculatedHash = this.calculateHash(index, previousHash, timestamp, data, nonce);
        
        // GENUINE Constant Time Comparison (Tier-1 Fix)
        try {
            // Using crypto.timingSafeEqual directly on buffers with hex encoding
            const bufferCalculated = Buffer.from(calculatedHash, 'hex');
            const bufferProvided = Buffer.from(providedHash, 'hex');
            if (bufferCalculated.length !== bufferProvided.length) return false;
            return crypto.timingSafeEqual(bufferCalculated, bufferProvided);
        } catch (e) {
            return false;
        }
    }
}
