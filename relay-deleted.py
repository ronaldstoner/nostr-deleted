#!/usr/bin/env python3
#
# Project:      nostr deleted events parser
# Members:      ronaldstoner
#
# Changelog
# 0.1 - Initial PoC
# 0.2 - Refactored code and websockets
version = "0.2"

import json
import asyncio
import websockets
import datetime

# Different relays may give different results. Some timeout, some loop, some keep alive.
#relay = "wss://brb.io"
#relay = "wss://nostr.rocks"
#relay = "wss://nostr.bitcoiner.social"
relay = "wss://relay.stoner.com"
#relay = "wss://nostr.fmt.wiz.biz"
#relay = "wss://relay.nostr.bg"
#relay = "wss://relay.damus.io"
#relay = "wss://relay.snort.social"

async def connect_to_relay():
    print("Connecting to websocket...")
    async with websockets.connect(relay, ping_interval=30) as websocket:
        print(f"Connected to {relay}")

        # Send a REQ message to subscribe to deletion events
        print("Subscribing to event types = 5")
        await websocket.send(json.dumps(["REQ", "subscription_id", {"kinds": [5]}]))

        original_events = {}
        while True:
            try:
                event = json.loads(await websocket.recv())
            except asyncio.IncompleteReadError as e:
                event = e.partial
            if event[0] == "EVENT" and event[2]["kind"] == 5:
                content = event[2]
                for tag in content["tags"]:
                    if tag[0] == "e":
                        original_event_hash = tag[1]
                        if original_event_hash not in original_events:
                            try:
                                await websocket.send(json.dumps(["REQ", "subscription_id", {"id": [original_event_hash]}]))
                                original_event = json.loads(await websocket.recv())
                                original_events[original_event_hash] = original_event
                            except:
                                print("Cannot find deleted event")
                        await handle_event(event, original_events[original_event_hash])

async def handle_event(event, original_event):
    if original_event[2]["content"] != "":

        print("---TYPE 5 DELETE EVENT---")
        print(f"Author:              {event[2]['pubkey']}")
        print(f"Time:                {datetime.datetime.fromtimestamp(event[2]['created_at']).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Type 5 Event ID:     {event[2]['id']}")
        print(f"Deletion Reason:     {event[2]['content']}")
        print(f"Requested Delete ID: {original_event[2]['id']}")
        print("---ORIGINAL EVENT---")
        print(f"Author:              {original_event[2]['pubkey']}")
        print(f"Time:                {datetime.datetime.fromtimestamp(original_event[2]['created_at']).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Deleted Event ID:    {original_event[2]['id']}")
        print(f"Deleted Content:     {original_event[2]['content']}\n")

loop = asyncio.get_event_loop()
loop.run_until_complete(connect_to_relay())
websocket.close()
print(f"Connection closed to {relay}")

