import random
import threading
import time

from sqlalchemy_1_3 import Column
from sqlalchemy_1_3 import exc
from sqlalchemy_1_3 import ForeignKey
from sqlalchemy_1_3 import Integer
from sqlalchemy_1_3 import String
from sqlalchemy_1_3.ext.declarative import declarative_base
from sqlalchemy_1_3.ext.declarative import declared_attr
from sqlalchemy_1_3.orm import clear_mappers
from sqlalchemy_1_3.orm import exc as orm_exc
from sqlalchemy_1_3.orm import relationship
from sqlalchemy_1_3.orm import Session
from sqlalchemy_1_3.testing import fixtures


class ConcurrentUseDeclMappingTest(fixtures.TestBase):
    def teardown(self):
        clear_mappers()

    @classmethod
    def make_a(cls, Base):
        class A(Base):
            __tablename__ = "a"

            id = Column(Integer, primary_key=True)
            data = Column(String)
            bs = relationship("B")

        # need a strong ref so that the class is not gc'ed
        cls.A = A

    @classmethod
    def query_a(cls, Base, result):
        s = Session()
        time.sleep(random.random() / 100)
        A = cls.A
        try:
            s.query(A).join(A.bs)
        except orm_exc.UnmappedClassError as oe:
            # this is the failure mode, where B is being handled by
            # declarative and is in the registry but not mapped yet.
            result[0] = oe
        except exc.InvalidRequestError:
            # if make_b() starts too slowly, we can reach here, because
            # B isn't in the registry yet.  We can't guard against this
            # case in the library because a class can refer to a name that
            # doesn't exist and that has to raise.
            result[0] = True
        else:
            # no conflict
            result[0] = True

    @classmethod
    def make_b(cls, Base):
        class B(Base):
            __tablename__ = "b"
            id = Column(Integer, primary_key=True)

            @declared_attr
            def data(cls):
                time.sleep(0.001)
                return Column(String)

            a_id = Column(ForeignKey("a.id"))

        cls.B = B

    def test_concurrent_create(self):
        for i in range(50):
            Base = declarative_base()
            clear_mappers()

            self.make_a(Base)
            result = [False]
            threads = [
                threading.Thread(target=self.make_b, args=(Base,)),
                threading.Thread(target=self.query_a, args=(Base, result)),
            ]

            for t in threads:
                t.start()

            for t in threads:
                t.join()

            if isinstance(result[0], orm_exc.UnmappedClassError):
                raise result[0]
