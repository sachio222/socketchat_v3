"""Bug 3: any client that sent a "C" message got a shell on the server. The
password check only ran on the client."""
import socket
import subprocess

import pytest

from chatutils.chatio2 import ChatIO
from handlers.routers import ServerCmds


@pytest.fixture
def shell_calls(monkeypatch):
    calls = []

    def fake_check_output(*args, **kwargs):
        calls.append(args)
        return b"pwned\n"

    monkeypatch.setattr(subprocess, "check_output", fake_check_output)
    return calls


@pytest.fixture
def pair():
    a, b = socket.socketpair()
    a.settimeout(5)
    b.settimeout(5)
    yield a, b
    a.close()
    b.close()


def send_cmd_to_server(client, server, command):
    ChatIO().pack_n_send(client, "C", command)
    msg_type = server.recv(1)
    assert msg_type == b"C"
    buffer = ChatIO.make_buffer({"mallory": server}, {"nick": "mallory"},
                                msg_type)
    ServerCmds.dispatch["C"](sock=server, buffer=buffer)


def test_server_refuses_remote_shell_by_default(pair, shell_calls):
    client, server = pair
    send_cmd_to_server(client, server, "touch pwned")

    assert shell_calls == []
    assert client.recv(1) == b"s"
    assert b"Remote shell is off" in ChatIO.unpack_data(client)


def test_refused_command_keeps_stream_in_sync(pair, shell_calls):
    client, server = pair
    send_cmd_to_server(client, server, "touch pwned")
    client.recv(1)
    ChatIO.unpack_data(client)

    ChatIO().pack_n_send(client, "M", "still here")
    assert server.recv(1) == b"M"
    assert ChatIO.unpack_data(server) == b"still here"


def test_server_runs_remote_shell_when_opted_in(pair, shell_calls,
                                                monkeypatch):
    monkeypatch.setattr(ServerCmds, "allow_remote_shell", True)
    client, server = pair
    send_cmd_to_server(client, server, "echo hi")

    assert len(shell_calls) == 1


def test_server_flag_is_off_unless_asked_for():
    import server
    assert server.parse_args([]).allow_remote_shell is False
    assert server.parse_args(["--allow-remote-shell"]).allow_remote_shell
