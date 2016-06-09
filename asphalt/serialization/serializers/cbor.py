from typing import Dict, Any

from typeguard import check_argument_types
import cbor2

from asphalt.serialization.api import Serializer


class CBORSerializer(Serializer):
    """
    Serializes objects using CBOR (Concise Binary Object Representation).

    To use this serializer backend, the ``cbor2`` library must be installed.
    A convenient way to do this is to install ``asphalt-serialization`` with the ``cbor``
    extra:

    .. code-block:: shell

        $ pip install asphalt-serialization[cbor]

    .. seealso:: `cbor2 documentation <https://pypi.io/project/cbor2/>`_

    :param encoder_options: keyword arguments passed to ``cbor2.dumps()``
    :param decoder_options: keyword arguments passed to ``cbor2.loads()``
    """

    __slots__ = '_encoder_options', '_decoder_options'

    def __init__(self, encoder_options: Dict[str, Any] = None,
                 decoder_options: Dict[str, Any] = None):
        assert check_argument_types()
        self._encoder_options = encoder_options or {}
        self._decoder_options = decoder_options or {}

    def serialize(self, obj) -> bytes:
        return cbor2.dumps(obj, **self._encoder_options)

    def deserialize(self, payload: bytes):
        return cbor2.loads(payload, **self._decoder_options)

    @property
    def mimetype(self):
        return 'application/cbor'
