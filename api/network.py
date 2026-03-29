"""
Bitcoin P2P Network API — Peer discovery and message broadcasting.
"""

import time
import hashlib
import json


# Known Bitcoin DNS seeds (bootstrap peers for the Bitcoin network)
DNS_SEEDS = [
    "seed.bitcoin.sipa.be",
    "dnsseed.bluematt.me",
    "dnsseed.bitcoin.dashjr.org",
    "seed.bitcoin.jonasschnelli.ch",
    "seed.btc.petertodd.org",
]


class P2PNetwork:
    """
    Bitcoin P2P Network layer — peer discovery and message routing.

    Manages the set of connected peers and handles broadcasting of
    transactions and blocks to the network.

    Example::

        network = P2PNetwork()
        peers = network.connect_to_seed_nodes()
        network.broadcast_transaction(tx)
    """

    def __init__(self):
        self.peers = []
        self.mempool = []  # Local transaction mempool
        self.inventory = {}  # inv messages: {hash -> type}

    def connect_to_seed_nodes(self) -> list:
        """
        Discover and connect to peer nodes via DNS seeds.

        In production, DNS seeds return a list of IP addresses running
        Bitcoin nodes. Here we simulate with a set of known peer addresses.

        Returns:
            list — List of connected peer addresses (IP:port strings).

        Example::

            peers = network.connect_to_seed_nodes()
            # ['192.168.1.1:8333', '10.0.0.5:8333']
        """
        # Simulate peer discovery
        discovered_peers = [
            f"192.168.{i}.{j}:8333"
            for i in range(1, 5)
            for j in range(100, 105)
        ]
        self.peers = discovered_peers[:8]  # Limit to 8 peers
        print(f"[P2P Network] Connected to {len(self.peers)} peers.")
        return self.peers

    def add_peer(self, address: str) -> None:
        """
        Manually add a peer to the connection list.

        Args:
            address: Peer address in 'IP:port' format.

        Example::

            network.add_peer("203.0.113.42:8333")
        """
        if address not in self.peers:
            self.peers.append(address)

    def remove_peer(self, address: str) -> None:
        """
        Remove a disconnected or unresponsive peer.

        Args:
            address: Peer address to remove.

        Example::

            network.remove_peer("203.0.113.42:8333")
        """
        if address in self.peers:
            self.peers.remove(address)

    def broadcast_transaction(self, tx: dict) -> None:
        """
        Broadcast a transaction to all connected peers.

        Implements the INV/GETDATA pattern:
        1. Send INV (inventory) message with tx hash
        2. Peers request tx via GETDATA
        3. Respond with TX message

        Args:
            tx: Transaction dict to broadcast.

        Example::

            network.broadcast_transaction(tx)
        """
        tx_hash = hashlib.sha256(
            json.dumps(tx, sort_keys=True, default=str).encode()
        ).hexdigest()

        self.mempool.append(tx_hash)
        self.inventory[tx_hash] = "tx"

        print(f"[P2P Network] Broadcasting TX {tx_hash[:8]}... to {len(self.peers)} peers.")
        for peer in self.peers:
            self._send_to_peer(peer, "inv", {"type": "tx", "hash": tx_hash})

    def broadcast_block(self, block: dict) -> None:
        """
        Broadcast a newly mined block to all connected peers.

        Args:
            block: Block dict to broadcast.

        Example::

            network.broadcast_block(mined_block)
        """
        block_hash = block.get('hash', '')
        if not block_hash:
            block_hash = hashlib.sha256(
                json.dumps(block, sort_keys=True, default=str).encode()
            ).hexdigest()

        self.inventory[block_hash] = "block"
        print(f"[P2P Network] Broadcasting BLOCK {block_hash[:8]}... to {len(self.peers)} peers.")
        for peer in self.peers:
            self._send_to_peer(peer, "inv", {"type": "block", "hash": block_hash})

    def request_block(self, index: int, peer: str = None) -> dict | None:
        """
        Request a specific block by index from a peer.

        Args:
            index: Block height to request.
            peer: Specific peer to query (None = any connected peer).

        Returns:
            Block dict if found and returned, None otherwise.

        Example::

            block = network.request_block(42)
        """
        target_peer = peer or (self.peers[0] if self.peers else None)
        if not target_peer:
            print("[P2P Network] No peers available for block request.")
            return None

        print(f"[P2P Network] Requesting block #{index} from {target_peer}.")
        return self._request_from_peer(target_peer, "getdata", {"type": "block", "index": index})

    def request_transaction(self, tx_hash: str, peer: str = None) -> dict | None:
        """
        Request a specific transaction by hash from a peer.

        Args:
            tx_hash: Transaction hash to request.
            peer: Specific peer to query (None = any connected peer).

        Returns:
            Transaction dict if found and returned, None otherwise.
        """
        target_peer = peer or (self.peers[0] if self.peers else None)
        if not target_peer:
            return None

        return self._request_from_peer(target_peer, "getdata", {"type": "tx", "hash": tx_hash})

    def get_mempool(self) -> list:
        """
        Return the local mempool (pending transactions).

        Returns:
            list — List of transaction hashes in the mempool.
        """
        return list(self.mempool)

    def get_peer_count(self) -> int:
        """
        Return the number of connected peers.

        Returns:
            int — Peer count.
        """
        return len(self.peers)

    # --- Internal methods ---

    def _send_to_peer(self, peer: str, msg_type: str, payload: dict) -> None:
        """Simulate sending a message to a peer."""
        # In production, this opens a TCP socket and sends Bitcoin wire protocol messages
        pass

    def _request_from_peer(self, peer: str, msg_type: str, payload: dict) -> dict | None:
        """
        Simulate a request/response with a peer.

        In production, this implements the full Bitcoin P2P wire protocol
        over TCP (version, verack, getdata, tx, block messages).
        """
        # Simulate successful response after network delay
        return None  # Subclasses or integration tests implement real responses
