# Hollister Swarm Server

This repository contains the **central server** for the Hollister Swarm project.

The server runs on a **laptop or desktop computer** and allows multiple Raspberry Pi Pico clients to:
- Discover the server automatically
- Connect reliably
- Send messages back to the server

This mirrors how real-world robotics fleets, IoT systems, and multiplayer servers work.

---

## What This Server Does

The server performs **two networking roles at the same time**:

### 1. UDP Discovery (Broadcast)
- The server repeatedly broadcasts a message to the local network
- Pico clients listen for this message
- This allows clients to find the server **without hard-coding an IP address**

### 2. TCP Communication (Reliable Connection)
- Once discovered, clients connect using TCP
- Each client gets its own connection
- Messages from clients are printed on the server

---

## Network Ports Used

| Purpose | Protocol | Port |
|------|--------|------|
| Server discovery | UDP | 50002 |
| Client communication | TCP | 50001 |

⚠️ These ports must be open on the laptop’s firewall.

---

## Requirements

- Python 3.9 or newer
- A laptop or desktop connected to the **same Wi-Fi network** as the Pico clients
- No additional Python libraries required (standard library only)

---

## File Overview
```
server.py # Main server program
README.md # This file
```


---

## How to Run the Server

1. Clone or download this repository:
```
git clone https://github.com/Hollister-Advanced-Engineering/hollister_swarm_server
```

2. Navigate into the directory:
```
cd hollister_swarm_server
```


3. Run the server:
```
python server.py
```


4. You should see output similar to:
```
Server started.
- Broadcasting on UDP port 50002
- Listening for TCP connections on port 50001
```


The server is now running and discoverable.

---

## What Happens When a Pico Connects

- The Pico discovers the server via UDP
- The Pico opens a TCP connection
- The server prints messages sent by the Pico:
```
[NEW CONNECTION] ('192.168.1.42', 53781)
[192.168.1.42] says: Hello from CircuitPython!
```

Each Pico runs in its own thread, so multiple clients can connect at once.

---

## Common Issues & Fixes

### Pico cannot find the server
- Ensure both devices are on the **same Wi-Fi network**
- Check firewall settings (UDP + TCP allowed)
- Confirm the server is running before powering the Pico

### Server starts but shows no connections
- Pico may not be connected to Wi-Fi
- Verify ports match between client and server
- Check Pico serial output for errors

### Firewall Problems
You may need to allow Python through your firewall:
- **Windows**: Allow Python through Windows Defender Firewall
- **macOS**: System Settings → Network → Firewall
- **Linux**: Allow UDP 50002 and TCP 50001

---

## Design Notes (Why This Matters)

- UDP discovery avoids fragile IP configuration
- TCP ensures ordered, reliable messages
- Threads enable real multi-client systems
- This architecture scales to:
- Robot swarms
- IoT fleets
- Game servers
- Distributed sensing systems

---

## Next Steps (Planned Extensions)

- Client registration & IDs
- Server → client command messages
- Heartbeat / disconnect detection
- Shared state between robots
- Visualization dashboard

---

## Classroom Rule

Do **not** modify `server.py` unless instructed.  
All robot behavior should be implemented on the client side.

---

You are now running a real networked system.  
Welcome to distributed robotics. 🚀

