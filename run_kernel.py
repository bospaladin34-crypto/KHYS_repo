import socket, json, threading, time
def run_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(('127.0.0.1', 8080))
        print("[DEBUG: BIND_SUCCESS]")
        s.listen(1)
        print("[STATUS: LISTENING_ON_PORT_8080]")
        while True:
            conn, addr = s.accept()
            payload = {"integrity": 1.0, "status": "stable"}
            conn.sendall(json.dumps(payload).encode('utf-8'))
            conn.close()
    except Exception as e:
        print(f"[DEBUG: ERROR -> {e}]")

thread = threading.Thread(target=run_server, daemon=True)
thread.start()
while True: time.sleep(1)
