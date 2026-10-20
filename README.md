# socketchat v3

A chat you run from the terminal. One person starts a small server, friends connect from their own machines, and messages can be encrypted with ChaCha20-Poly1305, a modern cipher that also catches tampering.

v3 is a rewrite of [socketchat v2](https://github.com/sachio222/socketchat_v2) from 2020: same idea, cleaner design and stronger encryption. It is still a learning project, so don't use it for anything you need to keep secret. "Before you rely on it" below lists where it falls short.

## New since v2

- **Encryption that catches tampering.** v2 used AES-256 in CBC mode with no tamper check. v3 adds ChaCha20-Poly1305, which rejects any message changed on the way.
- **Pick your cipher while you chat.** `/cryp chacha` switches ciphers, and `/cryp ls` lists the options.
- **A cleaner design.** v2 handles every message in one long chain of checks in `client.py`. In v3, each message type goes to its own handler module in `handlers/routers/`, so adding a command means adding a handler.
- **A config file.** Host, port and cipher live in `config/config.json`, which the first run creates from `config/configDefaults.json`.
- **Room tools.** `/boot <name>` removes someone from the room. `/hackmyserver` opens a shell on the server, off unless the server starts with `--allow-remote-shell`. Its local password is stored as an Argon2 hash, the current standard for storing passwords.
- **Accented letters work.** Message lengths count bytes, so "über" and emoji go through cleanly. v2 can break on them.
- **A sturdier server.** One bad connection no longer stops the server from accepting new people.

v2 still has two things v3 hasn't caught up on: `/trust` with one person rather than the whole room, and a complete `/sendfile` flow (unencrypted in v2).

## Install

You need Python 3.10 or newer. It was last tested on Python 3.14 on macOS.

```
git clone https://github.com/sachio222/socketchat_v3.git
cd socketchat_v3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run it

### Start the server

```
python server.py
```

The server listens on your own machine (127.0.0.1) at port 12222. To chat across your network or the internet, change `defaultHost` and `defaultPort` in `config/configDefaults.json` before the first run, or in `config/config.json` after it.

### Start two clients

Each client keeps its config and keys in its own folder, so run each one from its own clone. To try it on one machine, clone the repo a second time and set up a venv there too. Then in each folder:

```
python client.py
```

Pick a name when asked, type a message and press Enter.

## Encrypted chat

1. Both clients connect.
2. One client types `/trust`. The clients swap public keys, and the message keys travel inside a sealed NaCl box. The other client prints "Symmetric keys unpacked."
3. Type `/cryp chacha`. Your messages are now encrypted with ChaCha20-Poly1305, and the server sees only scrambled text.

`chacha` is the cipher tested end to end. `/cryp ls` also lists older options that are unfinished or untested, and `goober` turns encryption off.

## Before you rely on it

- **The server hands out public keys, and nothing checks them.** A dishonest server could swap in its own key and read everything.
- **Clients don't verify the server's certificate.** The client loads it but accepts any server.
- **`/trust` covers the whole room,** not one person.
- **The name says XChaCha20, the code runs ChaCha20.** The module is named `XChaCha20Poly1305.py`, but it uses ChaCha20-Poly1305 with a 12-byte nonce. It's still an authenticated cipher.
- **The server sees who talks to whom.** Names travel in the clear.
- **Files and ping are unfinished.** `/sendfile` and `ping` are still in progress.
- **The remote shell is dangerous when on.** With `--allow-remote-shell`, anyone who can connect can run commands on the server machine. Only use it on a network you trust.

## Commands

| Command | What it does |
|---|---|
| `/help` | Lists commands and add-ons. |
| `/trust` | Swaps keys with everyone in the room. |
| `/cryp <cipher>` or `/encryption <cipher>` | Switches cipher. `/cryp ls` lists them. |
| `/status` | Shows who's online. |
| `/boot <name>` | Removes someone from the room. |
| `/hackmyserver` | Shell on the server, off unless the server runs with `--allow-remote-shell`. |
| `/mute`, `/unmute` | Turns chat sounds off and on. |
| `/about` | About socketchat. |
| `/exit` | Quits the client. |

Add-ons: `/weather <place>`, `/moon`, `/map <place>`, `/wikipedia <term>` (or `/wp`), `/urband <term>`, `/mathfacts <number>` and `/epic`, which stitches together NASA's latest images of the Earth turning. `/mathfacts` needs a free key from rapidapi.com:

```
export RAPIDAPI_KEY=your-key-here
```

## Tests

```
pip install pytest
python -m pytest tests
```

## Troubleshooting

On a Mac, `socket.gaierror: [Errno 8] nodename nor servname provided, or not known` usually clears if you turn Sharing on and off again in System Settings ([details](https://stackoverflow.com/a/53382881/5369711)).

## Credits

Jake Krajewski and M. Holcombe.

Built on [PyNaCl](https://pynacl.readthedocs.io/), [pycryptodome](https://www.pycryptodome.org/), [cryptography](https://pypi.org/project/cryptography/) and [argon2-cffi](https://argon2-cffi.readthedocs.io/).

## License

MIT. See [LICENSE.md](LICENSE.md).
