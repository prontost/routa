"""Work module database: unified Avalone SQLite.

All Work tables live in the single Avalone platform database and use the
`work_` prefix. Modules import `DB_PATH` or `connection()` from here.
"""

import os
import sqlite3

from avalone_core.db import connection as _connection
from avalone_core.db import DB_PATH, configure

# Legacy test override: allow isolated test DBs while the app uses the unified DB.
if os.getenv("ROUTA_DB_PATH"):
    configure(os.getenv("ROUTA_DB_PATH"))


def connection() -> sqlite3.Connection:
    """Return a connection to the unified Avalone database."""
    return _connection()
