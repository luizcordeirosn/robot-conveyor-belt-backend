from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def as_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }