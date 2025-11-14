import grpc
import events_pb2
import events_pb2_grpc


def run():
    # Connect to your server
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = events_pb2_grpc.EventServiceStub(channel)
        stub2 = events_pb2_grpc.TelemetryServiceStub(channel)

        # Start streaming
        request = events_pb2.StreamRequest()
        fix_request = events_pb2.FixRequest()
        stub.RequestFix(fix_request)
        try:
            for event in stub.StreamEvents(request):
                print(event)
        except grpc.RpcError as e:
            print(e)


if __name__ == "__main__":
    run()
