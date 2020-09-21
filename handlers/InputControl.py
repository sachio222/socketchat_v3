
import json
from pathlib2 import Path

from chatutils import utils
from handlers.routers import default, addons


def input_control_handler(sock, msg: str):

    # TODO: Move to module.
    """Sorts through input control messages and calls controller funcs.

    All of the controller commands are routed through this function based
    on the presence of a "/" character at the beginning of the command,
    which is detected by the sender function. Each command has a different
    end point and they all behave differently depending on their defined
    purposes.

    Args
        msg - (Usually str) - the raw input command before processing.
    """
    # Convert to string if needed. 
    if type(msg) == bytes:
        msg.decode()

    # Split msg into command and keywords
    msg_parts = msg.split(' ')

    # Check through default command dict.
    self_name = default
    func = self_name.Router().cmd_dict.get(msg_parts[0], False)

    if not func:
        # Check through addons command dict.
        self_name = addons
        func = self_name.Router().cmd_dict.get(msg_parts[0], False)
    
    if func:
        func(self_name.Router, msg_parts)

    else:
        print('-!- Not a valid command.')


    # if msg_parts[0] == '/about':
    #     # Read from file in config folder.
    #     path = 'config/about.txt'
    #     utils.print_from_file(path)
    # elif msg_parts[0] in ('/help', '/h'):
    #     # Read from file in config folder.
    #     path = 'config/help.txt'
    #     utils.print_from_file(path)
    # elif msg_parts[0] in ('/sendfile', '/sf'):
    #     # Initiates Send File (SF) sequence.
    #     self.start_sendfile_process(sock)
    # elif msg_parts[0] == '/status':
    #     # Ask SERVER to broadcast who is online.
    #     # join and strip. Send over full string.
    #     msg = ' '.join(msg_parts)
    #     msg = msg_parts[1:]
    #     self.pack_n_send(sock, '/', msg)
    # elif msg_parts[0] == '/mute':
    #     self.muted = True
    #     self.print_message("@YO: Muted. Type /unmute to restore sound.")
    # elif msg_parts[0] == '/unmute':
    #     self.muted = False
    #     self.print_message("@YO: B00P! Type /mute to turn off sound.")
    # elif msg_parts[0] == '/trust':
    #     self.trust(msg_parts)
    # elif msg_parts[0] == '/sendkey':
    #     self.sendkey(sock, msg_parts)
    # elif msg_parts[0] == '/exit' or msg_parts[0] == '/close':
    #     print('Disconnected.')
    #     sock.shutdown(socket.SHUT_RDWR)
    #     sock.close()
    #     pass
    # elif msg_parts[0] == '/weather':
    #     weather.report(msg)
    #     # print('\r-=-', report)
    # elif msg[0] == '/urband':
    #     urbandict.urbandict(msg)
    # elif msg[0] == '/moon':
    #     moon.phase()
    # elif msg[0] == '/mathtrivia':
    #     mathfacts.get_fact(msg)
    # elif msg[0] == '/map':
    #     map.open_map(msg)
    # elif msg[0] == '/epic':
    #     globe.animate()
    # elif msg[0] in ('/wikipedia', '/wp'):
    #     wikip.WikiArticle().run_from_cli(msg)
    # elif msg[0] == '/bloomberg':
        # bloomberg.Bloomberg().get_stories_about(msg)
    #     pass 


class ConfigJson():
    def __init__(self, json_path):
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)

    def save(self, json_path):
        with open(json_path, "w") as f:
            json.dump(self.__dict__, f, indent=4)

    def update(self, json_path):
        """Loads parameters from json file."""
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)

    @property
    def dict(self):
        """Gives dict-like access to Params instance by 'params.dict['learning_rate]."""
        return self.__dict__

# Initialize paths to json parameters
json_path = Path().absolute() / "config/config.json"
cfg = ConfigJson(json_path)
print(cfg)

# Load params json
assert json_path.is_file(
), f"\n\nERROR: No config.json file found at {json_path}\n"