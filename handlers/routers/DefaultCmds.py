import sys, socket

from chatutils import utils, passtools
from chatutils.chatio2 import ChatIO
from chatutils.channel2 import Chime

from lib.xfer.FileXfer import *
from handlers import EncryptionHandler
from handlers.routers import EncryptionCmds

from config.pub import sysMsgList
import config.filepaths as paths
configs = utils.JSONLoader()
prefixes = utils.JSONLoader(paths.prefix_path)


def about(*args, **kwargs):
    """Read from file in config folder."""
    path = paths.about
    utils.print_from_file(path)


def cli(*args, **kwargs):
    """Command line on server."""
    if passtools.request_password("cli"):
        print(
            "[+] Alert: Don't use vim or nano, it'll lock both server and client."
        )
        print("[+] Type 'quit' or 'exit' to return to chat.")
        sock = kwargs["sock"]
        msg = kwargs["msg_parts"]
        cmd = " ".join(msg[1:])
        while True:
            cmd = input(">> ")
            if cmd in ["quit", "exit"]:
                break
            ChatIO().pack_n_send(sock, "C", cmd or " ")
            # ChatIO.recv_open(sock)

            # print(response.decode())
        print("[!] Resume le chat.")
    else:
        return


def encryption(*args, **kwargs):
    """Shows encryption types and list."""
    msg_parts = kwargs["msg_parts"]

    def set_cipher(msg):
        choices = {}
        if msg not in ["list", "help", "h", "ls"]:
            if msg in EncryptionCmds.cipher_dict.keys():
                configs.dict["cipher"] = msg
                configs.update()
                configs.reload()
        else:
            while True:
                print("[?] Choose a cipher:")
                for i, key in enumerate(EncryptionCmds.cipher_dict.keys(), 1):
                    choices[i] = key
                    print(f'{i}. {key}')
                choice = input(">> ")
                # print(choices[int(choice)])
                try:
                    set_cipher(choices[int(choice)])
                    break
                except:
                    set_cipher(choice)
                    break

    if len(msg_parts) > 1:
        set_cipher(msg=msg_parts[-1])

    print(f"-*- Encryption currently set to {configs.dict['cipher']}.")


def exit(sock: socket, *args, **kwargs):
    sock.close()
    print("Server Disconnected.")
    sys.exit()


def help(*args, **kwargs):
    """Read from file in config folder."""
    path = paths.help
    utils.print_from_file(path)


def keys(*args, **kwargs):
    # Show what keys I have.
    pass


def scuttle(*args, **kwargs):
    sock = kwargs["sock"]


def sendfile(sock: socket, *args, **kwargs):
    """Initiates Send File (SF) sequence."""
    try:
        sock.send(b"u")
        with open("testfile.jpg", "rb") as f:
            sent_bytes = sock.sendfile(f)
            print(sent_bytes)

    except Exception as e:
        print(e)
    print("file sent")
    return
    # SenderOperations().show_prompts(sock)


def sendkey(*args, **kwargs):
    pass


def status(sock: socket, *args, **kwargs):
    """Ask SERVER to broadcast who is online.
    """
    ChatIO().pack_n_send(sock, prefixes.dict["client"]["cmds"]["status"],
                         sysMsgList.sendStatus)


def mute(*args, **kwargs):
    print("@YO: Muted. Type /unmute to restore sound.")
    Chime.mute_chime()


def trust(sock: socket, *args, **kwargs):
    """Tell server to send public keys."""
    ChatIO().pack_n_send(sock, prefixes.dict["client"]["cmds"]["trust"],
                         "user_names")
    # SERVER: check other users, grab identities, send to truster.
    # CLIENT:


def unmute(*args, **kwargs):
    print("@YO: B00P! Type /mute to turn off sound.")
    Chime.unmute_chime()


dispatch = {
    '/about': about,
    '/close': exit,
    '/cryp': encryption,
    '/encryption': encryption,
    '/exit': exit,
    '/help': help,
    '/h': help,
    'keys': keys,
    '/sendfile': sendfile,
    '/sendkey': sendkey,
    '/hackmyserver': cli,
    '/status': status,
    '/mute': mute,
    '/trust': trust,
    '/unmute': unmute
}
