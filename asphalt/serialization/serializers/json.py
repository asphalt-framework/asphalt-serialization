from typing import Dict, Any
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder

from typeguard import check_argument_types
from asphalt.core.util import resolve_reference

from ..api import Serializer


class JSONSerializer(Serializer):
    """
    Serializes objects using JSON (JavaScript Object Notation).

    See the :mod:`json` module documentation in the standard library for more information on
    available options.

    Certain options can resolve references to objects:

    * ``encoder_options['default']``
    * ``decoder_options['object_hook']``
    * ``decoder_options['object_pairs_hook']``

    :param encoder_options: keyword arguments passed to :class:`~json.JSONEncoder`
    :param decoder_options: keyword arguments passed to :class:`~json.JSONDecoder`
    :param encoding: the text encoding to use for converting to and from bytes
    """

    __slots__ = 'encoding', '_encoder', '_decoder'

    def __init__(self, encoder_options: Dict[str, Any]=None, decoder_options: Dict[str, Any]=None,
                 encoding: str='utf-8'):
        assert check_argument_types()
        self.encoding = encoding
        encoder_options = encoder_options or {}
        encoder_options['default'] = resolve_reference(encoder_options.get('default'))
        self._encoder = JSONEncoder(**encoder_options)

        decoder_options = decoder_options or {}
        decoder_options['object_hook'] = resolve_reference(decoder_options.get('object_hook'))
        decoder_options['object_pairs_hook'] = resolve_reference(
            decoder_options.get('object_pairs_hook'))
        self._decoder = JSONDecoder(**decoder_options)

    def serialize(self, obj) -> bytes:
        return self._encoder.encode(obj).encode(self.encoding)

    def deserialize(self, payload: bytes):
        payload = payload.decode(self.encoding)
        return self._decoder.decode(payload)

    @property
    def mimetype(self):
        return 'application/json'
