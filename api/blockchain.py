"""
Bitcoin Blockchain API — Storage, consensus, and block validation.
"""

import hashlib
import time
import json


class ChainIntegrityError(Exception):
    """Raised when blockchain integrity check fails."""
    pass


def compute_block_hash(block: dict) -> str:
    """
    Compute the SHA-256 hash of a block.

    Args:
        block: Block dict. The 'hash' field, if present, is excluded
               from the computation.

    Returns:
        str — Hex-encoded SHA-256 hash.
    """
    fields = {k: v for k, v in block.items() if k != 'hash'}
    block_str = json.dumps(fields, sort_keys=True, default=str)
    return hashlib.sha256(block_str.encode()).hexdigest()


def compute_merkle_root(transactions: list) -> str:
    """
    Compute the Merkle root of a list of transactions.

    Args:
        transactions: List of transaction dicts.

    Returns:
        str — Hex-encoded Merkle root hash.
    """
    if not transactions:
        return hashlib.sha256(b'').hexdigest()

    def hash_pair(a: str, b: str) -> str:
        return hashlib.sha256((a + b).encode()).hexdigest()

    hashes = [compute_block_hash(tx) for tx in transactions]

    while len(hashes) > 1:
        if len(hashes) % 2 != 0:
            hashes.append(hashes[-1])
        hashes = [hash_pair(hashes[i], hashes[i + 1]) for i in range(0, len(hashes), 2)]

    return hashes[0]


class Blockchain:
    """
    Bitcoin blockchain — an append-only ledger of blocks.

    Inherits from BitcoinComponent and manages the core chain data structure.

    Example::

        blockchain = Blockchain()
        genesis = blockchain.create_genesis_block()
        blockchain.add_block(my_block)
        assert blockchain.is_chain_valid()
    """

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self) -> dict:
        """
        Create the genesis (first) block of the chain.

        Returns:
            dict — Genesis block with index=0, hash='0', and timestamp.

        Example::

            genesis = blockchain.create_genesis_block()
        """
        block = {
            "index": 0,
            "timestamp": 1231006505.0,  # Bitcoin genesis block timestamp
            "data": "Genesis Block",
            "hash": "0",
            "previous_hash": "0",
            "transactions": []
        }
        return block

    def add_block(self, block: dict) -> None:
        """
        Append a validated block to the local chain.

        Validates:
        - Block has a 'previous_hash' matching the last chain block's hash
        - Block's own hash is correctly computed

        Args:
            block: Block dict with 'index', 'timestamp', 'data', 'hash',
                   'previous_hash', and optionally 'transactions'.

        Raises:
            ChainIntegrityError: If previous_hash doesn't match or hash is invalid.

        Example::

            blockchain.add_block(new_block)
        """
        if block['index'] != len(self.chain):
            raise ChainIntegrityError(
                f"Block index mismatch: expected {len(self.chain)}, got {block['index']}"
            )

        prev_block = self.get_latest_block()
        if block.get('previous_hash', prev_block['hash']) != prev_block['hash']:
            raise ChainIntegrityError(
                f"Previous hash mismatch at block {block['index']}"
            )

        # Verify the block's own hash
        expected_hash = compute_block_hash(block)
        if block.get('hash') != expected_hash:
            raise ChainIntegrityError(
                f"Block hash invalid at index {block['index']}"
            )

        self.chain.append(block)
        print(f"[Blockchain] Block #{block['index']} added. Hash: {block['hash'][:8]}...")

    def get_block(self, index: int) -> dict | None:
        """
        Retrieve a block by its index.

        Args:
            index: Block index (0-based).

        Returns:
            Block dict if found, None otherwise.

        Example::

            block = blockchain.get_block(42)
        """
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None

    def get_latest_block(self) -> dict:
        """
        Return the most recent block in the chain.

        Returns:
            dict — The last block.

        Example::

            latest = blockchain.get_latest_block()
            print(f"Height: {latest['index']}")
        """
        return self.chain[-1]

    def get_chain_length(self) -> int:
        """
        Return the total number of blocks.

        Returns:
            int — Block count.
        """
        return len(self.chain)

    def is_chain_valid(self) -> bool:
        """
        Validate the entire chain by verifying every hash link.

        Checks:
        - Each block's 'previous_hash' links to the prior block's hash
        - Each block's own hash is correctly computed

        Returns:
            bool — True if the chain is valid.

        Raises:
            ChainIntegrityError: On the first invalid block encountered.

        Example::

            assert blockchain.is_chain_valid()
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Verify hash linkage
            if current.get('previous_hash') != previous.get('hash', compute_block_hash(previous)):
                raise ChainIntegrityError(
                    f"Chain broken at block {i}: previous_hash mismatch"
                )

            # Verify block hash
            expected = compute_block_hash(current)
            if current.get('hash') != expected:
                raise ChainIntegrityError(
                    f"Chain broken at block {i}: hash mismatch"
                )

        return True

    def add_pending_transaction(self, tx: dict) -> None:
        """
        Add a transaction to the pending mempool.

        Args:
            tx: Transaction dict.

        Example::

            blockchain.add_pending_transaction(tx)
        """
        self.pending_transactions.append(tx)

    def get_pending_transactions(self) -> list:
        """
        Return all pending (unconfirmed) transactions.

        Returns:
            list — Copy of the pending transaction mempool.
        """
        return list(self.pending_transactions)

    def mine_pending_transactions(self, miner_reward: float = 6.25) -> dict:
        """
        Create a new block from all pending transactions and add it to the chain.

        Args:
            miner_reward: The coinbase reward for the miner (default: 6.25 BTC).

        Returns:
            dict — The newly mined block.

        Example::

            new_block = blockchain.mine_pending_transactions()
        """
        if not self.pending_transactions:
            raise ValueError("No pending transactions to mine.")

        # Add coinbase transaction for miner
        coinbase_tx = {
            "sender_public_key": "0000...miner",
            "recipient_public_key": "0000...miner",
            "amount": miner_reward,
            "reference": "coinbase",
            "signature": "coinbase",
            "timestamp": time.time()
        }

        merkle_root = compute_merkle_root(
            self.pending_transactions + [coinbase_tx]
        )
        latest = self.get_latest_block()

        new_block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "data": f"Mined block with {len(self.pending_transactions)} transactions",
            "previous_hash": latest.get('hash', compute_block_hash(latest)),
            "merkle_root": merkle_root,
            "transactions": self.pending_transactions + [coinbase_tx],
            "nonce": 0
        }

        # Simple proof-of-work (find hash starting with '00')
        difficulty = 2  # Number of leading zero bytes
        while True:
            new_block_str = json.dumps(new_block, sort_keys=True, default=str)
            new_block['hash'] = hashlib.sha256(new_block_str.encode()).hexdigest()
            if new_block['hash'][:difficulty] == '0' * difficulty:
                break
            new_block['nonce'] += 1

        self.add_block(new_block)
        self.pending_transactions = []
        return new_block
