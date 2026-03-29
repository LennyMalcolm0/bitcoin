"""
Bitcoin Network Metrics API — Hashrate, TPS, and blockchain statistics.
"""

import time
import hashlib
import json


class NetworkAnalyzer:
    """
    Bitcoin network statistics analyzer.

    Provides hashrate estimation, transaction throughput metrics,
    and a formatted dashboard for monitoring chain health.

    Example::

        from api import NetworkAnalyzer, Blockchain
        blockchain = Blockchain()
        analyzer = NetworkAnalyzer(blockchain)
        stats = analyzer.get_transaction_volume()
    """

    def __init__(self, blockchain):
        """
        Initialize the analyzer with a blockchain reference.

        Args:
            blockchain: Blockchain instance to analyze.
        """
        self.blockchain = blockchain
        self.start_time = time.time()
        self.last_check_time = time.time()
        self.last_block_count = len(blockchain.chain)

    def calculate_hashrate(self, window_blocks: int = 5) -> float:
        """
        Estimate the network hashrate based on recent block times.

        Uses the formula::

            hashrate = (Difficulty * 2^32 * BlockCount) / TimeElapsed

        Args:
            window_blocks: Number of recent blocks to average over (default: 5).

        Returns:
            float — Estimated hashrate in MH/s (megahashes per second).

        Note:
            Uses a mock difficulty constant (1) for simulation.
            Real Bitcoin mainnet difficulty is dynamic (DAA).

        Example::

            mh_s = analyzer.calculate_hashrate(window_blocks=10)
            print(f"Hashrate: {mh_s} MH/s")
        """
        chain = self.blockchain.chain
        if len(chain) < 2:
            return 0.0

        recent = chain[-window_blocks:] if len(chain) >= window_blocks else chain
        time_elapsed = recent[-1]['timestamp'] - recent[0]['timestamp']

        if time_elapsed <= 0:
            return 0.0

        # Mock difficulty — real Bitcoin uses difficulty bits in block header
        mock_difficulty = 1
        estimated_hashes = (mock_difficulty * (2 ** 32)) * len(recent)
        hashrate_ps = estimated_hashes / time_elapsed

        return round(hashrate_ps / 10 ** 6, 2)  # Convert to MH/s

    def get_transaction_volume(self) -> dict:
        """
        Compute transaction volume statistics across the entire chain.

        Returns:
            dict with keys:
                - ``total_transactions``: Total confirmed transactions
                - ``tps``: Average transactions per second
                - ``avg_txs_per_block``: Average transactions per block

        Example::

            stats = analyzer.get_transaction_volume()
            print(f"Total TX: {stats['total_transactions']}, TPS: {stats['tps']}")
        """
        total_tx = 0
        for block in self.blockchain.chain:
            txs = block.get("transactions", [])
            total_tx += len(txs) if isinstance(txs, list) else 0

        uptime = time.time() - self.start_time
        tps = total_tx / uptime if uptime > 0 else 0.0
        avg_txs = total_tx / len(self.blockchain.chain) if self.blockchain.chain else 0.0

        return {
            "total_transactions": total_tx,
            "tps": round(tps, 4),
            "avg_txs_per_block": round(avg_txs, 2)
        }

    def get_block_reorg_resistance(self) -> float:
        """
        Estimate the cost of a 51% attack (reorg resistance score).

        Returns:
            float — Estimated cost in arbitrary units (higher = more secure).
        """
        chain_len = len(self.blockchain.chain)
        if chain_len < 6:
            return 0.0

        # A longer chain with consistent hashrate is harder to reorg
        recent_hashrate = self.calculate_hashrate(window_blocks=6)
        depth_factor = min(chain_len / 100, 1.0)  # Normalize to 0-1

        return round(recent_hashrate * depth_factor, 4)

    def get_block_interval_stats(self) -> dict:
        """
        Compute block interval statistics.

        Returns:
            dict with keys:
                - ``avg_interval``: Average time between blocks (seconds)
                - ``min_interval``: Minimum block interval
                - ``max_interval``: Maximum block interval

        Example::

            stats = analyzer.get_block_interval_stats()
            print(f"Avg block time: {stats['avg_interval']:.1f}s")
        """
        chain = self.blockchain.chain
        if len(chain) < 2:
            return {"avg_interval": 0, "min_interval": 0, "max_interval": 0}

        intervals = [
            chain[i]['timestamp'] - chain[i - 1]['timestamp']
            for i in range(1, len(chain))
        ]

        return {
            "avg_interval": round(sum(intervals) / len(intervals), 2),
            "min_interval": round(min(intervals), 2),
            "max_interval": round(max(intervals), 2)
        }

    def display_dashboard(self) -> None:
        """
        Print a formatted network statistics dashboard to stdout.

        Dashboard shows:
        - Network hashrate (MH/s)
        - Total transactions and TPS
        - Chain length and block interval stats

        Example::

            analyzer.display_dashboard()
            # --- Bitcoin Network Statistics ---
            # Hashrate:        0.45 MH/s
            # Total TX:        42
            # TPS:             0.0012
            # Chain length:    127
            # Avg block time:  8.3s
            # --------------------------------
        """
        hashrate = self.calculate_hashrate()
        volume = self.get_transaction_volume()
        block_stats = self.get_block_interval_stats()
        chain_len = len(self.blockchain.chain)

        print()
        print("--- Bitcoin Network Statistics ---")
        print(f"  Network Hashrate:       {hashrate} MH/s")
        print(f"  Total Transactions:      {volume['total_transactions']}")
        print(f"  Transactions Per Second: {volume['tps']}")
        print(f"  Avg TXs Per Block:       {volume['avg_txs_per_block']}")
        print(f"  Chain Length:            {chain_len}")
        print(f"  Avg Block Interval:      {block_stats['avg_interval']}s")
        print(f"  Min/Max Interval:        {block_stats['min_interval']}s / {block_stats['max_interval']}s")
        print("-" * 38)
        print()
