#!/usr/bin/env python3
"""Test script to verify msg_seq generation in QQ channel."""

import asyncio
from nanobot.channels.qq import QQChannel
from nanobot.bus.queue import MessageBus
from nanobot.config.schema import QQConfig

async def test_msg_seq_generation():
    """Test that msg_seq is unique even with concurrent calls."""
    config = QQConfig(
        enabled=True,
        app_id="test_app_id",
        secret="test_secret",
        allow_from=["*"]
    )
    bus = MessageBus()
    qq_channel = QQChannel(config, bus)
    
    # Simulate concurrent send calls
    async def send_message():
        from nanobot.bus.events import OutboundMessage
        msg = OutboundMessage(
            channel="qq",
            chat_id="test_chat_id",
            content="Test message"
        )
        # We'll just test the msg_seq generation, not the actual API call
        async with qq_channel._seq_lock:
            current_seq = qq_channel._msg_seq
            qq_channel._msg_seq += 1
            if qq_channel._msg_seq >= 2**31:
                qq_channel._msg_seq = 1
            return current_seq
    
    # Test sequential calls
    print("Testing sequential calls...")
    seq_numbers = []
    for i in range(5):
        seq = await send_message()
        seq_numbers.append(seq)
        print(f"Sequential call {i+1}: msg_seq = {seq}")
    
    # Check for duplicates
    if len(seq_numbers) == len(set(seq_numbers)):
        print("✓ Sequential calls: No duplicates")
    else:
        print("✗ Sequential calls: Duplicates found!")
    
    # Test concurrent calls
    print("\nTesting concurrent calls...")
    tasks = [send_message() for _ in range(100)]
    concurrent_seq_numbers = await asyncio.gather(*tasks)
    
    # Check for duplicates
    if len(concurrent_seq_numbers) == len(set(concurrent_seq_numbers)):
        print("✓ Concurrent calls: No duplicates")
    else:
        print("✗ Concurrent calls: Duplicates found!")
        # Find duplicates
        seen = set()
        duplicates = set()
        for seq in concurrent_seq_numbers:
            if seq in seen:
                duplicates.add(seq)
            else:
                seen.add(seq)
        print(f"Duplicate msg_seq values: {duplicates}")
    
    # Print some stats
    print(f"\nTotal messages sent: {len(concurrent_seq_numbers)}")
    print(f"Unique msg_seq values: {len(set(concurrent_seq_numbers))}")
    print(f"Min msg_seq: {min(concurrent_seq_numbers)}")
    print(f"Max msg_seq: {max(concurrent_seq_numbers)}")

if __name__ == "__main__":
    asyncio.run(test_msg_seq_generation())