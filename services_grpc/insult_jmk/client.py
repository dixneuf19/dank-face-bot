import grpc
import time

from . import insult_jmk_pb2
from . import insult_jmk_pb2_grpc


class InsultJMKClient:

    def __init__(self, host='localhost:50051'):
        self.channel = grpc.insecure_channel(host)
        self.stub = insult_jmk_pb2_grpc.InsulterStub(self.channel)

    def get_insult(self, name=""):
        name_grpc = insult_jmk_pb2.InsultRequest(name=name)
        response = self.stub.GetInsult(name_grpc)
        return response.message

def get_insult(host="localhost:50051", name=""):
    with grpc.insecure_channel(host) as channel:

        stub = insult_jmk_pb2_grpc.InsulterStub(channel)
        grpc_name = insult_jmk_pb2.InsultRequest(name=name)
        response = stub.GetInsult(grpc_name)
        return response.message
