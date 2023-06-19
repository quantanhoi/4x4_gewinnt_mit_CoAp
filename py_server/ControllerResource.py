from PyQt5.QtCore import QObject, pyqtSignal
from aiocoap import Message, resource, Code

class ControllerSignalEmitter(QObject):
    payload_received = pyqtSignal(int)  # Change to int

class ControllerResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.playerID = 0
        self.signal_emitter = ControllerSignalEmitter()

    async def render_post(self, request):
        if len(request.payload) != 1:
            print("Warning: Expected payload of length 1, got length", len(request.payload))
            return
        payload = request.payload[0]  # convert byte to integer
        #print(f'Received message from client: {payload}')
        # ...
        # Rest of the code remains same
        if payload == [ord(char) for char in "init"]:  # Changed to compare with list
            response_payload = f"Player ID: {self.playerID}"
            self.playerID += 1
        else:
            self.signal_emitter.payload_received.emit(payload)
            response_payload = "Receive from Client: " + bytes(payload).decode('utf-8', 'ignore')
        response = Message(code=Code.CONTENT)
        response.payload = response_payload.encode('utf-8')
        response.opt.content_format = 0
        return response
