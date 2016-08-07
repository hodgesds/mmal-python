from __future__ import absolute_import
import unittest
from nose.tools import eq_
from mmal.proto import *

class TestPandas(unittest.TestCase):

    def test_get_col(self):
        ts = TimeSeries()
        idx = ts.Column()
        idx.strings.extend([
            "2016-01-01",
        ])
        idx.type = TYPE_STRING
        idx.name = "Index"

        col1 = ts.Column()
        col1.type = TYPE_STRING
        col1.name = "1"
        col1.strings.extend([
            "test"
        ])
        ts.columns.extend([idx, col1])

        eq_(
            "2016-01-01",
            get_col(ts, 0),
        )

        eq_(
            "test",
            get_col(ts, 1),
        )

if __name__ == '__main__':
    unittest.main()
