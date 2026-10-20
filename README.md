#### secure-cli-socketchat-python-v1
# Secure CLI Socket Chat (BETA)
### Street name: Encryptochat / Cryptochat
======

You don't need messenger. **Secure CLI Socket Chat** 

## Features:
* Secure, client-side, end to end encryption/decryption
* Uses Diffie Hellman Key Exchange with pynacl.
* Supports XChaCha20-poly1305, aes256, Fernet (aes128) message encryption.
* Use it on your own LAN to chat between computers, or across the world with friends.
* Direct message or multiple chat-client connections.
* Secure chat: Encrypt your traffic using assymetric key encryption.
* Tiny filesize and runs in terminal.
* Monitor unencrypted chats on your server.
* Supports Addons and features added continually.

[![Flattr this git repo](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=diamondhawk&url=https://github.com/sachio222/socketchat_v1)

## Install

Needs Python 3.10 or newer. Tested on Python 3.14 on macOS.

```
git clone https://github.com/sachio222/socketchat_v3.git
cd socketchat_v3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Start the server

```
python server.py
```

The server listens on 127.0.0.1, port 12222. To chat across your LAN or the internet, change `defaultHost` and `defaultPort` in `config/configDefaults.json` before the first run, or in `config/config.json` after it. The first run copies the defaults into `config/config.json`.

### Start two clients

Each client keeps its config and keys in its own folder, so run each one from its own clone. To try it on one machine, clone the repo a second time and set up a venv there too. Then in each folder run:

```
python client.py
```

Pick a name when asked. Type a message and press enter to send it.

### Encrypted chat

1. Both clients connect.
2. One client types `/trust`. The two clients swap public keys, then the symmetric keys travel inside an encrypted NaCl box. The other client prints `Symmetric keys unpacked.`
3. Pick a cipher, for example `/cryp chacha`. Messages from that client are now encrypted with XChaCha20-Poly1305, and the server only sees ciphertext.

`/cryp ls` lists the ciphers. `goober` means no encryption.

### Remote shell is off

`/hackmyserver` lets a client run shell commands on the server. The server refuses those commands unless you start it with:

```
python server.py --allow-remote-shell
```

With that flag on, anyone who can connect can run commands on the server machine, so only use it on a network you trust. The client also asks you to set a local password the first time you use `/hackmyserver`. It is stored as a hash in `config/prv/keys/hashes.json`, which git ignores.

### Math facts

`/mathfacts` calls the Numbers API on RapidAPI. Get a key at rapidapi.com and set it before you start the client:

```
export RAPIDAPI_KEY=your-key-here
```

### Tests

```
pip install pytest
python -m pytest tests
```

## Commands

```/trust``` Exchange keys (Currently only works with all clients, single client trust coming soon)

```/help``` Shows commands, and addons

```/about```

```/mute```

```/unmute```

```/encryption``` or ```/cryp``` Displays current encryption.

```/encryption list``` or ```/cryp ls``` Shows available encryption methods

```/status``` Shows who's in the room at the moment. 

```/boot <name>``` Kicks a user from the room.

```/hackmyserver``` Shell on the server. Off unless the server runs with ```--allow-remote-shell```.

```ping``` IN PROGRESS. Sends a ping request to the server.

```/exit``` Quits the client. 

```/sendfile``` IN PROGRESS. Sends file (currently unencrypted) to selected user.

## Current Addons

```/wikipedia``` or ```/wp``` Wikipedia

```/map``` Open street maps

```/urband``` Urban Dictionary

```/moon``` Current Phase of the moon

```/weather``` Weather near you

```/mathfacts``` Trivia about a number. Needs ```RAPIDAPI_KEY```.

```/epic``` splices together latest Earth rotation sequence from the Earth Polychromatic Imaging Camera

## Contributors
J. Krajewski
M. Holcombe


## License 
* see [LICENSE](https://github.com/username/sw-name/blob/master/LICENSE.md) file

## Version 
* Version 1.1

## Troubleshooting
Currently tested on MacOSX and Linux. 

Error:
```socket.gaierror: [Errno 8] nodename nor servname provided, or not known```

System: Mac

Solution: [Enable Sharing Permissions, then Disable](https://stackoverflow.com/a/53382881/5369711)

## Contact
#### Developer/Company

* Twitter: [@jakekrajewski](https://twitter.com/jakekrajewski "@jakekrajewski")
* Medium: [@Jakekrajewski](https://medium.com/@Jakekrajewski)

