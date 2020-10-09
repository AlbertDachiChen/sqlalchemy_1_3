from sqlalchemy_1_3 import dialects
from sqlalchemy_1_3.testing import fixtures
from sqlalchemy_1_3.testing import is_not


class ImportStarTest(fixtures.TestBase):
    def _all_dialect_packages(self):
        return [
            getattr(__import__("sqlalchemy_1_3.dialects.%s" % d).dialects, d)
            for d in dialects.__all__
            if not d.startswith("_")
        ]

    def test_all_import(self):
        for package in self._all_dialect_packages():
            for item_name in package.__all__:
                is_not(None, getattr(package, item_name))
