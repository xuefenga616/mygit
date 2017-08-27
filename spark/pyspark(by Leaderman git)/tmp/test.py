datas = {"key1": "val1", "key2": "val2", "key3": "val3"}

print sorted(datas.items())

from pyspark.sql.types import Row

row = Row(key1="val1", key2="val2", key3="val3")

print row.__fields__

print tuple(row)

print zip(row.__fields__, tuple(row))

from collections import namedtuple

NamedRow = namedtuple("NamedRow", ["key1", "key2", "key3"])

row = NamedRow(key1="val1", key2="val2", key3="val3")

print row._fields

print tuple(row)

print zip(row._fields, tuple(row))


class MyRow(object):

    def __init__(self, key1, key2, key3):
        self.key1 = key1
        self.key2 = key2
        self.key3 = key3

row = MyRow("val1", "val2", "val3")

print sorted(row.__dict__.items())

row = ("val1", "val2", "val3")

names = ['_%d' % i for i in range(1, len(row) + 1)]

print zip(names, row)
