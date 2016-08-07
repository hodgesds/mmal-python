# MMAL: Meteorological Middleware Application Layer
MMAL is a set of libraries designed to make handling time series meteorological
a simple task.

To understand the uses of MMAL lets start with an example.

## Example
Lets create a database using sqlite and and some data:

```sh
$ cat example.sql
CREATE TABLE IF NOT EXISTS temp(timestamp INTEGER PRIMARY KEY, temp INTEGER);
INSERT INTO temp VALUES(1470600282123, 10);
INSERT INTO temp VALUES(1470600282218, 11);
INSERT INTO temp VALUES(1470600282377, 12);
INSERT INTO temp VALUES(1470600282450, 11);
CREATE TABLE IF NOT EXISTS wind(timestamp TEXT PRIMARY KEY, speed INTEGER, direction REAL);
INSERT INTO wind VALUES('2016-08-07T16:00:20-04:00', 10, 120.3);
INSERT INTO wind VALUES('2016-08-07T16:00:20-05:00', 11, 183.8);
INSERT INTO wind VALUES('2016-08-07T16:00:20-06:00', 12, 90.1);
INSERT INTO wind VALUES('2016-08-07T16:00:20-07:00', 11, 220.4);
```

```sh
$ cat example.sql | sqlite3 example.sqlite
```

Now that we have a database lets use MMAL server as a rpc transport layer.

```sh
$ mmal server -d 'sqlite:///example.sqlite'
```

### Ping Pong
With the rpc server running we can now issue rpc requests with some command line tools.

The most basic rpc request is a **ping** request, this can be used to ping a server
and make sure it is up. Here is an example of a **ping** request:

```sh
$ mmal ping
id: "bb783ff8-5cdb-11e6-b733-44850017d653"
pong_reply {
      pong: "PONG"
}
```

The ping request was successful and the server responsed with a **pong** reply.
This is interesting, but lets do something useful with some ***actual*** data.

### Paths
MMAL provides an abstraction layer that you can think of like a file system. A
***folder*** contains many ***files*** which contain data; likewise with MMAL
data is stored in a path hierarchy. In this example the path `/temp` maps to
the database table **temp** that was created earlier. When a **path** request
is issued information is returned about the path.

Here is a simple example using the **temp** table:
`mmal path /temp`

```sh
$ mmal path /temp
id: "8555b0d0-5cdc-11e6-ba72-44850017d653"
type: PATH
path_reply {
  paths {
    parts: "temp"
    columns: "timestamp"
    columns: "temp"
  }
}

```

As you can see the **path** is returned along with the column names.


### Time Series
MMAL is designed to be a middleware layer for working with time series data.
Using the filesystem inspired design it becomes a powerful middleware layer to
interact with time series data. Querying the data exposed by the rpc server is
done with a **time series** or **ts** request.

Here is a simple **ts** request:
`mmal ts /temp`

```sh
$ mmal ts /temp
id: "5480c282-5cdd-11e6-b482-44850017d653"
type: TIMESERIES
ts_reply {
  time_series {
    columns {
      int64s: 1470600282123
      int64s: 1470600282218
      int64s: 1470600282377
      int64s: 1470600282450
      type: TYPE_INT64
      name: "timestamp"
    }
    columns {
      int64s: 10
      int64s: 11
      int64s: 12
      int64s: 11
      type: TYPE_INT64
      name: "temp"
    }
  }
  paths {
    parts: "temp"
    columns: "timestamp"
    columns: "temp"
  }
}
```

The **ts** command line option has many arguments for querying and filtering data:

```sh
usage: mmal ts [-h] [-p PORT] [--host HOST] [-c COLUMNS] [-o OFFSET]
               [-l LIMIT]
               [path [path ...]]

positional arguments:
  path                  path

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Default port
  --host HOST           Default host
  -c COLUMNS, --columns COLUMNS
                        Columns
  -o OFFSET, --offset OFFSET
                        Offset
  -l LIMIT, --limit LIMIT
                        Limit
```

Using a **ts** request becomes even more powerful when you combine filters across many **paths**:

```sh
$ mmal ts -l 1 /temp /wind
id: "ca920d5a-5cdd-11e6-92ad-44850017d653"
type: TIMESERIES
ts_reply {
  time_series {
    columns {
      int64s: 1470600282123
      type: TYPE_INT64
      name: "timestamp"
    }
    columns {
      int64s: 10
      type: TYPE_INT64
      name: "temp"
    }
  }
  time_series {
    columns {
      strings: "2016-08-07T16:00:20-04:00"
      type: TYPE_STRING
      name: "timestamp"
    }
  }
  paths {
    parts: "temp"
    columns: "timestamp"
    columns: "temp"
  }
  paths {
    parts: "wind"
    columns: "timestamp"
    columns: "speed"
    columns: "direction"
  }
}
```
