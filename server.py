import socket
import threading
import time

TCP_PORT = 50001
UDP_PORT = 50002
clients = []


def broadcast_presence():
    """Continuously broadcast server IP over UDP."""
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = f"SERVER_IP_DISCOVERY:{TCP_PORT}".encode()
    while True:
        # Broadcast to the entire subnet
        udp_socket.sendto(message, ('<broadcast>', UDP_PORT))
        time.sleep(3)


def handle_pico(conn, addr):
    """Handle individual Pico TCP connection."""
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(conn)
    try:
        while True:
            data = conn.recv(1024)
            if not data: break
            print(f"[{addr}] says: {data.decode()}")
    except:
        pass
    finally:
        clients.remove(conn)
        conn.close()


# Start UDP Broadcaster in a separate thread
threading.Thread(target=broadcast_presence, daemon=True).start()

# Start TCP Server
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind(('0.0.0.0', TCP_PORT))
tcp_server.listen()

print(f"Server started. Discoverable on UDP {UDP_PORT}, listening on TCP {TCP_PORT}")
while True:
    conn, addr = tcp_server.accept()
    thread = threading.Thread(target=handle_pico, args=(conn, addr))
    thread.start()