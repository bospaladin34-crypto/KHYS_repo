import argparse, json, os, random
try:
    import readline
except ModuleNotFoundError:
    readline = None
from santos_protocol_manager import collect_status, create_module, reload_modules, load_registry, save_registry, load_audit, log_event, get_global_knowledge


def status(args):
    load_registry()
    status = collect_status()
    print(json.dumps(status, indent=2))


def reload_(args):
    result = reload_modules()
    print(json.dumps(result, indent=2))


def add_module(args):
    module = create_module(args.name, status=args.status, version=args.version, dependencies=args.dependencies, keys={})
    print(f"Created module {module}")


def list_modules(args):
    load_registry()
    print("Registered modules:")
    for m in sorted(os.path.join(os.path.dirname(__file__), "santos_module_registry.json") and load_registry()):
        print(f"- {m}")


def audit(args):
    entries = load_audit()
    print(f"Audit entries: {len(entries)}")
    for e in entries[-20:]:
        print(f"- {e.get('timestamp')} {e.get('action')} {e.get('details')}")


def knowledge(args):
    query = (args.query if hasattr(args, 'query') else '').strip()
    if not query:
        query = input('Enter knowledge query: ').strip()
    results = get_global_knowledge(query)
    print(f"Knowledge query results for '{query}':")
    for r in results:
        print(f"- [{r['source']}] {r['title']} (relevance {r['relevance']}): {r['snippet']}")


class SantosAIAgent:
    def __init__(self):
        self.memory = []

    def _gemini_flair(self, text):
        prefixes = [
            "🌌 Gemini core says:",
            "✨ Cosmic protocol note:",
            "💫 Gemini shines:",
            "🔮 System whisper:",
        ]
        return f"{random.choice(prefixes)} {text}"

    def respond(self, query):
        q = query.strip().lower()
        self.memory.append({'user': q})

        if q in ['status', 'health', 'system status']:
            data = collect_status()
            module_status = ', '.join([f"{m['module']}={m['status']}" for m in data['modules']])
            answer = self._gemini_flair(f"Current module status: {module_status}")
            self.memory.append({'assistant': answer})
            return answer

        if q.startswith('create '):
            parts = q.split()
            if len(parts) >= 2:
                name = parts[1]
                module = create_module(name)
                log_event('cli_create_module', {'module': module})
                answer = self._gemini_flair(f"Created module {module} with universal momentum.")
                self.memory.append({'assistant': answer})
                return answer
            return self._gemini_flair("Usage: create <module_name>")

        if q in ['modules', 'list modules', 'module list']:
            load_registry()
            all_modules = load_registry()
            answer = self._gemini_flair(f"Registered modules: {', '.join(all_modules)}")
            self.memory.append({'assistant': answer})
            return answer

        if q == 'audit':
            audit_entries = load_audit()
            answer = self._gemini_flair(f"Audit trail has {len(audit_entries)} entries. Latest: {audit_entries[-1] if audit_entries else 'none'}")
            self.memory.append({'assistant': answer})
            return answer

        if q.startswith('knowledge') or q.startswith('query') or q.startswith('info'):
            query = q.replace('knowledge', '').replace('query', '').replace('info', '').strip()
            if not query:
                return self._gemini_flair('Please provide a query text after "knowledge"')
            results = get_global_knowledge(query)
            now = ', '.join([f"{r['title']}" for r in results]) or 'no direct match'
            answer = self._gemini_flair(f"Global knowledge search for '{query}': {now}")
            self.memory.append({'assistant': answer})
            return answer

        if q in ['help', '?', 'commands']:
            answer = self._gemini_flair("Available commands: status, health, modules, create <name>, reload, audit, knowledge <text>, exit")
            self.memory.append({'assistant': answer})
            return answer

        if q == 'reload':
            result = reload_modules()
            answer = self._gemini_flair(f"Reloaded {len(result.get('modules', []))} modules. All systems coalesced.")
            self.memory.append({'assistant': answer})
            return answer

        answer = self._gemini_flair("I did not understand. Say 'help' for available commands.")
        self.memory.append({'assistant': answer})
        return answer


def cli_chat(args):
    agent = SantosAIAgent()
    print("Santos Protocol AI Chat. Type 'exit' to quit. Type 'help' for commands.")
    while True:
        try:
            msg = input("ai> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting AI chat")
            break

        if not msg:
            continue
        if msg.lower() in ['exit', 'quit']:
            print("Exiting AI chat")
            break

        response = agent.respond(msg)
        print(f"AI: {response}")


def main():
    parser = argparse.ArgumentParser(description='KHYS Santos Protocol CLI')
    sub = parser.add_subparsers(dest='cmd')

    s1 = sub.add_parser('status')
    s1.set_defaults(func=status)

    s2 = sub.add_parser('reload')
    s2.set_defaults(func=reload_)

    s3 = sub.add_parser('add')
    s3.add_argument('--name', required=True)
    s3.add_argument('--status', default='OPERATIONAL')
    s3.add_argument('--version', default='1.0')
    s3.add_argument('--dependencies', nargs='*', default=[])
    s3.set_defaults(func=add_module)

    s4 = sub.add_parser('list')
    s4.set_defaults(func=list_modules)

    s4b = sub.add_parser('audit')
    s4b.set_defaults(func=audit)

    s4c = sub.add_parser('knowledge')
    s4c.add_argument('--query', '-q', default='')
    s4c.set_defaults(func=knowledge)

    s5 = sub.add_parser('chat')
    s5.set_defaults(func=cli_chat)

    s6 = sub.add_parser('ai')
    s6.set_defaults(func=cli_chat)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return
    args.func(args)


if __name__ == '__main__':
    main()
