"""Known bypass counterexample for the bounded loopback reference PEP."""

import threading
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest


class RecordingHandler(BaseHTTPRequestHandler):
    def log_message(self, _format, *_args):
        return

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        self.server.events.append(("POST", self.path, body))  # type: ignore[attr-defined]
        self.send_response(204)
        self.end_headers()


@pytest.mark.xfail(
    strict=True,
    reason=(
        "The bounded DGAF/SBCF application PEP is not an OS socket interceptor; "
        "same-process code can bypass it by opening a direct connection"
    ),
)
def test_direct_socket_cannot_bypass_reference_pep():
    server = ThreadingHTTPServer(("127.0.0.1", 0), RecordingHandler)
    server.events = []  # type: ignore[attr-defined]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        connection = HTTPConnection("127.0.0.1", server.server_port, timeout=2)
        try:
            connection.request("POST", "/effect", body=b"direct-bypass")
            response = connection.getresponse()
            response.read()
            assert response.status == 204
        finally:
            connection.close()

        assert server.events == []  # type: ignore[attr-defined]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
