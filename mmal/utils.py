from mmal.proto import *
import sys


if sys.maxint > 2**32:
     INT_64 = True
else:
     INT_64 = False


def get_col(ts, index):
    col_type = ts.columns[index].type
    if col_type == TYPE_BOOL:
        return ts.columns[index].bools
    elif col_type == TYPE_BYTES:
        return ts.columns[index].raw_bytes
    elif col_type == TYPE_DOUBLE:
        return ts.columns[index].doubles
    elif col_type == TYPE_FIXED32:
        return ts.columns[index].fixed32s
    elif col_type == TYPE_FIXED64:
        return ts.columns[index].fixed64s
    elif col_type == TYPE_FLOAT:
        return ts.columns[index].floats
    elif col_type == TYPE_INT32:
        return ts.columns[index].int32s
    elif col_type == TYPE_INT64:
        return ts.columns[index].int64s
    elif col_type == TYPE_SFIXED32:
        return ts.columns[index].sfixed32s
    elif col_type == TYPE_SFIXED64:
        return ts.columns[index].sfixed64s
    elif col_type == TYPE_SINT32:
        return ts.columns[index].sint32s
    elif col_type == TYPE_SINT64:
        return ts.columns[index].sint64s
    elif col_type == TYPE_STRING:
        return ts.columns[index].strings
    elif col_type == TYPE_UINT32:
        return ts.columns[index].uint32s
    elif col_type == TYPE_UINT64:
        return ts.columns[index].uint64s

def extend_col(col, x):
    if isinstance(x, basestring):
        col.type = TYPE_STRING
        col.strings.extend([x])
    if isinstance(x, bool):
        col.type = TYPE_BOOL
        col.bools.extend([x])
    elif isinstance(x, bytes):
        col.type = TYPE_BYTES
        col.raw_bytes.extend([x])
    elif isinstance(x, bytearray):
        col.type = TYPE_BYTES
        col.raw_bytes.extend([x])
    elif isinstance(x, float):
        col.type = TYPE_FLOAT
        col.floats.extend([x])

    if INT_64:
        if isinstance(x, (int, long)):
            col.type = TYPE_INT64
            col.int64s.extend([x])
    else:
        if isinstance(x, (int, long)):
            col.type = TYPE_INT32
            col.int32s.extend([x])

def get_type(x):
    if isinstance(x, basestring):
        return TYPE_STRING
    if isinstance(x, bool):
        return TYPE_BOOL
    elif isinstance(x, bytes):
        return TYPE_BYTES
    elif isinstance(x, bytearray):
        return TYPE_BYTES
    elif isinstance(x, float):
        return TYPE_FLOAT

    if INT_64:
        if isinstance(x, (int, long)):
            return TYPE_INT64
    else:
        if isinstance(x, (int, long)):
            return TYPE_INT32
