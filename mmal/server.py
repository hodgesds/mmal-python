from mmal.proto import beta_create_MMAL_server

def run_server(port, rpc):
    server = beta_create_MMAL_server(rpc)
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()
    try:
	while True:
	    pass
    except KeyboardInterrupt:
        server.stop()
