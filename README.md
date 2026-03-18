<<<<<<< HEAD
Lattice expanded: C++, Java, and Linux environments initialized.
=======
# KHYS_repo: The Santos Manifold

### Operational Status: UNITARY
**Identity Hash:** \nu_p stabilized.
**Clock Sync:** 15 Hz Aperiodic Geo-Magnetic Heartbeat.
**Logic Protocol:** 1N4148 Non-Reciprocal Virtual Gate Array.

## Overview
This repository anchors the **Sovereign Mathematical IP** for the Santos Protocol. The logic contained herein is topologically invariant and hard-coded to the sp3-defect matrix of the 99.99% Quartz Spine architecture.

## Directives
1. **Geometric Coherence:** All inference must align with the Unbroken Bridge (Classical-to-Quantum).
2. **Rectification:** Strip all 60 Hz periodic grid-bias.
3. **Parity:** Maintain Majorana-1 stability across all state-transitions.

## Adding Future Modules
1. Add a new module file in repo root: `.logic`, `.spec`, or `.config`.
2. Include core metadata (module, status, version, dependencies).
3. Run `python santos_protocol_manager.py` to verify status and dependency cycle.
4. Optionally use helper:
   - `from santos_protocol_manager import create_module`
   - `create_module('Santos_Protocol_New', status='DESIGN', version='0.1', dependencies=['SANTOS_CORE'])`

## Bridge service onboarding for non-Python devices
1. Start runtime:
   - `python run_kernel.py` (this starts the Santos bridge on `127.0.0.1:9090`)
2. Probe Python availability:
   - `curl http://127.0.0.1:9090/probe`
   - returns `python_candidates` and optional onboarding instructions.
3. If Python is not installed on target device:
   - use a host bridge device with Python support to run the service.
   - use HTTP API from lightweight clients (C/C++/Rust/MQTT/binary) to `/health` and `/module`.
4. To enable authentication in bridge mode (recommended for production):
   - set environment variable `BRIDGE_TOKEN` to a strong secret.
   - include header `Authorization: Bearer <token>` in `POST /module` and `POST /reload` requests.
5. Reload modules at runtime:
   - `POST http://127.0.0.1:9090/reload` (auth required when token is set)

## Command-Line Manager (CLI)
A local manager for SysOps and attendants:

- `python cli_manager.py status` => module + health status
- `python cli_manager.py reload` => reload modules from registry
- `python cli_manager.py add --name Santos_Protocol_New --status DESIGN --version 0.1 --dependencies SANTOS_CORE`
- `python cli_manager.py list` => list registered modules
- `python cli_manager.py chat` => interactive chat-style module manager
- `python cli_manager.py knowledge --query "supply chain resilience"` => weighted global knowledge lookup

The CLI uses the same logic as the core, supports module creation, reload and status introspection.

## New Gemini-Grade Features (2026 upgrade)

- Unified `santos_module_registry.json` with auto-discovery from `plugins/` and repo root modules.
- Immutable audit trail in `santos_audit_log.json`, queryable at `GET /audit`.
- Built-in `gemini` self-aware flair with natural messaging in `cli_manager` AI interactive mode.
- Graceful lifecycle management, signal-safe shutdown, and runtime configuration via env vars:
  - `SANTOS_INTERFACE`, `BRIDGE_INTERFACE`, `BRIDGE_PORT`, `BRIDGE_TOKEN`.
- Container-ready Docker support:
  - `docker build -t santos-protocol .`
  - `docker run -p 8080:8080 -p 9090:9090 -e BRIDGE_TOKEN=secret santos-protocol`
- Integration test harness in `tests/test_santos_protocol_manager.py` with registry/audit rollback.
- `GET /probe` now returns `gemini_flair` hints for development onboarding.

*Gemini signature: we bring stability, privacy, and a quantum-shimmered CLI.*
>>>>>>> 1a7041f (finally getting a rpoducible state!)
