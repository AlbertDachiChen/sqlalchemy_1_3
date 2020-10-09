# firebird/__init__.py
# Copyright (C) 2005-2020 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from sqlalchemy_1_3.dialects.firebird.base import BIGINT
from sqlalchemy_1_3.dialects.firebird.base import BLOB
from sqlalchemy_1_3.dialects.firebird.base import CHAR
from sqlalchemy_1_3.dialects.firebird.base import DATE
from sqlalchemy_1_3.dialects.firebird.base import FLOAT
from sqlalchemy_1_3.dialects.firebird.base import NUMERIC
from sqlalchemy_1_3.dialects.firebird.base import SMALLINT
from sqlalchemy_1_3.dialects.firebird.base import TEXT
from sqlalchemy_1_3.dialects.firebird.base import TIME
from sqlalchemy_1_3.dialects.firebird.base import TIMESTAMP
from sqlalchemy_1_3.dialects.firebird.base import VARCHAR
from . import base  # noqa
from . import fdb  # noqa
from . import kinterbasdb  # noqa


base.dialect = dialect = fdb.dialect

__all__ = (
    "SMALLINT",
    "BIGINT",
    "FLOAT",
    "FLOAT",
    "DATE",
    "TIME",
    "TEXT",
    "NUMERIC",
    "FLOAT",
    "TIMESTAMP",
    "VARCHAR",
    "CHAR",
    "BLOB",
    "dialect",
)
