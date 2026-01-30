"""
Hollister Swarm Server – Python (Annotated)

This program acts as the CENTRAL SERVER for all Pico clients.

It has two main jobs:

1. UDP Discovery
   - Periodically broadcasts its presence so clients can find it
   - This avoids hard-coding IP addresses on robots

2. TCP Server
   - Accepts reliable, long-lived connections from Pico clients
   - Receives messages from each connected device

Think of this like:
- UDP = "Hey robots, I'm over here!"
- TCP = "Okay, now let's talk."
"""

# -------------------------
# Imports
# -------------------------

import socket       # Low-level networking (UDP + TCP)
import threading    # Allows multiple things to run at the same time
import time         # Used for delays (sleep)

# -------------------------
# Network Configuration
# -------------------------

TCP_PORT = 50001    # Port used for reliable TCP connections
UDP_PORT = 50002    # Port used for UDP discovery broadcasts

# List to keep track of connected clients
clients = []

# -------------------------
# UDP Discovery Broadcaster
# -------------------------
# This function runs in the background.
# It repeatedly broadcasts a message announcing:
#   - "I am the server"
#   - "Here is the TCP port you should connect to"

def broadcast_presence():
    """Continuously broadcast server presence over UDP."""

    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Enable broadcast mode (required to send to <broadcast>)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Message format expected by the Pico clients
    # Example: SERVER_IP_DISCOVERY:50001
    message = f"SERVER_IP_DISCOVERY:{TCP_PORT}".encode()

    while True:
        # Send the message to every device on the local network
        udp_socket.sendto(message, ('<broadcast>', UDP_PORT))

        # Broadcast every 3 seconds
        time.sleep(3)

# -------------------------
# TCP Client Handler
# -------------------------
# Each Pico that connects gets its own thread.
# This lets multiple robots talk to the server at once.

def handle_pico(conn, addr):
    """Handle communication with a single Pico client."""

    print(f"[NEW CONNECTION] {addr} connected.")

    # Track the client connection
    clients.append(conn)

    try:
        while True:
            # Receive up to 1024 bytes from the client
            data = conn.recv(1024)

            # If recv() returns empty bytes, the client disconnected
            if not data:
                break

            # Print whatever the Pico sent
            print(f"[{addr}] says: {data.decode()}")

    except Exception as e:
        # Catch unexpected errors (client crash, network issue, etc.)
        print(f"[ERROR] Connection issue with {addr}: {e}")

    finally:
        # Clean up when the client disconnects
        clients.remove(conn)
        conn.close()
        print(f"[DISCONNECTED] {addr}")

# -------------------------
# Start UDP Broadcaster Thread
# -------------------------
# This runs independently of the TCP server.
# `daemon=True` means it automatically stops when the program exits.

threading.Thread(
    target=broadcast_presence,
    daemon=True
).start()

# -------------------------
# Start TCP Server
# -------------------------

# Create TCP socket
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to all network interfaces so any device can connect
tcp_server.bind(('0.0.0.0', TCP_PORT))

# Start listening for incoming connections
tcp_server.listen()

print(
    f"Server started.\n"
    f" - Broadcasting on UDP port {UDP_PORT}\n"
    f" - Listening for TCP connections on port {TCP_PORT}"
)

# -------------------------
# Main Accept Loop
# -------------------------
# This loop waits for new Pico connections forever.

while True:
    # accept() blocks until a client connects
    conn, addr = tcp_server.accept()

    # Create a new thread for each client
    thread = threading.Thread(
        target=handle_pico,
        args=(conn, addr)
    )
    thread.start()
