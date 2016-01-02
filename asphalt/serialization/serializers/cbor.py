from typeguard import check_argument_types

from ..api import Serializer

try:
    import cbor
except ImportError:  # pragma: no cover
    raise ImportError('cbor is missing -- install asphalt-serialization[cbor] to fix this')


class CBORSerializer(Serializer):
    """
    Serializes objects using CBOR (Concise Binary Object Representation).

    To use this serializer backend, the ``cbor`` library must be installed.
    A convenient way to do this is to install ``asphalt-serialization`` with the ``cbor``
    extra:

    .. code-block:: shell

        $ pip install asphalt-serialization[cbor]

    .. seealso:: `CBOR web site <http://cbor.io/>`_

    :param sort_keys: ``True`` to output dictionary items by keys when serializing
    """

    __slots__ = '_sort_keys'

    def __init__(self, sort_keys: bool=False):
        assert check_argument_types()
        self._sort_keys = sort_keys

    def serialize(self, obj) -> bytes:
        return cbor.dumps(obj, self._sort_keys)

    def deserialize(self, payload: bytes):
        return cbor.loads(payload)

    @property
    def mimetype(self):
        return 'application/cbor'
