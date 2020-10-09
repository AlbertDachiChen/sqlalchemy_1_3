"""Generic mapping to Select statements"""
import sqlalchemy_1_3 as sa
from sqlalchemy_1_3 import column
from sqlalchemy_1_3 import Integer
from sqlalchemy_1_3 import select
from sqlalchemy_1_3 import String
from sqlalchemy_1_3 import testing
from sqlalchemy_1_3.orm import mapper
from sqlalchemy_1_3.orm import Session
from sqlalchemy_1_3.testing import assert_raises
from sqlalchemy_1_3.testing import assert_raises_message
from sqlalchemy_1_3.testing import AssertsCompiledSQL
from sqlalchemy_1_3.testing import eq_
from sqlalchemy_1_3.testing import fixtures
from sqlalchemy_1_3.testing.schema import Column
from sqlalchemy_1_3.testing.schema import Table


# TODO: more tests mapping to selects


class SelectableNoFromsTest(fixtures.MappedTest, AssertsCompiledSQL):
    @classmethod
    def define_tables(cls, metadata):
        Table(
            "common",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("data", Integer),
            Column("extra", String(45)),
        )

    @classmethod
    def setup_classes(cls):
        class Subset(cls.Comparable):
            pass

    def test_no_tables(self):
        Subset = self.classes.Subset

        selectable = select([column("x"), column("y"), column("z")]).alias()
        mapper(Subset, selectable, primary_key=[selectable.c.x])

        self.assert_compile(
            Session().query(Subset),
            "SELECT anon_1.x AS anon_1_x, anon_1.y AS anon_1_y, "
            "anon_1.z AS anon_1_z FROM (SELECT x, y, z) AS anon_1",
            use_default_dialect=True,
        )

    def test_no_table_needs_pl(self):
        Subset = self.classes.Subset

        selectable = select([column("x"), column("y"), column("z")]).alias()
        assert_raises_message(
            sa.exc.ArgumentError,
            "could not assemble any primary key columns",
            mapper,
            Subset,
            selectable,
        )

    def test_no_selects(self):
        Subset, common = self.classes.Subset, self.tables.common

        subset_select = select([common.c.id, common.c.data])
        assert_raises(
            sa.exc.InvalidRequestError, mapper, Subset, subset_select
        )

    def test_basic(self):
        Subset, common = self.classes.Subset, self.tables.common

        subset_select = select([common.c.id, common.c.data]).alias()
        mapper(Subset, subset_select)
        sess = Session(bind=testing.db)
        sess.add(Subset(data=1))
        sess.flush()
        sess.expunge_all()

        eq_(sess.query(Subset).all(), [Subset(data=1)])
        eq_(sess.query(Subset).filter(Subset.data == 1).one(), Subset(data=1))
        eq_(sess.query(Subset).filter(Subset.data != 1).first(), None)

        subset_select = sa.orm.class_mapper(Subset).persist_selectable
        eq_(
            sess.query(Subset).filter(subset_select.c.data == 1).one(),
            Subset(data=1),
        )
