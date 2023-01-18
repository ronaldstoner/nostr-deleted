#!/usr/bin/env python3
#
# Project:      nostr deleted events parser
# Members:      ronaldstoner
#
# Changelog
# 0.1 - Initial PoC
version = "0.1"

import json
import asyncio
import websockets
import datetime
import time

# Different relays may give different results. Some timeout, some loop, some keep alive.
#relay = "wss://brb.io"
#relay = "wss://nostr.bitcoiner.social"
#relay = "wss://relay.stoner.com"
#relay = "wss://relay.nostr.bg"
#relay = "wss://relay.damus.io"
relay = "wss://relay.snort.social"

# Connect to the relay's websocket endpoint
async def connect_to_relay():
    print("Conneting to websocket...")
    async with websockets.connect(relay, ping_interval=30) as websocket:
        print("Connected to", relay)

        # Send a REQ message to subscribe to deletion events
        print("Subscribing to event types = 5")
        await websocket.send(json.dumps(["REQ", "subscription_id", {"kinds": [5]}]))

        while True:
            # Wait for an event from the relay
            event = json.loads(await websocket.recv())
            if event[0] == "EVENT":
                if event[2]["kind"] == 5:

                    # Parse the content of the deletion event
                    content = event[2]
                    # Iterate through the tags of the deletion event
                    for tag in content["tags"]:
                        if tag[0] == "e":
                            original_event_hash = tag[1]
                            # Query the relay for the original event
                            try:
                                await websocket.send(json.dumps(["REQ", "subscription_id", {"id": [original_event_hash]}]))
                                original_event = json.loads(await websocket.recv())

                                # Output the text of the original event
                                if original_event[2]["content"] != "":
                                    print("---TYPE 5 DELETE EVENT---")
                                    print("Author:              ", event[2]["pubkey"])
                                    print("Time:                ", datetime.datetime.                        fromtimestamp(event[2]["created_at"]).strftime('%Y-%m-%d %H:%M:%S'))
                                    print("Type 5 Event ID:     ", event[2]["id"])
                                    print("Deletion Reason:     ", event[2]["content"])
                                    print("Requested Delete ID: ", tag[1])
                                    print("---ORIGINAL EVENT---")
                                    print("Author:              ", original_event[2]["pubkey"])
                                    print("Time:                ", datetime.datetime.fromtimestamp(original_event[2]["created_at"]).strftime('%Y-%m-%d %H:%M:%S'))
                                    print("Deleted Event ID:    ", original_event[2]["id"])
                                    print("Deleted Content:     ", original_event[2]["content"])
                                    print("\n")
                            except:
                                print("Cannot find deleted event")
#asyncio.get_event_loop().run_until_complete(connect_to_relay())
loop = asyncio.get_event_loop()
loop.run_until_complete(connect_to_relay())
websocket.close()
print("Connection closed to", relay)
