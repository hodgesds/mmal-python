import uuid
from mmal.proto import (
    beta_create_MMAL_stub,
    beta_implementations,
    Path,
    PathRequest,
    PingRequest,
    Request,
    TimeSeriesRequest,
)


class Client(object):
    def __init__(self, host, port):
        self.channel = beta_implementations.insecure_channel(host, port)
        self.stub =  beta_create_MMAL_stub(self.channel)

    def request(self, request):
        return self.stub.RPCRequest(request, 10)

    def _mk_request(self):
        return Request(id=str(uuid.uuid1()))

    def _mk_paths(self, paths):
        return [
            Path(parts=path)
            for path in paths
        ]

    def ping_request(self, paths):
        ping_req = PingRequest()
        req = Request(ping_request=ping_req)
        req.id = str(uuid.uuid1())
        req.type = req.PING

        return self.request(req)

    def path_request(self, paths):
        path_req = PathRequest()
        path_req.paths.extend(self._mk_paths(paths))
        req = Request(path_request=path_req)
        req.id = str(uuid.uuid1())
        req.type = req.PATH

        return self.request(req)

    def ts_request(self, paths, cols=[], offset=0, limit=10):
        ts_req = TimeSeriesRequest(offset=offset, limit=limit)
        ts_req.paths.extend(self._mk_paths(paths))
        ts_req.columns.extend(list(set(cols)))
        req = Request(ts_request=ts_req)
        req.id = str(uuid.uuid1())
        req.type = req.TIMESERIES

        return self.request(req)
