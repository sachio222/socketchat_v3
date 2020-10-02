import json
import socket
from types import ModuleType
from chatutils import utils
import config.filepaths as paths

configs = utils.JSONLoader()
prefixes = utils.JSONLoader(paths.prefix_path)
users = utils.JSONLoader(paths.user_dict_path)

HEADER_LEN = configs.dict["system"]["headerLen"]
PREFIX_LEN = configs.dict["system"]["prefixLen"]


class ChatIO:

    def __init__(self):
        pass

    def pack_n_send(self, sock: socket, typ_pfx: str, data: str) -> None:
        """Convenience function, packs data and sends data."""
        data = self.pack_data(typ_pfx, data)
        sock.send(data)

    def pack_data(self, typ_pfx: str, data: str) -> bytes:
        """
        Example packet:
            
        """
        try:
            data = data.decode()
        except:
            pass

        # data = data + "\n"
        size = len(data)
        header = self._make_header(size)
        packed_data = f"{typ_pfx}{header}{data}"
        return packed_data.encode()

    def _make_header(self, size: int, header_len: int = HEADER_LEN):
        header = f'{size:<{header_len}}'
        return header

    def recv_n_unpack(self, sock: socket, shed_pfx: bool = False) -> bytes:
        if shed_pfx:
            # Dump bytes into the ether.
            sock.recv(PREFIX_LEN)
        data = self.unpack_data(sock)
        return data

    def recv_n_dispatch(self, sock: socket, cmd_module: ModuleType) -> bytes:
        """Gets type and dispatches to proper command module"""
        msg_type = sock.recv(PREFIX_LEN)
        bytes_data = self.dispatch(sock, msg_type, cmd_module)
        return bytes_data

    def dispatch(self, sock: socket, msg_type: str,
                 cmd_module: ModuleType) -> bytes:
        """Sorts through incoming data by prefix."""
        assert type(msg_type) == bytes, "Convert prefix to str"
        func = cmd_module.dispatch.get(msg_type.decode(), cmd_module.error)
        bytes_data = func(sock=sock, msg_type=msg_type)

        return bytes_data

    @classmethod
    def unpack_data(cls, sock: socket) -> bytes:
        """UNPACK DATA"""
        msg_len = sock.recv(HEADER_LEN)
        try:
            msg = sock.recv(int(msg_len))
        except:
            msg = ""

        # msg = msg.rstrip()
        return msg

    def broadcast(self, send_sock: socket, client_list: dict, msg_bytes: bytes):
        for client in client_list:
            if client != send_sock:
                self.pack_n_send(client, prefixes.dict["server"]["chat"]["default"], msg_bytes)
