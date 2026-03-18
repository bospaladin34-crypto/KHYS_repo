import json, os, shutil
from http.server import BaseHTTPRequestHandler, HTTPServer
from santos_protocol_manager import collect_status, create_module, reload_modules, load_registry, log_event, load_audit


def detect_python():
    candidates = ["python", "python3", "py"]
    found = {}
    for c in candidates:
        path = shutil.which(c)
        if path:
            found[c] = path
    return found


def onboarding_instructions():
    return {
        "step1": "Install Python 3.x from https://www.python.org/downloads/ if not already installed.",
        "step2": "Run 'python -m pip install --upgrade pip' to ensure pip is current.",
        "step3": "In repository folder, run 'python santos_protocol_manager.py' then 'python run_kernel.py'.",
        "step4": "For non-Python devices, call bridge API at http://127.0.0.1:9090/health and /module.",
    }


class BridgeHandler(BaseHTTPRequestHandler):
    def _send_json(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _get_expected_token(self):
        return os.environ.get("BRIDGE_TOKEN", "").strip()

    def _authenticate(self):
        expected = self._get_expected_token()
        if not expected:
            return True
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth.split("Bearer ", 1)[1].strip()
            return token == expected
        return False

    def do_GET(self):
        if self.path == "/health" or self.path == "/status":
            summary = collect_status()
            overall = "OPERATIONAL" if all(m["status"] in ["OPERATIONAL", "ACTIVE"] for m in summary["modules"]) else "DEGRADED"
            self._send_json(200, {"status": overall, "modules": summary["modules"], "module_order": summary["module_order"]})
            return

        if self.path == "/modules":
            summary = collect_status()
            self._send_json(200, summary)
            return

        if self.path == "/probe":
            p = detect_python()
            self._send_json(200, {
                "python_candidates": p,
                "onboarding": onboarding_instructions(),
                "gemini_flair": "☄️ you have arrived at Santos Bridge 2.0 with cosmic resiliency",
            })
            return

        if self.path.startswith("/knowledge"):
            # URL can be /knowledge?q=<text>
            query = ""
            if "?" in self.path:
                _, qs = self.path.split("?", 1)
                for kv in qs.split("&"):
                    if kv.startswith("q="):
                        query = kv.split("=", 1)[1]
                        break
            from santos_protocol_manager import get_global_knowledge
            results = get_global_knowledge(query)
            self._send_json(200, {
                "query": query,
                "results": results,
                "guide": "Add real-world data sources by editing santos_knowledge_corpus.json",
            })
            return

        if self.path == "/audit":
            audit = load_audit()
            self._send_json(200, {
                "audit_entries": audit,
                "count": len(audit),
            })
            return

        self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        if not self._authenticate():
            self._send_json(401, {"error": "Unauthorized"})
            return

        if self.path == "/module":
            length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(length).decode("utf-8")

            try:
                payload = json.loads(data)
            except json.JSONDecodeError:
                self._send_json(400, {"error": "Invalid JSON"})
                return

            module_name = payload.get("module_name")
            status = payload.get("status", "OPERATIONAL")
            version = payload.get("version", "1.0")
            dependencies = payload.get("dependencies", [])
            keys = payload.get("keys", {})

            if not module_name:
                self._send_json(422, {"error": "module_name is required"})
                return

            try:
                created = create_module(module_name, status=status, version=version, dependencies=dependencies, keys=keys)
                log_event("bridge_create_module", {"module": module_name, "origin": self.client_address[0]})
                self._send_json(201, {"module": created, "status": "created"})
            except FileExistsError as e:
                self._send_json(409, {"error": str(e)})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        if self.path == "/reload":
            try:
                result = reload_modules()
                log_event("bridge_reload", {"origin": self.client_address[0], "module_count": len(result.get("modules", []))})
                self._send_json(200, {"status": "reloaded", "module_count": len(result.get("modules", []))})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        self._send_json(404, {"error": "Not found"})

        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON"})
            return

        module_name = payload.get("module_name")
        status = payload.get("status", "OPERATIONAL")
        version = payload.get("version", "1.0")
        dependencies = payload.get("dependencies", [])
        keys = payload.get("keys", {})

        if not module_name:
            self._send_json(422, {"error": "module_name is required"})
            return

        try:
            created = create_module(module_name, status=status, version=version, dependencies=dependencies, keys=keys)
            self._send_json(201, {"module": created, "status": "created"})
        except FileExistsError as e:
            self._send_json(409, {"error": str(e)})
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def log_message(self, format, *args):
        return


def run_bridge(interface="127.0.0.1", port=9090):
    server = HTTPServer((interface, port), BridgeHandler)
    print(f"[STATUS] Santos Bridge API running at http://{interface}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_bridge()