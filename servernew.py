from routernew import Router
import _thread

class Server(Router):
    def __init__(self, serverCode, host, port):
        super().__init__(serverCode, host, port)

        # listen for new Routers
        try:
            _thread.start_new_thread(self.listen, ())
        except:
            print("Error: unable to start listen thread")