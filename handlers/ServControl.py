from chatutils import utils
from handlers.routers import ServerCmds

def data_router(client_cnxn, data):
    """Sorts through incoming data, by looking at prefixes."""
    
    print(data)
    if data == "/".encode():
        print(data)
        

    # """Handles incoming data based on its message type."""
    # # Send confirm dialog to recip if user is sending file.
    # if data == "/".encode():
    #     # Drain socket of controller message so it doesn't print.
    #     control = self.unpack_msg(client_cnxn).decode()
    #     control = control.split(' ')

    #     if control[0] == 'status':
    #         # Send room status.
    #         # TODO: break into method.
    #         status, _ = self.get_status(nick_addy_dict)
    #         status = self.pack_message('S', status)
    #         if control[-1] == 'self':
    #             target = 'self'
    #         else:
    #             target = 'all'
    #         self.broadcast(status, sockets, client_cnxn, target=target)