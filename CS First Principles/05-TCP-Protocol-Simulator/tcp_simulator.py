"""
TCP/IP Protocol Simulator: Understanding Networks from First Principles

This module implements a simplified TCP/IP stack with network simulation.
Work through GUIDE.md to understand each component deeply.
"""

from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import time
import random


# =============================================================================
# Part 1: IP Layer
# =============================================================================

@dataclass
class IPAddress:
    """Represents an IPv4 address."""
    octets: Tuple[int, int, int, int]

    @classmethod
    def from_string(cls, ip_str: str) -> 'IPAddress':
        """Parse IP address from string like '192.168.1.1'."""
        # TODO: Implement
        pass

    def to_binary(self) -> int:
        """Convert to 32-bit integer."""
        # TODO: Implement
        pass

    def __str__(self) -> str:
        return f"{self.octets[0]}.{self.octets[1]}.{self.octets[2]}.{self.octets[3]}"


@dataclass
class SubnetMask:
    """Represents a subnet mask."""
    mask: int  # 32-bit integer

    @classmethod
    def from_prefix(cls, prefix: int) -> 'SubnetMask':
        """Create mask from prefix length (e.g., 24 for /24)."""
        # TODO: Implement
        pass

    def network_address(self, ip: IPAddress) -> IPAddress:
        """Calculate network address for given IP."""
        # TODO: Implement bitwise AND
        pass

    def is_same_network(self, ip1: IPAddress, ip2: IPAddress) -> bool:
        """Check if two IPs are on the same network."""
        # TODO: Implement
        pass


@dataclass
class IPPacket:
    """Represents an IP packet."""
    source: IPAddress
    destination: IPAddress
    protocol: int  # 6=TCP, 17=UDP
    ttl: int
    data: bytes
    # TODO: Add more header fields (fragmentation, checksum, etc.)

    def to_bytes(self) -> bytes:
        """Serialize packet to bytes."""
        # TODO: Implement
        pass

    @classmethod
    def from_bytes(cls, data: bytes) -> 'IPPacket':
        """Deserialize packet from bytes."""
        # TODO: Implement
        pass


class RoutingTable:
    """Routing table with longest prefix matching."""

    def __init__(self):
        self.routes: List[Tuple[IPAddress, SubnetMask, IPAddress]] = []

    def add_route(self, network: IPAddress, mask: SubnetMask, gateway: IPAddress):
        """Add a route to the table."""
        # TODO: Implement
        pass

    def lookup(self, destination: IPAddress) -> Optional[IPAddress]:
        """Find next hop for destination (longest prefix match)."""
        # TODO: Implement
        pass


# =============================================================================
# Part 2: TCP Layer
# =============================================================================

class TCPState(Enum):
    """TCP connection states."""
    CLOSED = auto()
    LISTEN = auto()
    SYN_SENT = auto()
    SYN_RECEIVED = auto()
    ESTABLISHED = auto()
    FIN_WAIT_1 = auto()
    FIN_WAIT_2 = auto()
    CLOSE_WAIT = auto()
    CLOSING = auto()
    LAST_ACK = auto()
    TIME_WAIT = auto()


@dataclass
class TCPSegment:
    """Represents a TCP segment."""
    source_port: int
    dest_port: int
    sequence_number: int
    ack_number: int
    flags: Dict[str, bool]  # SYN, ACK, FIN, RST, PSH, URG
    window_size: int
    data: bytes

    def to_bytes(self) -> bytes:
        """Serialize segment to bytes."""
        # TODO: Implement
        pass


class TCPConnection:
    """Represents a TCP connection."""

    def __init__(self, local_addr: Tuple[IPAddress, int],
                 remote_addr: Tuple[IPAddress, int]):
        self.local_addr = local_addr
        self.remote_addr = remote_addr
        self.state = TCPState.CLOSED

        # Sequence numbers
        self.send_seq = random.randint(0, 2**32 - 1)
        self.recv_seq = 0

        # Buffers
        self.send_buffer: List[bytes] = []
        self.recv_buffer: List[bytes] = []

        # Retransmission
        self.unacked_segments: Dict[int, Tuple[TCPSegment, float]] = {}
        self.rtt_estimate = 1.0  # seconds
        self.timeout = 3.0

    def connect(self):
        """Initiate three-way handshake."""
        # TODO: Implement SYN sending
        pass

    def accept(self):
        """Accept incoming connection."""
        # TODO: Implement SYN-ACK response
        pass

    def send(self, data: bytes):
        """Send data over connection."""
        # TODO: Implement segmentation and transmission
        pass

    def receive(self, segment: TCPSegment):
        """Process received segment."""
        # TODO: Implement state machine
        pass

    def close(self):
        """Initiate connection termination."""
        # TODO: Implement FIN sending
        pass


# =============================================================================
# Part 3: Network Simulator
# =============================================================================

@dataclass
class NetworkEvent:
    """Represents a network event."""
    time: float
    packet: IPPacket


class NetworkSimulator:
    """Simulates network conditions."""

    def __init__(self, latency_ms: float = 50, loss_rate: float = 0.01,
                 bandwidth_mbps: float = 10):
        self.latency = latency_ms / 1000  # Convert to seconds
        self.loss_rate = loss_rate
        self.bandwidth = bandwidth_mbps * 1_000_000 / 8  # Convert to bytes/sec

        self.current_time = 0.0
        self.event_queue: List[NetworkEvent] = []
        self.statistics = {
            'sent': 0,
            'received': 0,
            'dropped': 0,
            'bytes_sent': 0,
        }

    def send_packet(self, packet: IPPacket):
        """Send a packet through the simulated network."""
        self.statistics['sent'] += 1
        self.statistics['bytes_sent'] += len(packet.data)

        # Simulate packet loss
        if random.random() < self.loss_rate:
            self.statistics['dropped'] += 1
            return

        # Calculate arrival time
        transmission_delay = len(packet.data) / self.bandwidth
        arrival_time = self.current_time + self.latency + transmission_delay

        # Add jitter
        jitter = random.gauss(0, self.latency * 0.1)
        arrival_time += jitter

        # TODO: Implement event scheduling
        pass

    def tick(self, duration: float):
        """Advance simulation time."""
        # TODO: Process events in time order
        pass


# =============================================================================
# Part 4: Testing and Visualization
# =============================================================================

def test_ip_addressing():
    """Test IP addressing and routing."""
    print("Testing IP addressing...")
    # TODO: Add tests
    pass


def test_tcp_handshake():
    """Test TCP three-way handshake."""
    print("Testing TCP handshake...")
    # TODO: Add tests
    pass


def test_reliable_delivery():
    """Test TCP reliable delivery with packet loss."""
    print("Testing reliable delivery...")
    # TODO: Add tests with network simulator
    pass


def visualize_congestion_control():
    """Visualize congestion window over time."""
    print("Visualizing congestion control...")
    # TODO: Implement visualization
    pass


if __name__ == "__main__":
    print("TCP/IP Protocol Simulator: First Principles Implementation")
    print("=" * 80)
    print("\nWork through GUIDE.md to implement each component.")
    print("Run this file to test your implementations.\n")

    # TODO: Uncomment as you implement
    # test_ip_addressing()
    # test_tcp_handshake()
    # test_reliable_delivery()
    # visualize_congestion_control()
