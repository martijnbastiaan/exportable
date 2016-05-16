import itertools
import datetime
import dateutil.parser

CREATION_COUNTER = itertools.count()


class Column(object):
    def __init__(self, ctype, label=None, cellfunc=None, verbose_name=None, _creation_counter=None):
        self.type = ctype
        self.label = label
        self.cellfunc = cellfunc
        self.verbose_name = label if verbose_name is None else verbose_name

        # Index refers to the index of the column including None-columns
        self._index = 0

        # View index refers to the index of the column excluding None-columns
        self._view_index = 0

        # Creation counter is kept to determine the order in declared tables
        self._creation_counter = next(CREATION_COUNTER) if _creation_counter is None else _creation_counter

    def from_str(self, s):
        """Convert value from str. Might be used by importers which support all formats."""
        return self.type(s) if s else None

    def to_str(self, value):
        """Convert value into string representation. Might be used by exporters which file
        format does not support types or specific types."""
        return "" if value is None else str(value)

    def __copy__(self):
        return self.__class__(self.type, self.label, self.cellfunc, self.verbose_name, self._creation_counter)

    def __repr__(self):
        return "<{}(label={})>".format(self.__class__.__name__, self.label)


class TextColumn(Column):
    def __init__(self, label=None, **kwargs):
        super().__init__(str, label, **kwargs)

    def to_str(self, value):
        return value


class IntColumn(Column):
    def __init__(self, label=None, **kwargs):
        super().__init__(int, label, **kwargs)


class FloatColumn(Column):
    def __init__(self, label=None, **kwargs):
        super().__init__(float, label, **kwargs)


class DateColumn(Column):
    def __init__(self, label=None, **kwargs):
        super().__init__(datetime.date, label, **kwargs)

    def from_str(self, s) -> datetime.date:
        return dateutil.parser.parse(s).date() if s else None

    def to_str(self, date: datetime.date):
        return date.isoformat()


class DateTimeColumn(Column):
    def __init__(self, label=None, **kwargs):
        super().__init__(datetime.datetime, label, **kwargs)

    def from_str(self, s) -> datetime.datetime:
        return dateutil.parser.parse(s) if s else None

    def to_str(self, time: datetime.datetime):
        return time.isoformat()
