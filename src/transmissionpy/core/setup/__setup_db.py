from __future__ import annotations

from transmissionpy.core import db
from transmissionpy.core.depends import db_depends

def setup_database():
    engine = db_depends.get_db_engine()
    db.create_base_metadata(base=db.Base, engine=engine)
