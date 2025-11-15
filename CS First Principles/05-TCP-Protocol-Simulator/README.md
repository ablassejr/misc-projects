# Project 05: TCP/IP Protocol Simulator

## Overview

This project teaches you how computer networks work by implementing the TCP/IP protocol stack from scratch. You'll understand how reliable communication is built on top of an unreliable network.

## What You'll Learn

- The layered architecture of network protocols
- IP addressing, routing, and fragmentation
- TCP connection management (three-way handshake)
- Reliable delivery through acknowledgments and retransmission
- Flow control and congestion control
- How the internet actually works

## Key Concepts

### IP Layer (Network Layer)
- Addressing and subnetting
- Routing and forwarding
- Packet fragmentation and reassembly
- TTL and loop prevention

### TCP Layer (Transport Layer)
- Connection establishment and termination
- Sequence numbers and acknowledgments
- Reliable delivery and retransmission
- Flow control (sliding window)
- Congestion control (slow start, AIMD)

### Network Simulation
- Packet loss and delays
- Bandwidth limitations
- Reordering and duplication
- Statistics and analysis

## How to Use

### Self-Guided Learning
1. Study `GUIDE.md` section by section
2. Implement each layer incrementally
3. Test with the network simulator
4. Analyze performance under different conditions

### Claude Code CLI Guided Mode
```bash
claude-code "Walk me through implementing TCP/IP from first principles. Start with IP addressing and routing."
```

## Prerequisites

- Strong Python knowledge
- Understanding of binary operations (Project 01)
- Completed Projects 01-04 or equivalent

## Time Estimate

- Fast path: 10-12 hours
- Deep understanding: 20-25 hours
- Mastery: 30+ hours

## Success Criteria

You've mastered this project when you can:
- Explain how TCP provides reliable delivery
- Implement a working TCP/IP stack
- Debug network issues from first principles
- Analyze performance trade-offs
- Design network protocols

## Real-World Applications

Understanding TCP/IP helps you:
- Debug network connectivity issues
- Optimize application performance
- Design APIs and protocols
- Understand security vulnerabilities
- Build distributed systems

## Extensions

- Implement UDP
- Add IPv6 support
- Build HTTP on top of TCP
- Implement DNS resolution
- Create a simple VPN
- Study QUIC protocol
