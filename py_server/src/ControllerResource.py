#ControllerResource.py

from PyQt5.QtCore import QObject, pyqtSignal
from aiocoap import Message, resource, Code


class ControllerSignalEmitter(QObject):
    payload_received = pyqtSignal(tuple)  # Change to tuple for ip address and payload


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
        client_address = request.remote.hostinfo

        self.signal_emitter.payload_received.emit((client_address, payload))  # Pass tuple with client_address and payload
        response_payload = "Receive from Client: " + str(payload)  # Note: payload is integer, so convert it to string first

        response = Message(code=Code.CONTENT)
        response.payload = response_payload.encode('utf-8')
        response.opt.content_format = 0
        return response
