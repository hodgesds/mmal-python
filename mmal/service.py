from sqlalchemy import *
from sqlalchemy.sql.expression import select, table as TABLE
from sqlalchemy.sql.expression import column as COLUMN
from mmal.utils import extend_col
from mmal.proto import (
    BetaMMALServicer,
    Reply,
    Path,
    TimeSeries,
)

def exception_handler(func):
    def inner(*args, **kwargs):
        try:
	    return func(*args, **kwargs)
        except Exception as e:
            req = args[1]
	    reply = Reply()

	    if req.type == req.PING:
		reply.type = reply.PONG
            elif req.type == req.PATH:
		reply.type = reply.PATH
            elif req.type == req.TIMESERIES:
		reply.type = reply.TIMESERIES

	    reply.error.type = reply.error.EXCEPTION
            reply.error.message = str(e)

            return reply

    return inner

class BaseMmalRPC(BetaMMALServicer):

    @exception_handler
    def RPCRequest(self, request, context):
        if request.type == request.PING:
            return self.on_ping(request)
        elif request.type == request.PATH:
            return self.on_path(request)
        elif request.type == request.TIMESERIES:
            return self.on_ts(request)

    def on_ping(self, request):
        reply = Reply()
        reply.id = request.id
        reply.type = reply.PONG
        reply.pong_reply.pong = "PONG"
        return reply

    def on_path(self, request):
        reply = Reply()
        reply.id = request.id
        reply.type = reply.PATH
        return reply

    def on_ts(self, request):
        reply = Reply()
        reply.id = request.id
        reply.type = reply.TIMESERIES
        return reply

def strip_path(path):
    if path[0] == u'/':
        return path[1:]

    return path

class MmalRPCSqlAlchemy(BaseMmalRPC):
    sql_engine = None
    tables = dict()

    def connect(self, dsn):
        self.sql_engine = create_engine(dsn)
        inspector = inspect(self.sql_engine)
        meta = MetaData()
        meta.reflect(bind=self.sql_engine)
        self.meta = meta
        tables = inspector.get_table_names()

        for table in tables:
            self.tables[table] = inspector.get_columns(table)

    def on_path(self, request):
        reply = super(MmalRPCSqlAlchemy, self).on_path(request)
        req_paths = [ x.parts for x in request.path_request.paths[:] ]

        if any([ x[0] == u'/' and len(x) <= 1 for x in req_paths ]):
            for table, cols in self.tables.items():
                path = Path()
                path.type = path.LEAF
                path.parts.extend([table])
                path.columns.extend([ x.get('name', '') for x in cols])
                reply.path_reply.paths.extend([path])

        else:
            for req_path in req_paths:
                if req_path[-1] not in self.tables:
                    reply.error.type = reply.error.INVALID_PATH
                    reply.error.message = "no such path {}".format(req_path)
                    break

                cols = self.tables[req_path[-1]]
                path = Path()
                path.type = path.LEAF
                path.parts.extend(strip_path(req_path))
                path.columns.extend([ x.get('name', '') for x in cols])
                reply.path_reply.paths.extend([path])

        return reply

    def on_ts(self, request):
        reply = super(MmalRPCSqlAlchemy, self).on_ts(request)
        req_paths = [ x.parts for x in request.ts_request.paths[:] ]
        req_cols = request.ts_request.columns[:]

        if any([ x[0] == u'/' and len(x) <= 1 for x in req_paths ]) or len(req_paths) == 0:
            for table, cols in self.tables.items():
                col_names = [ x.get('name', '') for x in cols]

                if len(req_cols) == 0:
                    req_cols = col_names

                ts = TimeSeries()
                if len(req_cols) > 0:
                    ts.columns.extend([
                        ts.Column(name=x)
                        for x in req_cols if x in col_names
                    ])
                else:
                    ts.columns.extend([
                        ts.Column(name=x)
                        for x in col_names
                    ])

                with self.sql_engine.connect() as conn:
                    sql_table = self.meta.tables[table]
                    statement = select(
                        from_obj=sql_table,
                    ).with_only_columns([
                        sql_table.columns.get(str(x))
                        for x in req_cols if str(x) in sql_table.columns
                    ])

                    statement = statement.limit(request.ts_request.limit)
                    statement = statement.offset(request.ts_request.offset)

                    rows = conn.execute(statement)

                    for row in rows:
                        row_idx = 0
                        for i, col_data in enumerate(row):
                            if col_data is not None and len(ts.columns)-1 >= row_idx:
                                extend_col(ts.columns[row_idx], col_data)
                                row_idx += 1

                # set path info
                path = Path()
                path.type = path.LEAF
                path.parts.extend([table])
                path.columns.extend(col_names)
                reply.ts_reply.time_series.extend([ts])
                reply.ts_reply.paths.extend([path])

        else:
            for req_path in req_paths:
                if req_path[-1] not in self.tables:
                    reply.error.type = reply.error.INVALID_PATH
                    reply.error.message = "no such path {}".format(req_path)
                    break

                table = req_path[-1]
                cols = self.tables[req_path[-1]]
                col_names = [ x.get('name', '') for x in cols]
                if len(req_cols) == 0:
                    req_cols = col_names

                ts = TimeSeries()
                if len(req_cols) > 0:
                    ts.columns.extend([
                        ts.Column(name=x)
                        for x in req_cols if x in col_names
                    ])
                else:
                    ts.columns.extend([
                        ts.Column(name=x)
                        for x in col_names
                    ])

                with self.sql_engine.connect() as conn:
                    sql_table = self.meta.tables[table]
                    statement = select(
                        from_obj=sql_table,
                    ).with_only_columns([
                        sql_table.columns.get(str(x))
                        for x in req_cols if str(x) in sql_table.columns
                    ])
                    statement = statement.limit(request.ts_request.limit)
                    statement = statement.offset(request.ts_request.offset)

                    rows = conn.execute(statement)

                    for row in rows:
                        row_idx = 0
                        for i, col_data in enumerate(row):
                            if col_data is not None and len(ts.columns)-1 >= row_idx:
                                extend_col(ts.columns[row_idx], col_data)
                                row_idx += 1

                    # set path info
                    path = Path()
                    path.type = path.LEAF
                    path.parts.extend([table])
                    path.columns.extend(col_names)
                    reply.ts_reply.time_series.extend([ts])
                    reply.ts_reply.paths.extend([path])

        return reply
