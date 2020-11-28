from chatutils import channel2
import socket, sys
from chatutils import utils
from chatutils.chatio2 import ChatIO
from handlers import HandshakeHandler
from lib.cmd import cmd
from lib.key_xfer import key_xchange

from config.pub import sysMsgList
import config.filepaths as paths

configs = utils.JSONLoader()
prefixes = utils.JSONLoader(paths.prefix_path)

HEADER_LEN = configs.dict["system"]["headerLen"]
BUFFER_LEN = configs.dict["system"]["bufferLen"]

def _b_handler(sock: socket, buffer: dict, *args, **kwargs):
    """Boot user."""
    bootee = ChatIO.unpack_data(sock).decode()

    if bootee in buffer["sockets"]:

        for nick in buffer["sockets"]:
            if nick == bootee:
                # Bootee sock matches Booter sock.
                if buffer["sockets"][nick] == sock:
                    # Booter can't boot self.
                    ChatIO().pack_n_send(sock,
                                prefixes.dict["server"]["chat"]["sysMsg"],
                                sysMsgList.bootSelf)
                else:
                    # Booter is not self.
                    print(f'[!] {bootee} has been kicked.')
                    ChatIO().pack_n_send(sock,
                                prefixes.dict["server"]["chat"]["sysMsg"],
                                f"{sysMsgList.bootSuccess} {bootee}")
                    
                    ChatIO().pack_n_send(buffer["sockets"][nick],
                                prefixes.dict["server"]["chat"]["sysMsg"],
                                sysMsgList.bootMsg)
                    
                    buffer["sockets"][nick].close()
                    # sys.exit()
                    # utils.delete_user(bootee)
                    return
            else:
                continue

            break
                    
    else:
        ChatIO().pack_n_send(sock,
                        prefixes.dict["server"]["chat"]["sysMsg"],
                        sysMsgList.bootUserNotFound)          


def _i_handler(sock: socket, buffer: dict, *args, **kwargs):
    """Clear user from user_dict if no response."""

    users = utils.JSONLoader(paths.user_dict_path)
    utils.purge_users(users, buffer)

    # print("Boomin back atcha!")


def _l_handler(sock: socket, buffer: dict, *args, **kwargs):
    """RELAY LINE BREAK"""
    bytes_data = ChatIO.unpack_data(sock)
    print(bytes_data)
    # print(buffer)
    ChatIO().broadcast(sock, buffer, pfx_name="newLine")
    return


def _n_handler(sock: socket, *args, **kwargs) -> bytes:
    "RETURNS NICK FROM CLIENT"
    msg_bytes = ChatIO.unpack_data(sock)
    return msg_bytes


def _u_handler(sock: socket, buffer: dict, *args, **kwargs):
    """RELAY UPLOAD DATA FROM SENDER TO RECIEVER"""

    print("[!] Relaying data.")
    sockets = buffer["sockets"]
    recv_len = 1

    sndr_sock = sock
    rcvr_sock = [s for s in sockets.values() if s != sndr_sock]
    try:
        rcvr_sock = rcvr_sock[0]

        rcvr_sock.send(prefixes.dict["server"]["chat"]["relayData"].encode())
    except:
        print("SENDFILE DEBUG: No recipient exists.")

    while recv_len:
        data = sndr_sock.recv(BUFFER_LEN)
        try:
            rcvr_sock.send(data)
        except:
            print(
                "ERROR: Recipient no longer exists. Make sure they're still connected."
            )

        recv_len = len(data)

        if recv_len < BUFFER_LEN:
            break

        if not data:
            break


def _s_handler(sock: socket, buffer: dict, *args, **kwargs):
    """SYSTEM MESSAGE HANDLER."""
    msg_bytes = buffer["msg_bytes"] = ChatIO.unpack_data(sock)
    print("System message is:", msg_bytes)
    ChatIO().broadcast(sock, buffer, pfxName="sysMsg")


def _C_handler(sock: socket, *args, **kwargs):
    """COMMAND LINE CONTROL."""
    cmd.commands(sock)


def _D_handler(sock: socket, *args, **kwargs) -> bytes:
    """DATA FROM CLIENT."""
    bytes_data = ChatIO.unpack_data(sock)
    return bytes_data


def _H_handler(sock: socket, *args, **kwargs) -> bytes:
    """Receive handshake dict with user info."""
    bytes_data = ChatIO.unpack_data(sock)
    return bytes_data


def _K_handler(sock: socket, buffer: dict, *args, **kwargs):
    """Relays key_packet to trustee."""
    recip_socket = None
    sender_nick = buffer["sender_nick"]

    enc_key_pack = ChatIO.unpack_data(sock)

    # TODO: Add username
    for socket in buffer["sockets"].items():
        if socket[1] != sock:
            recip_socket = socket[1]

    ChatIO().pack_n_send(recip_socket,
                         prefixes.dict["client"]["cmds"]["trustKeys"],
                         enc_key_pack)


def _M_handler(sock: socket, buffer: dict, *args, **kwargs) -> bytes:
    """DEFAULT MESSAGE HANDLER."""
    msg_bytes = buffer["msg_bytes"] = ChatIO.unpack_data(sock)
    print(msg_bytes.decode())
    ChatIO().broadcast(sock, buffer)
    return msg_bytes


def _T_handler(sock: socket, buffer: dict, *args, **kwargs):
    """Sends key to client."""
    recip_socket = None
    sender_nick = buffer["sender_nick"]

    user = ChatIO.unpack_data(sock)
    # Get keys from user_dict
    # TODO: pass in recip name.
    pub_key_sender, pub_key_recip, ver_key_sender, ver_key_recip = key_xchange.get_keys(
        sender_nick)

    for socket in buffer["sockets"].items():
        if socket[1] != sock:
            recip_socket = socket[1]

    ChatIO().pack_n_send(sock, prefixes.dict["server"]["cmds"]["trustSndr"],
                         pub_key_recip)
    ChatIO().pack_n_send(recip_socket,
                         prefixes.dict["server"]["cmds"]["trustRcvr"],
                         pub_key_sender)


def _S_handler(sock: socket, buffer: dict, *args, **kwargs):
    """Status report."""
    users_online = []
    bytes_data = ChatIO.unpack_data(sock)
    print(bytes_data.decode())

    for k in buffer["sockets"].keys():
        users_online.append(k)

    status_msg = f'@Yo: {len(users_online)} online - {", ".join(users_online)}'
    buffer["msg_bytes"] = status_msg

    ChatIO().broadcast(sock, buffer, pfx_name="sysMsg", target="self")


def _X_handler(sock: socket, *args, **kwargs) -> bytes:
    """TRANSFER HANDLER"""
    pass


def _P_handler(sock: socket, *args, **kwargs):
    """ADD PUBLIC KEY"""
    pass


def error(*args, **kwargs):
    print(kwargs)
    # print(f'Message Type Error: Invalid message type {kwargs["msg_type"]}')


dispatch = {
    "a": None,
    "b": _b_handler,
    "c": None,
    "d": None,
    "e": None,
    "f": None,
    "g": None,
    "h": None,
    "i": _i_handler,
    "j": None,
    "k": None,
    "l": _l_handler,
    "m": None,
    "n": _n_handler,
    "o": None,
    "p": None,
    "q": None,
    "r": None,
    "s": _s_handler,
    "t": None,
    "u": _u_handler,
    "v": None,
    "w": None,
    "x": None,
    "y": None,
    "z": None,
    "A": None,
    "B": None,
    "C": _C_handler,
    "D": _D_handler,
    "E": None,
    "F": None,
    "G": None,
    "H": _H_handler,
    "I": None,
    "J": None,
    "K": _K_handler,
    "L": None,
    "M": _M_handler,
    "N": None,
    "O": None,
    "P": None,
    "Q": None,
    "R": None,
    "S": _S_handler,
    "T": _T_handler,
    "U": None,
    "V": None,
    "W": None,
    "X": None,
    "Y": None,
    "Z": None,
    "/": None
}
