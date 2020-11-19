import argparse

def ArgParser():
    host, port = None

    parser = argparse.ArgumentParser(description='Lightweight encrypted chat.',
                                     epilog='Going under...')

    parser.add_argument('-g',
                        '--goober',
                        help='Goober chat, or no encryption.',
                        action='store_false',
                        dest='is_encrypted')

    addr_group = parser.add_mutually_exclusive_group()

    addr_group.add_argument(
        '-f',
        '--full-address',
        help='Input full address. eg: xxx.xxx.xxx.xxx:######',
        action='store',
        type=str,
        dest='addr')
    addr_group.add_argument(
        '-H',
        '--host',
        help='Input host name or address. eg: xxx.xxx.xxx.xxx',
        action='store',
        type=str,
        dest='host')

    parser.add_argument('-P',
                        '--port',
                        help='Input port number.',
                        action='store',
                        type=int,
                        dest='port')

    args = parser.parse_args()

    if not args.addr:
        if not args.host:
            host = input('-+- Enter hostname of server: ')
            host = host or 'ubuntu'
        else:
            host = args.host
            print(f'-+- Hostname: {host}')

        if not args.port:
            port = input('-+- Choose port: ')
            port = port or '12222'
            port = int(port)
        else:
            port = args.port
            print(f'-+- Port: {port}')
    
    return args