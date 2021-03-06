from sqlalchemy_1_3 import Column
from sqlalchemy_1_3 import Integer
from sqlalchemy_1_3 import MetaData
from sqlalchemy_1_3 import select
from sqlalchemy_1_3 import String
from sqlalchemy_1_3 import Table
from sqlalchemy_1_3.engine import default
from sqlalchemy_1_3.testing import AssertsExecutionResults
from sqlalchemy_1_3.testing import fixtures
from sqlalchemy_1_3.testing import profiling


t1 = t2 = None


class CompileTest(fixtures.TestBase, AssertsExecutionResults):
    __requires__ = ("cpython",)
    __backend__ = True

    @classmethod
    def setup_class(cls):

        global t1, t2, metadata
        metadata = MetaData()
        t1 = Table(
            "t1",
            metadata,
            Column("c1", Integer, primary_key=True),
            Column("c2", String(30)),
        )

        t2 = Table(
            "t2",
            metadata,
            Column("c1", Integer, primary_key=True),
            Column("c2", String(30)),
        )

        cls.dialect = default.DefaultDialect()

        # do a "compile" ahead of time to load
        # deferred imports, use the dialect to pre-load
        # dialect-level types
        t1.insert().compile(dialect=cls.dialect)

        # go through all the TypeEngine
        # objects in use and pre-load their _type_affinity
        # entries.
        for t in (t1, t2):
            for c in t.c:
                c.type._type_affinity
        from sqlalchemy_1_3.sql import sqltypes

        for t in list(sqltypes._type_map.values()):
            t._type_affinity

    @profiling.function_call_count()
    def test_insert(self):
        t1.insert().compile(dialect=self.dialect)

    @profiling.function_call_count(variance=0.15)
    def test_update(self):
        t1.update().compile(dialect=self.dialect)

    def test_update_whereclause(self):
        t1.update().where(t1.c.c2 == 12).compile(dialect=self.dialect)

        @profiling.function_call_count(variance=0.20)
        def go():
            t1.update().where(t1.c.c2 == 12).compile(dialect=self.dialect)

        go()

    def test_select(self):
        # give some of the cached type values
        # a chance to warm up
        s = select([t1], t1.c.c2 == t2.c.c1)
        s.compile(dialect=self.dialect)

        @profiling.function_call_count()
        def go():
            s = select([t1], t1.c.c2 == t2.c.c1)
            s.compile(dialect=self.dialect)

        go()

    def test_select_labels(self):
        # give some of the cached type values
        # a chance to warm up
        s = select([t1], t1.c.c2 == t2.c.c1).apply_labels()
        s.compile(dialect=self.dialect)

        @profiling.function_call_count()
        def go():
            s = select([t1], t1.c.c2 == t2.c.c1).apply_labels()
            s.compile(dialect=self.dialect)

        go()
