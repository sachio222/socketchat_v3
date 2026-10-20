"""TLS on current Python.

The client built its context with Purpose.CLIENT_AUTH, which is a server-side
context since Python 3.10, so every connect failed with "Cannot create a
client socket with a PROTOCOL_TLS_SERVER context". And one bad handshake
killed the server's accept loop for good.
"""
import socket
import threading
import time

import pytest

import client
import server
from lib.encryption import x509


@pytest.fixture(scope="module", autouse=True)
def certs():
    x509.X509()


@pytest.fixture
def listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    s.listen(5)
    yield s
    s.close()


def tls_connect(addr):
    raw = socket.create_connection(addr, timeout=5)
    return client.make_ssl_context().wrap_socket(raw,
                                                 server_hostname=addr[0])


def test_client_and_server_contexts_shake_hands(listener):
    server_ctxt = server.make_ssl_context()
    accepted = {}

    def accept():
        conn, _ = listener.accept()
        accepted["sock"] = server_ctxt.wrap_socket(conn, server_side=True)

    t = threading.Thread(target=accept, daemon=True)
    t.start()

    sock = tls_connect(listener.getsockname())
    t.join(5)
    assert sock.version() is not None
    assert "sock" in accepted
    sock.close()
    accepted["sock"].close()


def test_accept_loop_survives_a_bad_handshake(listener, monkeypatch):
    seen = []
    monkeypatch.setattr(server, "handle_client", lambda s, a: seen.append(a))
    monkeypatch.setattr(server,
                        "server_ctxt",
                        server.make_ssl_context(),
                        raising=False)
    threading.Thread(target=server.accept_client,
                     args=(listener,),
                     daemon=True).start()

    # Connect and hang up without TLS, like a port scanner would.
    socket.create_connection(listener.getsockname(), timeout=5).close()
    time.sleep(0.2)

    sock = tls_connect(listener.getsockname())
    end = time.time() + 5
    while not seen and time.time() < end:
        time.sleep(0.05)
    sock.close()
    assert len(seen) == 1
