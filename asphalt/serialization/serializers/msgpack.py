from typing import Dict, Any

from typeguard import check_argument_types

from ..api import Serializer

try:
    from msgpack import packb, unpackb
except ImportError:  # pragma: no cover
    raise ImportError('msgpack-python is missing -- install '
                      'asphalt-serialization[msgpack] to fix this')


class MsgpackSerializer(Serializer):
    """
    Serializes objects using the msgpack library.

    The following defaults are passed to packer/unpacker and can be overridden by setting values
    for the options explicitly:

    * ``use_bin_type=True`` (packer)
    * ``encoding='utf-8'`` (unpacker)

    To use this serializer backend, the ``msgpack-python`` library must be installed.
    A convenient way to do this is to install ``asphalt-serialization`` with the ``msgpack``
    extra:

    .. code-block:: shell

        $ pip install asphalt-serialization[msgpack]

    .. seealso:: `Msgpack web site <http://msgpack.org/>`_

    :param packer_options: keyword arguments passed to :func:`msgpack.packb`
    :param unpacker_options: keyword arguments passed to :func:`msgpack.unpackb`
    """

    __slots__ = '_packer_options', '_unpacker_options'

    def __init__(self, packer_options: Dict[str, Any]=None, unpacker_options: Dict[str, Any]=None):
        assert check_argument_types()
        packer_options = packer_options or {}
        packer_options.setdefault('use_bin_type', True)
        self._packer_options = packer_options

        unpacker_options = unpacker_options or {}
        unpacker_options.setdefault('encoding', 'utf-8')
        self._unpacker_options = unpacker_options

    def serialize(self, obj) -> bytes:
        return packb(obj, **self._packer_options)

    def deserialize(self, payload: bytes):
        return unpackb(payload, **self._unpacker_options)

    @property
    def mimetype(self):
        return 'application/x-msgpack'
