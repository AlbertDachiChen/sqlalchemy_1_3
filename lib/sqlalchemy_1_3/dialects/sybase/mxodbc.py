# sybase/mxodbc.py
# Copyright (C) 2005-2020 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
"""

.. dialect:: sybase+mxodbc
    :name: mxODBC
    :dbapi: mxodbc
    :connectstring: sybase+mxodbc://<username>:<password>@<dsnname>
    :url: http://www.egenix.com/

.. note::

    This dialect is a stub only and is likely non functional at this time.


"""
from sqlalchemy_1_3.connectors.mxodbc import MxODBCConnector
from sqlalchemy_1_3.dialects.sybase.base import SybaseDialect
from sqlalchemy_1_3.dialects.sybase.base import SybaseExecutionContext


class SybaseExecutionContext_mxodbc(SybaseExecutionContext):
    pass


class SybaseDialect_mxodbc(MxODBCConnector, SybaseDialect):
    execution_ctx_cls = SybaseExecutionContext_mxodbc


dialect = SybaseDialect_mxodbc
