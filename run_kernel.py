import json, os, threading, signal, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from santos_protocol_manager import collect_status, log_event, load_registry
from bridge_service import run_bridge

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "Santos_Protocol_Middleware.config")


def load_config(path):
    cfg = {}
    if not os.path.exists(path):
        return cfg
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                key, value = line.split(":", 1)
                cfg[key.strip().upper()] = value.strip()
    return cfg


class SantosHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ["/", "/health", "/status"]:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode("utf-8"))
            return

        moduled = collect_status()

        if self.path == "/health":
            overall = "OPERATIONAL" if all(m["status"] in ["OPERATIONAL", "ACTIVE"] for m in moduled["modules"]) else "DEGRADED"
            payload = {
                "status": overall,
                "module_order": moduled["module_order"],
                "modules": moduled["modules"],
            }
        else:
            payload = moduled

        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


http_server = None
bridge_thread = None

def graceful_shutdown(signum, frame):
    print(f"[STATUS] received shutdown signal {signum}, terminating services...")
    if http_server:
        http_server.shutdown()
    if bridge_thread and bridge_thread.is_alive():
        # signal `run_bridge` can also be closed by process exit
        pass
    log_event("shutdown", {"signal": signum})
    sys.exit(0)


def run_http(interface, port):
    global http_server
    http_server = HTTPServer((interface, port), SantosHandler)
    print(f"[STATUS] HTTP Santos Protocol API running at http://{interface}:{port}")
    log_event("run_http", {"interface": interface, "port": port})
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        print("[STATUS] KeyboardInterrupt received, shutting down HTTP server")
    finally:
        http_server.server_close()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)

    cfg = load_config(CONFIG_PATH)
    interface_full = os.getenv("SANTOS_INTERFACE", cfg.get("INTERFACE", "TCP://127.0.0.1:8080"))
    try:
        _, host_port = interface_full.split("//", 1)
        host, port_raw = host_port.split(":")
        port = int(port_raw)
        interface = host
    except Exception:
        interface = "127.0.0.1"
        port = 8080

    bridge_host = os.getenv("BRIDGE_INTERFACE", "127.0.0.1")
    bridge_port = int(os.getenv("BRIDGE_PORT", "9090"))

    bridge_thread = threading.Thread(target=run_bridge, kwargs={"interface": bridge_host, "port": bridge_port}, daemon=True)
    bridge_thread.start()

    print(f"[STATUS] Bridge thread started at http://{bridge_host}:{bridge_port}")
    load_registry()

    run_http(interface, port)
