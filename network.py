import socket
import json
import threading
import time

BROADCAST_IP = "255.255.255.255"
PORT = 5005

# Stores the latest state received from every node
node_states = {}

# Thread safety
state_lock = threading.Lock()

# Prevent the listener from being started multiple times
_listener_started = False


def send_state(
    node_id,
    flood_risk,
    fire_risk,
    pollution_risk,
    flood_sensors=None,
    fire_sensors=None,
    pollution_sensors=None
):
    """
    Broadcast the current environmental state of this node.
    """

    message = {
        "type": "NODE_STATE",
        "node_id": node_id,
        "timestamp": time.time(),

        "flood_risk": round(float(flood_risk), 1),
        "fire_risk": round(float(fire_risk), 1),
        "pollution_risk": round(float(pollution_risk), 1),

        "flood_sensors": flood_sensors or {},
        "fire_sensors": fire_sensors or {},
        "pollution_sensors": pollution_sensors or {}
    }

    data = json.dumps(message).encode("utf-8")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        sock.sendto(data, (BROADCAST_IP, PORT))
    except Exception as e:
        print("Network send error:", e)
    finally:
        sock.close()


def send_alert(node_id, hazard, risk):
    """
    Broadcast a critical hazard alert.
    """

    message = {
        "type": "ALERT",
        "node_id": node_id,
        "timestamp": time.time(),
        "hazard": hazard,
        "risk": round(float(risk), 1)
    }

    data = json.dumps(message).encode("utf-8")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        sock.sendto(data, (BROADCAST_IP, PORT))
    except Exception as e:
        print("Alert send error:", e)
    finally:
        sock.close()


def _listen():
    """
    Continuously listen for messages from other environmental nodes.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind(("", PORT))
    except Exception as e:
        print("Could not bind UDP port:", e)
        return

    while True:

        try:
            data, address = sock.recvfrom(65535)

            message = json.loads(data.decode("utf-8"))

            node_id = message.get("node_id")

            if not node_id:
                continue

            # Store the latest state
            with state_lock:

                if message.get("type") == "NODE_STATE":

                    node_states[node_id] = message

                elif message.get("type") == "ALERT":

                    # Preserve alert information
                    if node_id not in node_states:
                        node_states[node_id] = {
                            "node_id": node_id
                        }

                    node_states[node_id]["last_alert"] = message

                    node_states[node_id]["last_alert_time"] = time.time()

        except json.JSONDecodeError:
            print("Received invalid network message.")

        except Exception as e:
            print("Network listener error:", e)


def start_listener():
    """
    Start the network listener exactly once.
    """

    global _listener_started

    if _listener_started:
        return

    _listener_started = True

    thread = threading.Thread(
        target=_listen,
        daemon=True
    )

    thread.start()


def get_node_states():
    """
    Return a copy of the latest state from all nodes.
    """

    with state_lock:
        return dict(node_states)