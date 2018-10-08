import uuid
import arrow
import decimal


class Event:
    def __init__(self, *, id, t, **kwargs):
        assert isinstance(id, uuid.UUID)
        assert isinstance(t, arrow.Arrow)
        assert self._validate_raw_data(kwargs)

        self.__dict__['id'] = id
        self.__dict__['t'] = t
        self.__dict__.update(kwargs)

    def _validate_raw_data(self, value):
        assert isinstance(value, (str, int, decimal.Decimal, list, dict))
        if isinstance(value, list):
            for i in value:
                self._validate_raw_data(i)
        elif isinstance(value, dict):
            for k, v in value.items():
                assert isinstance(k, str)
                self._validate_raw_data(v)
        return True

    def __setattr__(self, key, value):
        if hasattr(self, key):
            raise AttributeError(
                '{} attributes can be added but not modified. '
                'Attribute {!r} already exists with value {!r}'
                    .format(self.__class__.__name__, key, getattr(self, key))
            )

        self._validate_raw_data(value)
        self.__dict__[key] = value

    def __eq__(self, rhs):
        if type(self) is not type(rhs):
            return NotImplemented

        if self.id != rhs.id:
            return False

        return self.__dict__ == rhs.__dict__

    def __ne__(self, rhs):
        return not (self == rhs)

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return '{}(id={}, t={}, {})'.format(
            self.__class__.__qualname__,
            str(self.id)[-6:],
            self.t,
            ', '.join(
                "{0}={1}".format(k, v)
                for k, v in sorted(self.__dict__.items())
                if k not in ('id', 't')
            )
        )

    def to_raw(self):
        raw = dict(self.__dict__)
        raw['id'] = str(raw['id'])
        raw['t'] = str(raw['t'])
        return raw
