"""Bug 4: the length header counted characters instead of bytes, send() could
send part of a packet, and recv() could return part of one."""
import socket

import pytest

from chatutils.chatio2 import ChatIO, HEADER_LEN


class TrickleSock:
    """Hands back at most `step` bytes per recv, like a busy network."""

    def __init__(self, data: bytes, step: int = 3):
        self.data = data
        self.step = step

    def recv(self, n):
        n = min(n, self.step)
        chunk, self.data = self.data[:n], self.data[n:]
        return chunk


class LazySendSock:
    """send() only takes one byte at a time. sendall() takes everything."""

    def __init__(self):
        self.sent = b""

    def send(self, data):
        self.sent += data[:1]
        return 1

    def sendall(self, data):
        self.sent += data


@pytest.fixture
def pair():
    a, b = socket.socketpair()
    a.settimeout(5)
    b.settimeout(5)
    yield a, b
    a.close()
    b.close()


def test_header_counts_bytes_not_characters():
    packet = ChatIO().pack_data("M", "éééé")
    header = packet[1:1 + HEADER_LEN]
    assert int(header) == len("éééé".encode()) == 8
    assert packet[1 + HEADER_LEN:] == "éééé".encode()


def test_non_ascii_round_trip_over_socketpair(pair):
    a, b = pair
    ChatIO().pack_n_send(a, "M", "éééé")
    ChatIO().pack_n_send(a, "M", "next one 👋")

    assert b.recv(1) == b"M"
    assert ChatIO.unpack_data(b) == "éééé".encode()
    assert b.recv(1) == b"M"
    assert ChatIO.unpack_data(b) == "next one 👋".encode()


def test_bytes_payload_round_trip(pair):
    a, b = pair
    ChatIO().pack_n_send(a, "D", '{"nick": "zoë"}'.encode())
    assert b.recv(1) == b"D"
    assert ChatIO.unpack_data(b) == '{"nick": "zoë"}'.encode()


def test_unpack_waits_for_the_whole_message():
    body = "x" * 50 + "é" * 20
    packet = ChatIO().pack_data("M", body)
    sock = TrickleSock(packet[1:])
    assert ChatIO.unpack_data(sock) == body.encode()


def test_pack_n_send_sends_everything():
    sock = LazySendSock()
    ChatIO().pack_n_send(sock, "M", "hello there")
    assert sock.sent == ChatIO().pack_data("M", "hello there")
