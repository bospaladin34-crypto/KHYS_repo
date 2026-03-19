import json
import os
import datetime

MODULES = [
    "Santos_Protocol_Core.logic",
    "Santos_Protocol_Adaptive.spec",
    "Santos_Protocol_Middleware.config",
]

REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "santos_module_registry.json")
AUDIT_PATH = os.path.join(os.path.dirname(__file__), "santos_audit_log.json")
KNOWLEDGE_PATH = os.path.join(os.path.dirname(__file__), "santos_knowledge_corpus.json")


def load_registry():
    global MODULES
    if os.path.exists(REGISTRY_PATH):
        try:
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                MODULES = data
        except Exception:
            pass

    MODULES = auto_discover_modules()
    save_registry()
    log_event("load_registry", {"module_count": len(MODULES), "modules": MODULES})
    return MODULES


def auto_discover_modules(search_dirs=None):
    discovered = set(MODULES)
    base = os.path.dirname(__file__)
    if search_dirs is None:
        search_dirs = [base, os.path.join(base, "plugins")]

    for directory in search_dirs:
        if not os.path.isdir(directory):
            continue
        try:
            for entry in os.listdir(directory):
                if entry.endswith(('.logic', '.spec', '.config')):
                    discovered.add(entry)
        except Exception:
            continue

    return sorted(list(discovered))


def load_knowledge_corpus():
    default_corpus = [
        {
            "title": "Santos Protocol Design Principles",
            "source": "internal",
            "content": "Santos Protocol uses dependency graphs, health status, adaptive middleware and stability enforcement.",
            "tags": ["protocol", "stability", "middleware"]
        },
        {
            "title": "Open Source Alignment",
            "source": "open-source",
            "content": "Use creative commons GPL/BSD/MIT data and transform with relevance weighting into module actions.",
            "tags": ["open source", "weighting", "data"]
        },
        {
            "title": "Current events general guidance",
            "source": "external",
            "content": "For current real-world example mapping, fetch live feeds from worldwide APIs and map to matching query keywords.",
            "tags": ["current events", "real world"]
        },
    ]
    if os.path.exists(KNOWLEDGE_PATH):
        try:
            with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list) and data:
                return data
        except Exception:
            pass

    try:
        with open(KNOWLEDGE_PATH, "w", encoding="utf-8") as f:
            json.dump(default_corpus, f, indent=2)
    except Exception:
        pass
    return default_corpus


def get_global_knowledge(query, top_n=3):
    q = str(query or "").lower().strip()
    if not q:
        return []

    corpus = load_knowledge_corpus()
    scan = []

    # Add module docs
    for module_name in MODULES:
        content = load_module(module_name)
        if not content:
            continue
        scan.append({
            "title": module_name,
            "source": "module",
            "content": content,
            "tags": [],
        })

    scan.extend(corpus)

    def relevance(entry):
        text = " ".join([str(entry.get('title', '')), str(entry.get('content', '')), " ".join(entry.get('tags', []))]).lower()
        score = sum(text.count(tok) for tok in q.split())
        return score + (5 if any(tok in text for tok in q.split()) else 0)

    scored = sorted(scan, key=relevance, reverse=True)
    result = []
    for item in scored[:top_n]:
        result.append({
            "title": item.get("title"),
            "source": item.get("source"),
            "snippet": item.get("content", "")[:260],
            "relevance": relevance(item),
        })

    log_event("knowledge_query", {"query": query, "results": [r['title'] for r in result]})
    return result
    base = os.path.dirname(__file__)
    if search_dirs is None:
        search_dirs = [base, os.path.join(base, "plugins")]

    for directory in search_dirs:
        if not os.path.isdir(directory):
            continue
        try:
            for entry in os.listdir(directory):
                if entry.endswith(('.logic', '.spec', '.config')):
                    discovered.add(entry)
        except Exception:
            continue

    return sorted(discovered)


def log_event(action, details=None):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "action": action,
        "details": details or {},
    }
    try:
        audit_entries = []
        if os.path.exists(AUDIT_PATH):
            with open(AUDIT_PATH, "r", encoding="utf-8") as f:
                audit_entries = json.load(f)
        audit_entries.append(entry)
        with open(AUDIT_PATH, "w", encoding="utf-8") as f:
            json.dump(audit_entries, f, indent=2)
    except Exception:
        pass
    return entry


def load_audit():
    if not os.path.exists(AUDIT_PATH):
        return []
    try:
        with open(AUDIT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_registry():
    try:
        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            json.dump(MODULES, f, indent=2)
    except Exception:
        pass


def load_module(module_name):
    path = os.path.join(os.path.dirname(__file__), module_name)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def parse_block(data):
    result = {}
    stripped = data.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        try:
            js = json.loads(stripped)
            for k, v in js.items():
                result[str(k).strip().upper()] = str(v).strip()
            return result
        except Exception:
            pass

    for line in data.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            key_clean = key.strip().strip("[]").upper()
            value_clean = value.strip().strip("[]")
            result[key_clean] = value_clean
    return result


def resolve_dependencies(modules):
    order = []
    seen = set()

    def visit(name):
        if name in seen:
            return
        seen.add(name)
        module_data = load_module(name)
        if not module_data:
            return
        parsed = parse_block(module_data)
        dep_str = parsed.get("DEPENDENCIES", "")
        for dep in [d.strip() for d in dep_str.split(",") if d.strip()]:
            dep_file = f"{dep}.logic" if not dep.endswith(('.logic', '.spec', '.config')) else dep
            if dep_file not in seen:
                visit(dep_file)
        order.append(name)

    for m in modules:
        visit(m)
    return order


def collect_status():
    resolved = resolve_dependencies(MODULES)
    modules = []

    for m in resolved:
        data = load_module(m)
        if data is None:
            modules.append({
                "module": m,
                "status": "MISSING",
                "version": "n/a",
                "dependencies": [],
            })
            continue

        parsed = parse_block(data)
        status = parsed.get("STATUS", "UNKNOWN")
        version = parsed.get("VERSION", "n/a")
        deps = [d.strip() for d in parsed.get("DEPENDENCIES", "").split(",") if d.strip()]

        modules.append({
            "module": m,
            "status": status,
            "version": version,
            "dependencies": deps,
        })

    return {
        "module_order": resolved,
        "modules": modules,
    }


def create_module(module_name, status="OPERATIONAL", version="1.0", dependencies=None, keys=None):
    if dependencies is None:
        dependencies = []
    if keys is None:
        keys = {}

    if not module_name.endswith(('.logic', '.spec', '.config')):
        module_filename = f"{module_name}.logic"
    else:
        module_filename = module_name

    path = os.path.join(os.path.dirname(__file__), module_filename)
    if os.path.exists(path):
        raise FileExistsError(f"Module file already exists: {module_filename}")

    lines = [f"[MODULE: {module_name.replace('.logic','').replace('.spec','').replace('.config','').upper()}]", f"[STATUS: {status}]", f"[VERSION: {version}]"]
    if dependencies:
        lines.append(f"[DEPENDENCIES: {', '.join(dependencies)}]")
    for k, v in keys.items():
        lines.append(f"[{k.upper()}: {v}]")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    if module_filename not in MODULES:
        MODULES.append(module_filename)
        save_registry()

    log_event("create_module", {
        "module": module_filename,
        "status": status,
        "version": version,
        "dependencies": dependencies,
        "keys": keys,
    })

    return module_filename


def reload_modules():
    load_registry()
    status = collect_status()
    log_event("reload_modules", {"module_count": len(status.get('modules', [])), "status": status})
    return status


def report():
    load_registry()
    summary = collect_status()
    print("Santos Protocol Module Manager")
    print("===============================")
    print(f"Module load order: {summary['module_order']}")

    for m in summary["modules"]:
        print(f"- {m['module']}: STATUS={m['status']} VERSION={m['version']}")


if __name__ == "__main__":
    report()
