from os import stat
import sys, socket
from chatutils import utils

configs = utils.JSONLoader()


def killit(sock: socket):
    sock.close()
    print("[x] Server Disconnected.")
    sys.exit()


class Chime:
    """Plays default sound in the channel."""

    # Ring my bell, ring my bell
    def __init__(self):
        self.muted = configs.dict["muted"]

    @staticmethod
    def play_chime():
        if not configs.dict["muted"]:
            sys.stdout.write("\a")
            sys.stdout.flush()

    @staticmethod
    def unmute_chime():
        configs.dict["muted"] = False
        configs.update()

    @staticmethod
    def mute_chime():
        configs.dict["muted"] = True
        configs.update()