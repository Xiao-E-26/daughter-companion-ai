from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from runtime.first_connection import FirstConnectionManager, FirstConnectionRequest


ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"


class Handler(BaseHTTPRequestHandler):
    manager = FirstConnectionManager()

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path not in {"/", "/index.html"}:
            self.send_error(404)
            return
        body = INDEX.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/first-connection":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            transcript = str(payload.get("transcript", ""))
        except Exception:
            self._send_json(400, {"connected": False, "reason": "invalid_request"})
            return

        result = self.manager.connect(
            FirstConnectionRequest(
                user_id="cao-yuchen",
                transcript=transcript,
                runtime_identity="daughter",
                guardian_state="verified_for_first_connection",
                voice_enrollment_status="pending_voice_backend",
            )
        )

        response = {
            "connected": result.connected,
            "response_text": result.response_text,
            "reason": result.reason,
            "record": result.record.__dict__ if result.record else None,
        }
        self._send_json(200 if result.connected else 400, response)


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("Daughter First Connection: http://127.0.0.1:8765")
    server.serve_forever()


if __name__ == "__main__":
    main()
