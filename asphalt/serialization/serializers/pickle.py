import pickle

from typeguard import check_argument_types

from ..api import Serializer


class PickleSerializer(Serializer):
    """
    Serializes objects using the standard library :mod:`pickle` module.

    .. warning:: This serializer is insecure because it allows execution of arbitrary code when
        deserializing. Avoid using this if at all possible.

    :param protocol: pickle protocol level to use (defaults to the highest possible)
    """

    __slots__ = 'protocol'

    def __init__(self, protocol: int=pickle.HIGHEST_PROTOCOL):
        assert check_argument_types()
        assert 0 <= protocol <= pickle.HIGHEST_PROTOCOL,\
            '"protocol" must be between 0 and {}'.format(pickle.HIGHEST_PROTOCOL)

        self.protocol = protocol

    def serialize(self, obj) -> bytes:
        return pickle.dumps(obj, protocol=self.protocol)

    def deserialize(self, payload: bytes):
        return pickle.loads(payload)

    @property
    def mimetype(self):
        return 'application/python-pickle'
