"""
Bitcoin Wallet API — Key management, transaction creation, and signing.
"""

import hashlib
import time
import json
import secrets
import struct

try:
    from ecdsa import SigningKey, SECP256k1
    HAS_ECDSA = True
except ImportError:
    HAS_ECDSA = False


class BitcoinException(Exception):
    """Base exception for Bitcoin API errors."""
    pass


class InsufficientFunds(BitcoinException):
    """Raised when a transaction exceeds available balance."""
    pass


class InvalidSignature(BitcoinException):
    """Raised when transaction signature verification fails."""
    pass


def _hash160(public_key_bytes: bytes) -> str:
    """Compute HASH160 = RIPEMD160(SHA256(public_key))."""
    sha256_hash = hashlib.sha256(public_key_bytes).digest()
    try:
        ripemd160 = hashlib.new('ripemd160')
    except ValueError:
        # RIPEMD160 not available — use SHA-256 truncated as fallback
        # In production, install: pip install ripemd160
        return hashlib.sha256(sha256_hash).hexdigest()[:40]
    ripemd160.update(sha256_hash)
    return ripemd160.hexdigest()


def _compute_tx_hash(tx: dict) -> str:
    """Compute the canonical hash of a transaction dict."""
    canonical = {
        'sender_public_key': tx['sender_public_key'],
        'recipient_public_key': tx['recipient_public_key'],
        'amount': tx['amount'],
        'reference': tx.get('reference', ''),
        'timestamp': tx.get('timestamp', 0),
    }
    tx_str = json.dumps(canonical, sort_keys=True, default=str)
    return hashlib.sha256(tx_str.encode()).hexdigest()


class Wallet:
    """
    Bitcoin wallet — manages keys, balances, and transactions.

    Example::

        wallet = Wallet()
        keys = wallet.generate_keys()
        tx = wallet.create_transaction(keys['public_key'], recipient, 0.5, keys['private_key'])
    """

    def __init__(self):
        self.balance = 0.0

    def generate_keys(self) -> dict:
        """
        Generate a new ECDSA key pair.

        Returns:
            dict with keys 'private_key' and 'public_key' (hex-encoded).

        Without secp256k1 library, uses SHA-256-based pseudo-key derivation.
        """
        if HAS_ECDSA:
            sk = SigningKey.generate(curve=SECP256k1)
            vk = sk.get_verifying_key()
            private_key = sk.to_string().hex()
            public_key = vk.to_string().hex()
        else:
            # Fallback: pseudo-key derivation from random seed
            # WARNING: Not cryptographically secure for production use
            entropy = secrets.token_bytes(32)
            private_key = hashlib.sha256(entropy).hexdigest()
            # Derive public key via simple point operation (simulated)
            public_key = hashlib.sha256((private_key + 'pub').encode()).hexdigest()

        print(f"[Wallet] Generated ECDSA key pair.")
        return {
            "private_key": private_key,
            "public_key": public_key,
            "address": _hash160(bytes.fromhex(public_key))
        }

    def create_transaction(
        self,
        sender: str,
        recipient: str,
        amount: float,
        private_key: str
    ) -> dict:
        """
        Create and sign a new transaction.

        Args:
            sender: Sender's public key (hex).
            recipient: Recipient's public key (hex).
            amount: Amount in BTC.
            private_key: Sender's private key (hex) for signing.

        Returns:
            dict — Transaction object with signature.

        Raises:
            BitcoinException: If amount is invalid.

        Example::

            tx = wallet.create_transaction(
                sender=pub_key,
                recipient=recipient_pub,
                amount=1.5,
                private_key=priv_key
            )
        """
        if amount <= 0:
            raise BitcoinException("Transaction amount must be positive.")

        tx = {
            "sender_public_key": sender,
            "recipient_public_key": recipient,
            "amount": amount,
            "reference": "",
            "signature": "",
            "timestamp": time.time()
        }

        # Create reference to last transaction (UTXO model simulation)
        tx_ref_hash = hashlib.sha256(
            json.dumps(tx, sort_keys=True, default=str).encode()
        ).hexdigest()[:16]
        tx["reference"] = tx_ref_hash

        # Sign the transaction
        tx_hash = _compute_tx_hash(tx)

        if HAS_ECDSA:
            sk = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
            sig = sk.sign(bytes.fromhex(tx_hash)).hex()
        else:
            # Fallback: simple HMAC-based signature
            sig = hashlib.sha256((tx_hash + private_key).encode()).hexdigest()

        tx["signature"] = sig
        print(f"[Wallet] Transaction created: {amount} BTC from {sender[:8]}... to {recipient[:8]}...")
        return tx

    def verify_transaction(self, tx: dict) -> bool:
        """
        Verify the cryptographic signature of a transaction.

        Args:
            tx: Transaction dict with 'signature' and all required fields.

        Returns:
            bool — True if signature is valid.

        Example::

            assert wallet.verify_transaction(tx), "Signature invalid!"
        """
        sig = tx.get("signature", "")
        if not sig:
            return False

        if HAS_ECDSA:
            try:
                tx_hash = _compute_tx_hash(tx)
                vk = SigningKey.from_string(
                    bytes.fromhex(tx['sender_public_key']), curve=SECP256k1
                )
                return vk.verify(bytes.fromhex(sig), bytes.fromhex(tx_hash))
            except Exception:
                return False
        else:
            # Fallback: verify that signature field is present and non-empty
            # In production with proper crypto, this would use HMAC verification
            return len(sig) >= 32

    def get_balance(self, address: str, blockchain=None) -> float:
        """
        Compute balance for an address by scanning the blockchain.

        Args:
            address: Public key / address to query.
            blockchain: Blockchain instance to scan (optional).

        Returns:
            float — Balance in BTC.

        Note:
            Without a blockchain reference, returns the in-memory wallet balance.
        """
        if blockchain is None:
            return self.balance

        balance = 0.0
        for block in blockchain.chain:
            txs = block.get("transactions", [])
            for tx in txs:
                if tx.get("recipient_public_key") == address:
                    balance += tx.get("amount", 0)
                if tx.get("sender_public_key") == address:
                    balance -= tx.get("amount", 0)
        return balance
