import sys
import json
from client import BPlusTreeEngine

def main():
    engine = BPlusTreeEngine()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "insert":
            engine.insert(params.get("key"), params.get("value"))
            res = {"status": "ok"}
        elif method == "search":
            val, latches = engine.search(params.get("key"))
            res = {"value": val, "latches": latches}
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
