# nostr-deleted
A script to pull and parse deleted nostr messages from relays 

# Screenshot
<img src="https://github.com/ronaldstoner/nostr-deleted/blob/main/images/example.png?raw-true" alt="A text console showing deleted events and the correlated event content" width="400"> 

# Note
Different relay software may store, process, and return deletion events in different ways. Reply schemas have not yet been created for different relayer software.

# TODO
- Class everything
- main loop
- Expect different respones based on relayer type
- Fix websocket keepalive, timeout, and overall session management
- Terminate websocket and close connection gracefully on quit/exit/crash
- Implement additional NIPs (username from pubkey for example)
- Create switch to pull from local relay db or remote relay through websockets
