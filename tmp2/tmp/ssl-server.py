# socket has 5 things.

import socket, ssl

host = socket.gethostname()
ip = socket.gethostbyname(host)
port = 2222
addy = (ip, port)

server_ctxt = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
server_ctxt.set_ecdh_curve('prime256v1')
server_ctxt.load_cert_chain('../certificate.pem', '../key.pem')
server_ctxt.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384')
server_ctxt.options |= ssl.OP_NO_COMPRESSION
server_ctxt.options |= ssl.OP_SINGLE_ECDH_USE
server_ctxt.options |= ssl.OP_CIPHER_SERVER_PREFERENCE

# Create
with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    s.bind(addy)
    print(f'socket bound to {ip}')

    s.listen(5)
    print('waiting for signal')

    with server_ctxt.wrap_socket(s, server_side=True) as ssock:
        conn, addr = ssock.accept()

    msg = conn.recv(1024)
    print(msg.decode())