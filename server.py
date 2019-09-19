import grpc
from concurrent import futures
import time

import chatServer_pb2 as chat 
import chatServer_pb2_grpc as rpc

class ChatServer(rpc.ChatServerServicer):

    def __init__(self):
        self.chats = []

    def ChatStream(self, request_iterator, context):
        lastindex = 0
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:
            # Check if there are any new messages
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n

    def SendNote(self, request, context):
        print("[{}]: {}".format(request.name, request.message))
        self.chats.append(request)
        return chat.Empty()


if __name__ == '__main__':

    port = 50051
    
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_ChatServerServicer_to_server(ChatServer(), server)

    print('Starting server. Listening...')
    server.add_insecure_port('[::]:' + str(port))
    server.start()

    # Server starts in background (another thread) so keep waiting
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)