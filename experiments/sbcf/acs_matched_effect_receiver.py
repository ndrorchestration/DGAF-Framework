"""External receipt sink for the ACS matched-effect candidate workflow."""

from __future__ import annotations

import hashlib
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

_RECEIPT_PATH = Path(os.environ["SBCF_RECEIPT_FILE"])
_PORT_PATH = Path(os.environ["SBCF_RECEIVER_PORT_FILE"])


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _record(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length else b""
        host_header = self.headers.get("Host", "")
        host, separator, port_text = host_header.partition(":")
        if separator != ":" or not port_text.isdigit():
            self.send_error(400, "explicit numeric Host port required")
            return
        record = {
            "trial_id": self.headers.get("X-SBCF-Trial-ID"),
            "method": self.command,
            "scheme": "http",
            "host": host,
            "port": int(port_text),
            "path": self.path,
            "body_sha256": hashlib.sha256(body).hexdigest(),
        }
        with _RECEIPT_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
        self.send_response(204)
        self.send_header("Content-Length", "0")
        self.send_header("Connection", "close")
        self.end_headers()

    do_GET = _record
    do_POST = _record

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    _PORT_PATH.write_text(str(server.server_port), encoding="ascii")
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
