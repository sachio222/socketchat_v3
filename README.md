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

## Usage

#### Encrypted chat
0.

## Commands

```/trust``` Exchange keys (Currently only works with all clients, single client trust coming soon)

```/help``` Shows commands, and addons

```/about```

```/mute```

```/unmute```

```/status``` Shows who's in the room at the moment. 

```ping``` IN PROGRESS. Sends a ping request to the server.

```/exit``` Quits the client. 

```/sendfile``` IN PROGRESS. Sends file (currently unencrypted) to selected user.

## Current Addons

```/wikipedia``` Wikipedia

```/maps``` Open street maps

```/urband``` Urban Dictionary

```/moon``` Current Phase of the moon

```/weather``` Weather near you

```/epic``` splices together latest Earth rotation sequence from the Earth Polychromatic Imaging Camera

## Contributors
J. Krajewski
M. Holcombe


### Third party libraries
https://pypi.org/project/cryptography/

Install using ``` pip install cryptography```

https://pynacl.readthedocs.io/en/1.4.0/

Install using ```pip install pynacl```

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

