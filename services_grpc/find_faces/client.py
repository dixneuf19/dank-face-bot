import grpc
import time
from logzero import logger

from . import find_faces_pb2
from . import find_faces_pb2_grpc


class FindFacesClient:

    def __init__(self, host='localhost:50051'):
        self.channel = grpc.insecure_channel(host)
        self.stub = find_faces_pb2_grpc.FindFacesStub(self.channel)

    def find_faces(self, file_path):
        picture = find_faces_pb2.Picture(path=file_path)
        request = find_faces_pb2.FindFacesRequest(picture=picture)
        response = self.stub.FindFaces(request)
        return response


def find_faces(host="localhost:50051", file_path=""):
    with grpc.insecure_channel(host) as channel:
        stub = find_faces_pb2_grpc.FindFacesStub(channel)
        picture = find_faces_pb2.Picture(path=file_path)
        request = find_faces_pb2.FindFacesRequest(picture=picture)
        response = stub.FindFaces(request)
        return response