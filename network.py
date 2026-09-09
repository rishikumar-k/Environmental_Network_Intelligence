import socket
import json
import threading
import queue

BROADCAST_IP = "255.255.255.255"
PORT = 5005

alert_queue = queue.Queue()


def send_alert(node_id, hazard, risk):
    """Broadcast an environmental alert to other nodes."""

    message = {
        "node_id": node_id,
        "hazard": hazard,
        "risk": round(float(risk), 1)
    }

    data = json.dumps(message).encode("utf-8")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        sock.sendto(data, (BROADCAST_IP, PORT))
    finally:
        sock.close()


def _listen():
    """Continuously listen for alerts from other nodes."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("", PORT))

    while True:
        try:
            data, address = sock.recvfrom(4096)

            message = json.loads(data.decode("utf-8"))

            alert_queue.put(message)

        except Exception as e:
            print("Network listener error:", e)


def start_listener():
    """Start the network listener in the background."""

    thread = threading.Thread(
        target=_listen,
        daemon=True
    )

    thread.start()


def get_alerts():
    """Return all alerts currently waiting in the queue."""

    alerts = []

    while not alert_queue.empty():
        alerts.append(alert_queue.get())

    return alerts