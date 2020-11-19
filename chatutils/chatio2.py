import json
import socket
from types import ModuleType
from chatutils import utils
from chatutils.channel2 import Chime
import config.filepaths as paths

configs = utils.JSONLoader()
prefixes = utils.JSONLoader(paths.prefix_path)
users = utils.JSONLoader(paths.user_dict_path)

PREFIX_LEN = configs.dict["system"]["prefixLen"]
HEADER_LEN = configs.dict["system"]["headerLen"]
BUFFER_LEN = configs.dict["system"]["bufferLen"]


class ChatIO:
    
    def __init__(self):
        pass

    def pack_n_send(self, sock: socket, typ_pfx: str, data: str) -> None:
        """Convenience function, packs data and sends data."""
        outgoing_data = self.pack_data(typ_pfx, data)
        sock.send(outgoing_data)

    def pack_data(self, typ_pfx: str, data: str) -> bytes:
        """
        Example packet:
        """
        try:
            data = data.decode()
        except:
            pass

        size = len(data)

        utils.debug_(size, "size", "pack_n_send")
        header = self._make_header(size)

        packed_data = f"{typ_pfx}{header}{data}"
        return packed_data.encode()

    def _make_header(self, size: int, header_len: int = HEADER_LEN):
        header = f'{size:<{header_len}}'
        return header

    def recv_n_unpack(self, sock: socket, shed_pfx: bool = False) -> bytes:
        """Unpacks data from packed message, returns data without header."""
        if shed_pfx:
            # Dump prefix bytes into the ether.
            sock.recv(PREFIX_LEN)
        data = self.unpack_data(sock)
        return data

    def recv_n_dispatch(self, sock: socket, cmd_module: ModuleType) -> bytes:
        """Gets type and dispatches to proper command module"""
        msg_type = sock.recv(PREFIX_LEN)
        bytes_data = self.dispatch(sock, msg_type, cmd_module)
        return bytes_data

    @staticmethod
    def recv_open(sock: socket):
        while True:
            response = b""
            recv_len = 1

            while recv_len:
                data = sock.recv(BUFFER_LEN)
                recv_len = len(data)
                response += data

                if recv_len < BUFFER_LEN:
                    break

                if not data:
                    break

            print(response.decode())

    def dispatch(self, sock: socket, msg_type: str,
                 cmd_module: ModuleType) -> bytes:
        """Sorts through incoming data by prefix."""
        assert type(msg_type) == bytes, "Convert prefix to str"
        func = cmd_module.dispatch.get(msg_type.decode(), cmd_module.error)
        bytes_data = func(sock=sock, msg_type=msg_type)

        return bytes_data

    @classmethod
    def unpack_data(cls, sock: socket) -> bytes:
        """RETURNS MSG"""
        msg_len = sock.recv(HEADER_LEN)
        try:
            msg_bytes = sock.recv(int(msg_len))
        except:
            msg_bytes = ""

        # msg = msg.rstrip()
        return msg_bytes

    @staticmethod
    def make_buffer(sockets_dict: dict, user_dict: dict,
                    msg_type: bytes, msg_bytes:str="") -> dict:

        return {
            'sender_nick': user_dict['nick'],
            'sockets'    : sockets_dict,
            'msg_type'   : msg_type,
            'msg_bytes'  : msg_bytes
        }

    def make_new_line_dict(self, msg_bytes, sender_nick) -> bytes:
        """SERVERSIDE: MAKE DICT FROM '/n' MESSAGE WITH SENDER + CIPHER TYPE ATTACHED.
        TODO: Could handle on sender side?
        """
        send_buffer = {}
        temp = {}
        # msg_bytes = msg_bytes.decode()
        send_buffer["cipher"] = "goober"
        temp["cipher_text"] = msg_bytes
        send_buffer["msg_pack"] = temp
        send_buffer["sender"] = sender_nick
        send_buffer = json.dumps(send_buffer)
        return send_buffer

    def add_sender_nick(self, msg_bytes, sender_nick):
        """SERVERSIDE: ADD SENDER NICK."""
        msg_bytes = json.loads(msg_bytes)
        msg_bytes["sender"] = sender_nick
        msg_bytes = json.dumps(msg_bytes)
        return msg_bytes.encode()

    def make_broadcast_dict(self, buffer: dict) -> bytes:
        """SERVERSIDE: PREP MSG FOR BROADCAST"""
        sender_nick = buffer["sender_nick"]
        msg_bytes = buffer["msg_bytes"]

        if msg_bytes == "" or msg_bytes == "\n":
            msg_bytes = self.make_new_line_dict(msg_bytes, sender_nick)
        else:
            msg_bytes = self.add_sender_nick(msg_bytes, sender_nick)
        return msg_bytes


    def broadcast(self,
                  send_sock: socket,
                  buffer: dict,
                  pfx_name: str = "default",
                  target: str = "other",
                  sockets_dict: dict = None):

        """Broadcast messages to multiple users. Pass in buffer with list of 
        connected sockets and message bytes. Default pfx_name is "msg", but
        system messages from server should use "sysMsg".

        To send a buffer as a string literal and not a dict, provide
        sockets_dict a dict of sockets to broadcast to.
        
        target="all": sends to all connected users.
        target="self": sends to self from server.
        target="other": sends to everyone else.
        """

        if type(buffer) == str:
            # Makes valid buffer with string as input and socket_dict
            msg_bytes = buffer
            sockets = sockets_dict

        else:
            msg_bytes = buffer["msg_bytes"]
            sockets = buffer["sockets"]

        # print(buffer)
        try:
            msg_bytes = self.make_broadcast_dict(buffer)
        except:
            pass
        # print(msg_bytes)
        # try:
        #     print(msg_bytes.decode())
        # except:
        #     print(msg_bytes)

        if target == "other":
            for s in sockets.values():
                if s != send_sock:
                    try:
                        self.pack_n_send(s, prefixes.dict["server"]["chat"][pfx_name],
                                        msg_bytes)
                    except:
                        continue

        elif target == "all":
            for s in sockets.values():
                try:
                    self.pack_n_send(s, prefixes.dict["server"]["chat"][pfx_name],
                                    msg_bytes)
                except:
                    continue

        elif target == "self":
            for s in sockets.values():
                if s == send_sock:
                    try:
                        self.pack_n_send(s, prefixes.dict["server"]["chat"][pfx_name],
                                        msg_bytes)
                    except:
                        continue
        else:
            raise Exception("Valid options for broadcast are 'self', 'other', or 'all'.")



    def print_to_client(self, sender: str, msg: str, muted:bool = False):
        Chime.play_chime()
        print(f'\033[1;33;48m@{sender}\033[1;37;0m: {msg}')
